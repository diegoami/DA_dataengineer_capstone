import psycopg2
import requests
from wikimovies import sparkql_queries
from wikimovies import insert_queries


WIKIDATA_URL = 'https://query.wikidata.org/sparql'



def process_data(cur, sparkl_query, insert_query, insert_query_columns):
    r = requests.get(WIKIDATA_URL, params={'format': 'json', 'query': sparkl_query})
    data = r.json()
    for item in data['results']['bindings']:
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


    process_data(cur, sparkql_queries.occupations_sparkql, insert_queries.insert_occupation, insert_queries.insert_occupation_columns)

    conn.close()


main()