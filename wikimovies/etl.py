import requests
import os
import json

from wikimovies.sparkql_queries import *
from wikimovies.staging_queries import *
from wikimovies import load_queries
from wikimovies.text_file import export_to_csv, try_read_data_from_json_file

WIKIDATA_URL = 'https://query.wikidata.org/sparql'


class ETLProcessor:
    """
    class encapsulating the ETL processing logic
    """

    def __init__(self, cur, conn, config):
        self.cur = cur
        self.conn = conn
        self.config = config

    def process_data(self, table_name, sparkl_query, insert_query, map_query_columns, year=None):
        insert_query_columns = map_query_columns.keys()
        base_file_name = "{}_{}".format(table_name, year) if year else table_name
        sparkl_query = sparkl_query.format(year, year+1) if year else sparkl_query

        file_output = os.path.join("json", f"{base_file_name}.json")
        exp_output = os.path.join("json", f"{base_file_name}_exp.csv")
        if self.config['ETL']['READ_JSON']:
            rel_data = try_read_data_from_json_file(file_output)

        if not rel_data:
            print("Executing query in Sparkql: {}".format(sparkl_query))
            r = requests.get(WIKIDATA_URL, params={'format': 'json', 'query': sparkl_query})
            data = r.json(strict=False)

            rel_data = [item for item in data['results']['bindings']]
            if self.config['ETL']['WRITE_JSON']:
                with open(file_output, 'w', encoding="utf-8") as fhandle:
                    print("Writing to {}".format(file_output))
                    json.dump(rel_data, fhandle)
        if self.config['ETL']['WRITE_CSV']:
            exp_data = [{map_query_columns[column]: item[column]['value'] for column in insert_query_columns} for item in rel_data]
            export_to_csv(exp_data, exp_output, map_query_columns)

        self.insert_records(insert_query, insert_query_columns, rel_data, table_name)

        self.conn.commit()



    def insert_records(self, insert_query, insert_query_columns, rel_data, table_name):
        print("Inserting {} rows into  {}".format(len(rel_data), table_name))
        for index, item in enumerate(rel_data):
            values_to_insert = [item[column]['value'] for column in insert_query_columns]
            try:
                self.cur.execute(insert_query, values_to_insert)
            except ValueError as ve:
                print("Could not execute query : {} with values".format(insert_query, values_to_insert))
                raise ve

            if index % 1000 == 0:
                print("Inserted {} rows".format(index))

        print("Finished inserting {}".format(table_name))


    def insert_relations_staging(self):

       self.process_data("movie_roles", movies_roles_sparkql, insert_movie_role, map_movie_role_columns)
       self.process_data("tvshow_roles", tvshow_roles_sparkql, insert_tvshow_role, map_tvshow_role_columns)
       self.process_data("song_roles", song_roles_sparkql, insert_song_role, map_song_role_columns)
       self.process_data("animatedmovie_roles", animatedmovie_roles_sparkql, insert_animatedmovie_role, map_animatedmovie_role_columns)
       self.process_data("videogame_roles", videogame_roles_sparkql, insert_videogame_role, map_videogame_role_columns)
       self.process_data("book_roles", book_roles_sparkql, insert_book_role, map_book_role_columns)


    def insert_entities_staging(self):
        self.process_data("movies", movies_sparkql, insert_movie, map_movie_columns)
        self.process_data("tvshows", tvshows_sparkql, insert_tvshow, map_tvshow_columns)
        self.process_data("animatedmovies", animatedmovies_sparkql, insert_animatedmovie, map_animatedmovie_columns)
        self.process_data("songs", songs_sparkql, insert_song, map_song_columns)
        self.process_data("videogames", videogames_sparkql, insert_videogame, map_videogame_columns)
        self.process_data("books", books_sparkql, insert_book, map_book_columns)


    def insert_roles_staging(self):

        self.process_data("roles", roles_sparkql, insert_role,
                     map_role_columns)


    def insert_humans_staging(self):
        for year in range(1880, 2020):
            self.process_data("humans", humans_byyear_sparkql, insert_human,
                         map_human_columns, year=year)

    def load_tables(self):
        print("Loading the creative works table")
        self.cur.execute(load_queries.insert_creative_works)
        self.conn.commit()

        print("Loading the participations table")

        self.cur.execute(load_queries.insert_participations)
        self.conn.commit()
