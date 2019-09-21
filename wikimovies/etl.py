import datetime
import requests
import os
import json
import time
import sys
from json.decoder import JSONDecodeError
from http.client import IncompleteRead

from wikimovies.sparql_queries import *
from wikimovies.staging_queries import *
from wikimovies import dwh_queries
from wikimovies.text_file import try_read_data_from_json_file, save_to_s3, try_read_data_from_s3


# URL of the Wikidata endpoint accepting queris in Sparql
WIKIDATA_URL = 'https://query.wikidata.org/sparql'

# The year we start retrieve humans from
START_YEAR_HUMANS = 1880

# The year we start retrieve creative works from
START_YEAR_CREATIVE_WORKS = 1900

# The range in years used to split queries from Wikidata
YEARS_RANGE = 3

# The current year
CURRENT_YEAR = datetime.datetime.now().year

# How many seconds to retry after a query to wikidata was not successuf
RETRY_INTERVAL = 30

# How many tries to call wikidata until it fails
NUM_TRIES = 20



class ELTProcessor:
    """
    class encapsulating the ELT processing logic.
    It extracts data from Wikidata, loads it into a postgres Database and transforms it into facts/dimensions,
        so that they can easily utilized by an analist.
    """

    def __init__(self, cur, conn, config):
        """
        class initialization
        :param cur: postgres cursor
        :param conn: postgres connection
        :param config: configuration information from the wikimovies.cfg file
        """
        self.cur = cur
        self.conn = conn
        self.config = config

        self.cache_dir = config['ETL']['CACHE_DIRECTORY']
        if not os.path.exists(self.cache_dir):
            os.mkdir(self.cache_dir)
            print("Directory json created ")
        else:
            print("Directory json already exists")



    def check_config(self, section, key):
        """
        true if a key in the config file has value True or Yes
        :param section: section in the config file
        :param key: key in the config file
        :return:
        """
        value = self.config[section][key]
        return value.lower() == 'yes' or value.lower() == 'true'


    def load_wikidata(self, table_name, sparql_query, insert_query,
                      map_query_columns, year=None, year_offset=1,
                      repeat_years=False):
        """

        :param table_name: the target Postgres table
        :param sparql_query: the wikidata sparql query
        :param insert_query: the query to insert data in postgres
        :param map_query_columns: the mapping between columns in sparql and those
        :param year: the start year to limit the query
        :param year_offset: how many years from start year to include in the query
        :param repeat_years: whether the year patterns appear twice in the sparql query
        """

        insert_query_columns = map_query_columns.keys()
        object_name = "{}_{}_{}".format(table_name, year, year + year_offset) if year else table_name
        sparql_query = (sparql_query.format(year, year + year_offset, year, year + year_offset) if repeat_years else sparql_query.format(year, year + year_offset)) if year else sparql_query
        base_name = "{}.json".format(object_name)
        file_output = os.path.join(self.cache_dir, base_name)
        result_data = None

        if self.check_config('ETL', 'READ_JSON_LOCAL'):
            print("Trying to Read locally from {}".format(file_output))
            result_data = try_read_data_from_json_file(file_output)
            if result_data is None:
                print("Could not read from {}".format(file_output))

        if result_data is None and self.check_config('S3', 'READ_FROM_S3'):
            region_name = self.config['S3']['REGION_NAME']
            bucket_name = self.config['S3']['BUCKET_NAME']
            result_data = try_read_data_from_s3(bucket_name, base_name, file_output, region_name)
            if result_data is None:
                print("Could not read data from s3://{}/{} to {}".format(bucket_name, base_name, file_output))
            else:
                print("Downloaded from s3://{}/{} to {}".format(bucket_name, base_name, file_output))
        if result_data is None:
            print("Executing query in Sparkql: {}".format(sparql_query))
            ok = False
            tries = 0
            interval = RETRY_INTERVAL
            while not ok and tries < NUM_TRIES:
                tries += 1
                try:
                    with requests.get(WIKIDATA_URL, params={'format': 'json', 'query': sparql_query}) as r:
                        if r.ok:
                            try:
                                data = r.json(strict=False)
                            except JSONDecodeError as jse:
                                print("Invalid JSON received ...trying again in {} seconds".format(interval))
                                time.sleep(interval)
                                interval *= 2
                                print("Retrying query...")
                                continue
                            result_data = [item for item in data['results']['bindings']]
                            if self.check_config('ETL', 'WRITE_JSON_LOCAL'):
                                with open(file_output, 'w', encoding="utf-8") as fhandle:
                                    print("Writing to {}".format(file_output))
                                    json.dump(result_data, fhandle)
                            ok = True
                        else:
                            print("Request not OK: {}, {}".format(r.status_code, r.reason))
                            if r.status_code == 429:
                                numbers = [int(word) for word in r.reason.split() if word.isdigit()]
                                number = max(numbers[0] + 1, 5)
                                print("Too many requests ... trying in {} seconds".format(number))
                                time.sleep(number)
                                print("Retrying query...")
                            else:
                                print("Unknown status - exiting")
                                sys.exit(1)
                except IncompleteRead as ir:
                    print("Incomplete read - trying again in {} seconds".format(interval))
                    time.sleep(interval)
                    interval *= 2
                    print("Retrying query...")
                    continue
            if tries >= NUM_TRIES:
                print("Wikidata not reachable - exiting")
                sys.exit(1)
        if self.check_config('S3', 'WRITE_TO_S3') and os.path.isfile(file_output):
            bucket_name = self.config['S3']['BUCKET_NAME']
            print("Saving to S3: {}/{}".format(bucket_name, base_name))
            save_to_s3(bucket_name, file_output, base_name)

        self.insert_records(insert_query, insert_query_columns, result_data, table_name)
        self.conn.commit()



    def insert_records(self, insert_query, insert_query_columns, wiki_data, table_name):
        """
        insert retrieved records from wikidata into a postgres table
        :param insert_query: the query to insert data into postggres
        :param insert_query_columns: the name of the columns for which to insert values
        :param wiki_data: data retrieved from Wikidata
        :param table_name: name of the table where to insert data
        :return:
        """
        print("Inserting {} rows into  {}".format(len(wiki_data), table_name))
        for index, item in enumerate(wiki_data):
            values_to_insert = [item[column]['value'] for column in insert_query_columns]
            try:
                self.cur.execute(insert_query, values_to_insert)
            except ValueError as ve:
                print("Could not execute query : {} with values".format(insert_query, values_to_insert))
                raise ve

            if index % 1000 == 0:
                print("Inserted {} rows".format(index))
        print("Inserted {} rows".format(len(wiki_data)))
        print("Finished inserting {}".format(table_name))



    def insert_relations_staging(self):
       """
       insert data in the staging tables for relations between entities and people
       """

       for year in range(START_YEAR_CREATIVE_WORKS, CURRENT_YEAR, YEARS_RANGE):
            self.load_wikidata("movie_roles", MOVIE_ROLES_BY_YEAR_SPARQL_QUERY, INSERT_MOVIE_ROLE_SQL_QUERY, INSERT_MOVIE_ROLE_MAP_COLUMNS, year, YEARS_RANGE)
            self.load_wikidata("tvshow_roles", TVSHOW_ROLES_BY_YEAR_SPARQL_QUERY, INSERT_TVSHOW_ROLE_SQL_QUERY, INSERT_TVSHOW_ROLE_MAP_COLUMNS, year, YEARS_RANGE)
            self.load_wikidata("animatedmovie_roles", ANIMATEDMOVIE_ROLES_BY_YEAR_SPARQL_QUERY, INSERT_ANIMATEDMOVIE_ROLE_SQL_QUERY, INSERT_ANIMATEDMOVIE_ROLE_MAP_COLUMNS, year, YEARS_RANGE)
            self.load_wikidata("song_roles", SONG_ROLES_BY_YEAR_SPARQL_QUERY, INSERT_SONG_ROLE_SQL_QUERY, INSERT_SONG_ROLE_MAP_COLUMNS, year, YEARS_RANGE, True)

       self.load_wikidata("videogame_roles", VIDEOGAME_ROLES_SPARQL_QUERY, INSERT_VIDEOGAME_ROLE_SQL_QUERY, INSERT_VIDEOGAME_ROLE_MAP_COLUMNS)
       self.load_wikidata("book_roles", BOOK_ROLES_SPARQL_QUERY, INSERT_BOOK_ROLE_SQL_QUERY, INSERT_BOOk_ROLE_SQL_QUERY)


    def insert_entities_staging(self):
        """
        insert data in the staging tables for entities
        """

        for year in range(1900, CURRENT_YEAR, YEARS_RANGE):
            self.load_wikidata("movies", MOVIES_BY_YEAR_SPARQL_QUERY, INSERT_MOVIE_SQL_QUERY, INSERT_MOVIE_MAP_COLUMNS, year, YEARS_RANGE)
            self.load_wikidata("tvshows", TVSHOWS_BY_YEAR_SPARQL_QUERY, INSERT_TVSHOW_SQL_QUERY, INSERT_TVSHOW_MAP_COLUMNS, year, YEARS_RANGE)
            self.load_wikidata("animatedmovies", ANIMATEDMOVIES_BY_YEAR_SPARQL_QUERY, INSERT_ANIMATEDMOVIE_SQL_QUERY, INSERT_ANIMATEDMOVIE_MAP_COLUMNS, year, YEARS_RANGE)
            self.load_wikidata("songs", SONGS_BY_YEAR_SPARQL_QUERY, INSERT_SONG_SQL_QUERY, INSERT_SONG_MAP_COLUMNS, year, YEARS_RANGE, True)
        self.load_wikidata("videogames", VIDEOGAMES_SPARQL_QUERY, INSERT_VIDEOGAME_SQL_QUERY, INSERT_VIDEOGAME_MAP_COLUMNS)
        self.load_wikidata("books", BOOKS_SPARQL_QUERY, INSERT_BOOK_SQL_QUERY, INSERT_BOOK_MAP_COLUMNS)


    def insert_roles_staging(self):
        """
        insert data in the staging tables for roles
        """

        self.load_wikidata("roles", ROLES_SPARQL_QUERY, INSERT_ROLE_SQL_QUERY,
                           INSERT_ROLE_MAP_COLUMNS)


    def insert_humans_staging(self):
        """
        insert data in the staging tables for humans
        """
        for year in range(1880, CURRENT_YEAR):
            self.load_wikidata("humans", HUMANS_BY_YEAR_SPARQL_QUERY, INSERT_HUMAN_SQL_QUERY,
                               INSERT_HUMAN_MAP_COLUMNS, year=year)


    def load_dwh_tables(self):
        """
        loads data into the DWH tables
        """
        print("Loading the creative works table")
        self.cur.execute(dwh_queries.INSERT_CREATIVE_WORKS_SQL_QUERY)
        self.conn.commit()

        print("Loading the participations table")

        self.cur.execute(dwh_queries.INSERT_PARTICIPATIONS_SQL_QUERY)
        self.conn.commit()
