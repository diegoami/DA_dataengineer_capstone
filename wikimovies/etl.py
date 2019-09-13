import psycopg2
import requests
import os
import json
from wikimovies import sparkql_queries
from wikimovies import insert_queries


WIKIDATA_URL = 'https://query.wikidata.org/sparql'



def process_data(cur, query_name, sparkl_query, insert_query, insert_query_columns, year=None):
    r = requests.get(WIKIDATA_URL, params={'format': 'json', 'query': sparkl_query})
    data = r.json(strict=False)
    file_output = os.path.join("json", f"{query_name}.json")
    exp_output = os.path.join("json", f"{query_name}_exp.json")

    rel_data = [item for item in data['results']['bindings']]
    exp_data = [{column: item[column]['value'] for column in insert_query_columns} for item in rel_data]

    with open(file_output, 'w', encoding="utf-8") as fhandle:
        json.dump(rel_data, fhandle)
    with open(exp_output, 'w', encoding="utf-8") as ehandle:
        json.dump(exp_data, ehandle)
    for item in rel_data:
        values_to_insert = [item[column]['value'] for column in insert_query_columns]
        print(values_to_insert)
        cmd_to_execute = insert_query.format(*values_to_insert)
        print(cmd_to_execute)
        cur.execute(insert_query, values_to_insert)
        print("executed {} with {}".format(insert_query, values_to_insert))

    cur.execute("COMMIT")

def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=wikidata user=wikidata password=wikidata")
    cur = conn.cursor()


    process_data(cur, "occupations", sparkql_queries.occupations_sparkql, insert_queries.insert_occupation, insert_queries.insert_occupation_columns)

    process_data(cur, "roles", sparkql_queries.roles_sparkql, insert_queries.insert_role, insert_queries.insert_role_columns)

    process_data(cur, "movies", sparkql_queries.movies_sparkql, insert_queries.insert_movie, insert_queries.insert_movie_columns)

    process_data(cur, "tvshows", sparkql_queries.tvshows_sparkql, insert_queries.insert_tvshow, insert_queries.insert_tvshow_columns)

    process_data(cur, "animatedmovies", sparkql_queries.animatedmovies_sparkql, insert_queries.insert_animatedmovie, insert_queries.insert_animatedmovie_columns)

    process_data(cur, "videogames", sparkql_queries.videogames_sparkql, insert_queries.insert_videogame,
                 insert_queries.insert_videogame_columns)

    process_data(cur, "books", sparkql_queries.books_sparkql, insert_queries.insert_book,
                 insert_queries.insert_book_columns)


    conn.close()


main()