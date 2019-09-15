# DA_dataengineer_capstone

## DATA SOURCE



The data is retrieved from wikidata using SPARQL in the first steps of the pipeline.
We retrieve information about 

* People on the Wikipedia (born after 1880)

and these type of creative works


* Movies
* Animated movies
* Tv shows
* Video games
* songs 
* Books

We also retrieve information about the relation between people and creative works. 

The idea is to build a database that would allow us to find out people who have been working on different types of creative works, for instance to find out what actors also perform songs, are voice actors in animated movies and games, or write books.


## CREATE DATABASE AND TABLES

To create the required tables in a Postgres database, execute the scripts `create_tables_staging.sql` and `create_tables_dwh.sql`

## PIPELINE

### STAGING

We fill the staging table importing data from Wikidata. Business logic is in `etl_staging` and queries are in `insert_queries`

### BUILD FACT/DIMENSION TABLES

We will transform staging tables into fact / dimension table for ease of querying. We are interested in 

* People (DIMENSION)
* Creative works (DIMENSION)
* Whether a person participated in a creative work (FACT)

## QUERIES

The queries retrieve entities' id and their labels in english from wikidata.


# SET UP DATABASE

```
CREATE DATABASE wikidata;
create user wikidata with encrypted password 'wikidata';
grant all privileges on database wikidata to wikidata;

\connect wikidata;
\i create_table.sql;
```