import psycopg2
import configparser

from wikimovies.etl import insert_humans_staging, insert_roles_staging, insert_entities_staging, \
    insert_relations_staging, load_tables

from wikimovies.ddl_queries import create_database

def main():
    config = configparser.ConfigParser()
    config.read('wikimovies.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['DB'].values()))

    cur = conn.cursor()

    create_database(cur, conn)

    insert_humans_staging(cur, conn)
    insert_roles_staging(cur, conn)
    insert_entities_staging(cur, conn)
    insert_relations_staging(cur, conn)

    load_tables(cur, conn)
    conn.close()

if __name__ == "__main__":
    main()