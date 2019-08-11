# DA_dataengineer_capstone

## DATA SOURCE



The data is retrieved from wikidata using SPARQL in the first steps of the pipeline.
We retrieve information about these entities


* People on the Wikipedia (born after 1850)
* Their occupation
* How many sitelinks

The idea is to build a database that would allow us to find out what person work on different types of media, for instance to find out what actors also perform songs, are voice actors in animated movies or write books.




## PIPELINE

### FIRST STEP: AIRFLOW, STAGING TABLES

We will build airflow jobs, with custom operators, to retrieve data from wikidata using their REST API, und upload data to staging tables in Redshift (or Postgres ).

### SECOND STEP: BUILD FACT/DIMENSION TABLES

We will load data into a simplified schema into Redshift (Postgres), where the main tables will be

* Person `Dimension`
* Occupation 

## QUERIES

The queries retrieve entities' id and their labels in english from wikidata.

### HUMANS

People in Wikipedia (with labels and occupations    ) - we need to retrieve them year by year

```
SELECT ?human ?humanLabel ?occupation ?linkcount WHERE {
  ?human wdt:P31 wd:Q5;
     wdt:P569 ?born .
  
  FILTER (?born >= "1980-01-01"^^xsd:dateTime && ?born < "1981-01-01"^^xsd:dateTime) .
   ?human wikibase:sitelinks ?linkcount .
  OPTIONAL { ?human wdt:P106 ?occupation } 
  SERVICE wikibase:label {
     bd:serviceParam wikibase:language "en" .
  }
  
}
```


### PROFESSIONS

```
SELECT (COUNT(?human) AS ?humanC) ?occupation (SUM(?linkcount) as ?linkcountS) WHERE {
  ?human wdt:P31 wd:Q5;
     wdt:P569 ?born .
  
  FILTER (?born >= "1980-01-01"^^xsd:dateTime) .
   ?human wikibase:sitelinks ?linkcount .
  OPTIONAL { ?human wdt:P106 ?occupation } 
  
}
GROUP BY (?occupation)
ORDER BY DESC (?humanC) DESC (?linkcountS)
```