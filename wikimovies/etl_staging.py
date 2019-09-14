import requests
import os
import json
import csv
import traceback


from wikimovies import sparkql_queries
from wikimovies import insert_queries


WIKIDATA_URL = 'https://query.wikidata.org/sparql'



def process_data(cur, table_name, sparkl_query, insert_query, map_query_columns, fetchIfPresent=False, year=None):
    insert_query_columns = map_query_columns.keys()
    base_file_name = "{}_{}".format(table_name, year) if year else table_name
    sparkl_query = sparkl_query.format(year, year+1) if year else sparkl_query


    file_output = os.path.join("json", f"{base_file_name}.json")
    exp_output = os.path.join("json", f"{base_file_name}_exp.csv")
    rel_data = None
    if os.path.isfile(file_output) and not fetchIfPresent:
        print("Reading data from file {}".format(file_output))
        with open(file_output, 'r', encoding="utf-8") as fhandle:
            try:
                rel_data = json.load(fhandle)
            except ValueError as ve:
                traceback.print_exc(ve)
                print("Could not read data from file {}".format(file_output))
    if not rel_data:
        print("Executing query in Sparkql: {}".format(sparkl_query))
        r = requests.get(WIKIDATA_URL, params={'format': 'json', 'query': sparkl_query})
        data = r.json(strict=False)

        rel_data = [item for item in data['results']['bindings']]
        with open(file_output, 'w', encoding="utf-8") as fhandle:
            print("Writing to {}".format(file_output))
            json.dump(rel_data, fhandle)

    exp_data = [{map_query_columns[column]: item[column]['value'] for column in insert_query_columns} for item in rel_data]
    with open(exp_output, 'w', encoding="utf-8") as ehandle:
        print("Writing to {}".format(exp_output))

        f = csv.writer(ehandle)

        # Write CSV Header, If you dont need that, remove this line
        f.writerow(map_query_columns.values() )
        for item in exp_data:
            f.writerow(item.values())


    insert_records(cur, insert_query, insert_query_columns, rel_data, table_name)

    cur.execute("COMMIT")

def copy_records(cur, input_file, output_table):
    ps_command = "COPY {} FROM '{}' CSV".format(output_table, input_file)
    copy_string = 'PGPASSWORD=wikidata psql  -h 127.0.0.1 -d wikidata -U wikidata -c "{}"'
    command = copy_string.format(ps_command)
    print("Executing command {}".format(command))
    out = os.popen(command).read()
    print(out)


def insert_records(cur, insert_query, insert_query_columns, rel_data, table_name):
    inserted=0
    print("Inserting {} rows into  {}".format(len(rel_data), table_name))
    for index, item in enumerate(rel_data):
        values_to_insert = [item[column]['value'] for column in insert_query_columns]
        try:
            cur.execute(insert_query, values_to_insert)
        except ValueError as ve:
            print("Could not execute query : {} with values".format(insert_query, values_to_insert))
            raise ve

        if index % 100 == 0:
            print("Inserted {} rows".format(index))

    print("Finished inserting {}".format(table_name))


def insert_relations_staging(cur):
    process_data(cur, "movie_roles", sparkql_queries.movies_roles_sparkql, insert_queries.insert_movie_role,
                 insert_queries.map_movie_role_columns)
    process_data(cur, "tvshow_roles", sparkql_queries.tvshow_roles_sparkql, insert_queries.insert_tvshow_role,
                 insert_queries.map_tvshow_role_columns)
    process_data(cur, "song_roles", sparkql_queries.song_roles_sparkql, insert_queries.insert_song_role,
                 insert_queries.map_song_role_columns)
    process_data(cur, "animatedmovie_roles", sparkql_queries.animatedmovie_roles_sparkql,
                 insert_queries.insert_animatedmovie_role,
                 insert_queries.map_animatedmovie_role_columns)
    process_data(cur, "videogame_roles", sparkql_queries.videogame_roles_sparkql,
                 insert_queries.insert_videogame_role,
                 insert_queries.map_videogame_role_columns)
    process_data(cur, "book_roles", sparkql_queries.book_roles_sparkql,
                 insert_queries.insert_book_role,
                 insert_queries.map_book_role_columns)


def insert_entities_staging(cur):
    process_data(cur, "movies", sparkql_queries.movies_sparkql, insert_queries.insert_movie,
                 insert_queries.map_movie_columns)
    process_data(cur, "tvshows", sparkql_queries.tvshows_sparkql, insert_queries.insert_tvshow,
                 insert_queries.map_tvshow_columns)
    process_data(cur, "animatedmovies", sparkql_queries.animatedmovies_sparkql, insert_queries.insert_animatedmovie,
                 insert_queries.map_animatedmovie_columns)
    process_data(cur, "videogames", sparkql_queries.videogames_sparkql, insert_queries.insert_videogame,
                 insert_queries.map_videogame_columns)
    process_data(cur, "books", sparkql_queries.books_sparkql, insert_queries.insert_book,
                 insert_queries.map_book_columns)


def insert_roles_staging(cur):
    process_data(cur, "occupations", sparkql_queries.occupations_sparkql, insert_queries.insert_occupation,
                 insert_queries.map_occupation_columns)
    process_data(cur, "roles", sparkql_queries.roles_sparkql, insert_queries.insert_role,
                 insert_queries.map_role_columns)


def insert_humans_staging(cur):
    for year in range(1880, 2020):
        process_data(cur, "humans", sparkql_queries.humans_byyear_sparkql, insert_queries.insert_human,
                     insert_queries.map_human_columns, year=year)


