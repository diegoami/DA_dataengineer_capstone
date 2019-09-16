import psycopg2
import configparser

from wikimovies.etl import ETLProcessor
from wikimovies.ddl_queries import create_database


def main():
    config = configparser.ConfigParser()
    config.read('wikimovies.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['DB'].values()))

    cur = conn.cursor()

    create_database(cur, conn)

    data_processor = ETLProcessor(cur=cur, conn=conn, config=config)
    data_processor.insert_humans_staging()
    data_processor.insert_roles_staging()
    data_processor.insert_entities_staging()
    data_processor.insert_relations_staging()

    data_processor.load_tables()
    conn.close()


if __name__ == "__main__":
    main()