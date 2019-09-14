import psycopg2

from wikimovies.etl_staging import insert_humans_staging, insert_roles_staging, insert_entities_staging, \
    insert_relations_staging


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=wikidata user=wikidata password=wikidata")
    cur = conn.cursor()

    insert_humans_staging(cur)

    insert_roles_staging(cur)

    insert_entities_staging(cur)

    insert_relations_staging(cur)


    conn.close()

main()