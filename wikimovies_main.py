"""Wikimovies main entry point

Usage:
  wikimovies_main.py do_all
  wikimovies_main.py create_tables
  wikimovies_main.py load_staging
  wikimovies_main.py load_dwh
  wikimovies_main.py load_all
  wikimovies_main.py test_tables


  wikimovies_main.py (-h | --help)

Options:
  -h --help     Show this screen.

"""
from docopt import docopt

import psycopg2
import configparser

from wikimovies.etl import ETLProcessor
from wikimovies.ddl_queries import create_schema
from wikimovies.test_queries import execute_tests


def load_staging():
    print("Loading data into staging tables")
    data_processor = ETLProcessor(cur=cur, conn=conn, config=config)
    data_processor.insert_humans_staging()
    data_processor.insert_roles_staging()
    data_processor.insert_entities_staging()
    data_processor.insert_relations_staging()


def load_dwh():
    print("Loading data into DWH tables")
    data_processor = ETLProcessor(cur=cur, conn=conn, config=config)
    data_processor.load_tables()


if __name__ == "__main__":
    arguments = docopt(__doc__)

    config = configparser.ConfigParser()
    config.read('wikimovies.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['DB'].values()))
    cur = conn.cursor()

    if arguments['create_tables'] or arguments['do_all']:
        create_schema(cur, conn)
    if arguments['load_staging'] or arguments['do_all'] or arguments['load_all']:
        load_staging()
    if arguments['load_dwh'] or arguments['do_all'] or arguments['load_all']:
        load_dwh()
    if arguments['test_tables'] or arguments['do_all']:
        execute_tests(cur)
    conn.close()