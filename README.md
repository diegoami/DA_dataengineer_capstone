# DA_dataengineer_capstone

## TASK

This is the capstone project for the Data Engineering nanodegree on Udacity. I decided to design my own project, using data from wikipedia.
In this project you have to 

* Scope the Project and Gather Data
* Explore and Assess the Data
* Define the Data Model
* Run ETL to Model the Data
* Complete Project Write Up


## OVERVIEW

### GOAL

The idea is to build a database from [Wikipedia](https://www.wikipedia.org/), that would allow analytics to find out people who have been working on different types of creative works, for instance to find out what actors also perform songs, are voice actors in animated movies and games, or write books.



### TYPE OF DATA

We retrieve information about 

* People on the Wikipedia (born after 1880)

and these type of creative works

* Movies
* Animated movies
* Tv shows
* Video games
* Songs 
* Books

and what people have been working on what creative works, and in what roles.

### TOOLS USED

For the amount of data I am working with, I decided to use a Postgres database, that I can start either locally or as a RDS database. On this database I put both the staging and the DWH tables.
Data is read from Wikidata, but is optionally cached in a S3 bucket.

To retrieve data, we use the API from [Wikidata](https://www.wikidata.org/) and the `requests` library. We save data in a S3 bucket, that can be used as a cache when wikidata is not accessible.


## EXECUTION

### CONFIGURE

To configure the project, you need to make a copy of `wikimovies_template.cfg` to `wikimovie.cfg` and set up the following Section

* **DB**  : The database configuration data
* **ETL** : parameters relating to the ETL workflow
* **S3**  : S3 configuration data. 

Note that you will need to configure your AWS credentials 


### SET UP ENVIRONMENT

You need to have an installation of `postgres` and `python`, with the libraries listed in requirements.txt . See `Dockerfile` for reference of what should be installed.
As a rule, you need 

* `postgres`, along with the required libraries for accessing it as a client and in python. 
* `python` and an environment where you can set up the libraries listed in `requirements.txt`
* A database `wikidata` where to save data in postgres

If you want to set up a docker container, install `docker` and execute following commands

* `docker build -t wikimovies_capstone .`
* `docker run -it -p 5432:5432 -e AWS_ACCESS_KEY_ID=<aws_access_key_id> AWS_SECRET_ACCESS_KEY=<aws_secret_access_key_id> --shm-size 2048m wikimovies_capstone /bin/bash` 

    
### EXECUTION 

Once you have set up a running environment and configured to connect to the correct database, execute these commands

* `python wikimovies_main.py create_tables`
* `python wikimovies_main.py load_staging`
* `python wikimovies_main.py load_dwh`
* `python wikimovies_main.py test_tables`

you can then connect to the postgres database on port 5432 and try and execute some of the queries listed in `test_queries.py`

## PIPELINE

### STAGING

We fill the staging table importing data from Wikidata in SPARQL, a semantic query language for databases. The queries used to retrieve data from it can be found in the file [wikimovies/sparql_queries.py](wikimovies/sparql_queries.py)

The _entities_ queries retrieve entities id and their labels in english from wikidata.
The _relations_ queries retrieve participation of people in creative works

### BUILD FACT/DIMENSION TABLES

We transform staging tables into fact / dimension table for ease of querying. We are interested in 

* People (DIMENSION)
    * human_id (PK, wikidata ID)
    * human_name
* Creative works (DIMENSION)
    * creative_work_id (PK, wikidata ID)
    * creative_work_name 
    * creative_work_type 
     
* Whether a person participated in a creative work (FACT)
    * human_id
    * creative_work_id
    * role



### QUERIES AND ANALYSIS

Examples of queries on how to access the database and retrieve relevant facts can be found in `test_queries.py`. Interesting information that for instance can be retrieved from the database is:

- in which creative works, and in what roles some person has been involved
- who has been developed the most creative works, of different types (such as e.g. songs and movies) and in different roles

### UPDATING DATA

As data in wikipedia can be updated regularly and across the board, the jobs should be repeated regularly to get more data. The nature of data on Wikipedia is such, that the process must be repeated over all years - we cannot be sure that people have not inserted information from previous years.

It is also the kind of data that does not need to be updated every day, but would be enough to update it every month. Therefore setting up Airflow for this may be an overkill. 

However, if the process had to be run every day, it would help to break down the tasks in smaller ones and have a scheduler deal with retrying tasks when wikidata is not reachable or tells you to try in some seconds. 

### SCALING DATA

The data that we have is around 2 millions humans (Dimension), 500k creative works (Dimension) and around 2 million participations of people in creative works (Fact).

If there was a hundred times more data, there are some things that we would have to change.

* as a target system, we would use Redshift. We would partition participations and humans over redshift nodes using human_id as a partition key (part key), to try and ensure that humans and their participations  are in the same partition. Creative works may be replicated over all nodes. Alternatively, if it is creative works that would explode, we would use creative_work_id as a part key, and replicate humans over all nodes.
* We would break down the process of retrieving data from Wikidata and transferring it into Postgres more clearly, at first retrieving all data from Wikidata, saving it all into csv files and using COPY to transfer it to Redshift. As of now, the process of retrieving data from Wikidata is much slower than the process of inserting it into the database (unless the database is remote) and therefore it does not make much of a difference using insert rather than COPY, unless we have previously saved data in S3.

If the data had to be accessed by a hundred people, with this amount of data postgres would be probably enough to deal with the load - just we would have to make sure that the database has enough connections.