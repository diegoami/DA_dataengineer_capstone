# DA_dataengineer_capstone

## DATA SOURCE



The data is retrieved from wikidata using SPARQL in the first steps of the pipeline.
We retrieve information about these entities, along with people that worked on them

* movies (along with cast, screenwriter, director...)
* songs (along with performers, author)
* tv shows(along with cast, screenwriter, director...)
* animated movies (along with voice actors, producers)
* video games (along with voice actors)
* books (along with author and creator)
*

The idea is to build a database that would allow us to find out what person work on different types of media, for instance to find out what actors also perform songs, are voice actors in animated movies or write books.




## PIPELINE

### FIRST STEP: AIRFLOW, STAGING TABLES

We will build airflow jobs, with custom operators, to retrieve data from wikidata using their REST API, und upload data to staging tables in Redshift (or Postgres ).

### SECOND STEP: BUILD FACT/DIMENSION TABLES

We will load data into a simplified schema into Redshift (Postgres), where the main tables will be

* Person `Dimension`
* Media `Dimension` (with a `media type` column: movie, tv show, song...)
* Participation `Fact` of a person in a media, along with a `role` column : actor, author, screenwriter... 

## QUERIES

The queries retrieve entities' id and their labels in english from wikidata.

### HUMANS

People in Wikipedia (with labels)

```
SELECT ?human ?humanLabel WHERE {
  ?human wdt:P31/wdt:P279* wd:Q5 .
   SERVICE wikibase:label {
     bd:serviceParam wikibase:language "en" .
  }
  
}
```

### MOVIES

Participation in movies as director, actor, composer, screen writer....
Records: ** **

```
SELECT ?film  ?role ?person l  WHERE {
  ?film wdt:P31 wd:Q11424;
    wdt:P57|wdt:P161|wdt:P162|wdt:P1431|wdt:P58|wdt:P344|wdt:P1040|wdt:P86|wdt:P2515|wdt:p2554|wdt:P170|wdt:P725 ?person.
  ?person ?role ?film.
}
```

Actors