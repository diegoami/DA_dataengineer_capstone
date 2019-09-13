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
  WHERE 
  FILTER (?born >= "1980-01-01"^^xsd:dateTime && ?born < "1981-01-01"^^xsd:dateTime) .
   ?human wikibase:sitelinks ?linkcount .
  OPTIONAL { ?human wdt:P106 ?occupation } 
  SERVICE wikibase:label {
     bd:serviceParam wikibase:language "en" .
  }
  
}
```

Humans excluding some profession:

```
SELECT ?human ?humanLabel ?occupation ?linkcount WHERE {
  ?human wdt:P31 wd:Q5;
     wdt:P569 ?born .

  FILTER (?born >= "1980-01-01"^^xsd:dateTime && ?born < "1981-01-01"^^xsd:dateTime) .
  FILTER (?occupation not in  ( wd:Q937857, wd:Q1650915, wd:Q3665646, wd:Q11774891, wd:Q11513337, wd:Q2309784, wd:Q2066131, wd:Q19204627, wd:Q14089670, wd:Q12299841, wd:Q10871364, wd:Q15117302, wd:Q13141064, wd:Q13365117,  wd:Q10873124) ) . 
   ?human wikibase:sitelinks ?linkcount .
  OPTIONAL { ?human wdt:P106 ?occupation } 
  SERVICE wikibase:label {
     bd:serviceParam wikibase:language "en" .
  }
  
}
```


### PROFESSIONS

Professions

```
SELECT ?occupation ?occupationLabel WHERE {
  ?occupation wdt:P31/wdt:P279* wd:Q12737077 .

  SERVICE wikibase:label {
     bd:serviceParam wikibase:language "en" .
  }

  
}
```

Humans and professions

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

````
SELECT (COUNT(?human) AS ?humanC) ?occupation ?occupationLabel (SUM(?linkcount) as ?linkcountS) WHERE {
  ?human wdt:P31 wd:Q5;
     wdt:P569 ?born .
  
  FILTER (?born >= "1980-01-01"^^xsd:dateTime) .
   ?human wikibase:sitelinks ?linkcount .
  OPTIONAL { ?human wdt:P106 ?occupation } 
  SERVICE wikibase:label {
     bd:serviceParam wikibase:language "en" .
  }

  
}
GROUP BY ?occupation ?occupationLabel

ORDER BY DESC (?humanC) DESC (?linkcountS)
````

### PARTICIPANTS

```
SELECT ?participant ?participantLabel WHERE {
  ?occupation wdt:P31/wdt:P279* wd:Q12737077 .

  SERVICE wikibase:label {
     bd:serviceParam wikibase:language "en" .
  }
}
```

### MOVIES

All movies with name
```
SELECT ?film  ?filmLabel  WHERE {
  ?film wdt:P31 wd:Q11424;
  SERVICE wikibase:label {
     bd:serviceParam wikibase:language "en" .
  }
}
```


All movies with roles
```
SELECT ?film  ?role  ?person  WHERE {
  ?film wdt:P31 wd:Q11424;
    wdt:P57|wdt:P58|wdt:P86|wdt:P161|wdt:P162|wdt:P170|wdt:P175|wdt:P344|wdt:P725|wdt:P1040|wdt:P1431|wdt:P2515|wdt:p2554|wdt:P14318  ?person.
  ?film ?role ?person
}
```


Roles in Movies
```
SELECT ?role ?realroleLabel WHERE {
  VALUES ?role { wdt:P57 wdt:P58 wdt:P86 wdt:P161 wdt:P162 wdt:P170 wdt:P175 wdt:P344 wdt:P725 wdt:P1040 wdt:P1431 wdt:P2515 wdt:p2554 wdt:P14318 }  .
   ?realrole wikibase:directClaim ?role
  SERVICE wikibase:label {
     bd:serviceParam wikibase:language "en" .
  }
 }


```

### VIDEO SHOW

Video shows with name
```
SELECT ?videoShow  ?videoShowLabel WHERE {
  ?videoShow wdt:P31 wd:Q5398426;
  SERVICE wikibase:label {
     bd:serviceParam wikibase:language "en" .
  }
}
```


Roles in VideoShow
```
SELECT ?videoShow  ?role  ?person  WHERE {
   ?videoShow wdt:P31 wd:Q5398426;
    wdt:P57|wdt:P58|wdt:P86|wdt:P161|wdt:P162|wdt:P170|wdt:P175|wdt:P344|wdt:P725|wdt:P1040|wdt:P1431|wdt:P2515|wdt:p2554|wdt:P14318  ?person.
  ?videoShow ?role ?person
 }
```


### ANIMATED MOVIES

Animated movies with name
```
SELECT ?animatedMovie  ?animatedMovieLabel WHERE {
  ?animatedMovie wdt:P31 wd:Q202866;
  SERVICE wikibase:label {
     bd:serviceParam wikibase:language "en" .
  }
}
```


Roles in Animated Movies
```
SELECT ?animatedMovie  ?role  ?person  WHERE {
   ?animatedMovie wdt:P31 wd:Q5398426;
  
    wdt:P57|wdt:P58|wdt:P86|wdt:P161|wdt:P162|wdt:P170|wdt:P175|wdt:P344|wdt:P725|wdt:P1040|wdt:P1431|wdt:P2515|wdt:p2554|wdt:P14318  ?person.
  ?animatedMovie  ?role ?person
  
}  
```

### SONGS

Songs with Name
```
SELECT ?song  ?songLabel WHERE {
  ?song wdt:P31/wdt:P279* wd:Q2188189;
  SERVICE wikibase:label {
     bd:serviceParam wikibase:language "en" .
  }
}
```


Roles in songs

```
SELECT ?person  ?role  ?song  WHERE {
 
  ?person wdt:P50|wdt:P86|wdt:P87|wdt:P170|wdt:P175|wdt:p676 ?song;
          wdt:P31/wdt:P279* wd:Q2188189.
  ?person ?role ?song.
  
}

```


### VIDEO_GAMES

Video games with Name
```
SELECT ?videogame ?videogameLabel WHERE {
  ?song wdt:P31/wdt:P279* wd:Q7889;
  SERVICE wikibase:label {
     bd:serviceParam wikibase:language "en" .
  }
}
```


Roles in video games

```
SELECT ?person ?role ?videogame WHERE {
  ?person wdt:P50|wdt:P86|wdt:P87|wdt:P162|wdt:P170|wdt:P175|wdt:P287|wdt:p676|wdt:P943 ?videogame;
          wdt:P31/wdt:P279* wd:Q7889.
  ?person ?role ?videogame.
  
}
```

### BOOKS

Books with Name
```
SELECT ?book ?bookLabel WHERE {
  ?song wdt:P31/wdt:P279* wd:Q571;
  SERVICE wikibase:label {
     bd:serviceParam wikibase:language "en" .
  }
}
```


Roles in books

```
SELECT ?person ?role ?book WHERE {
  ?person wdt:P50|wdt:P98|wdt:P110|wdt:P170|wdt:P674 ?book;
          wdt:P31/wdt:P279* wd:Q571.
  ?person ?role ?book.
}
```

# SET UP DATABASE

```
CREATE DATABASE wikidata;
create user wikidata with encrypted password 'wikidata';
grant all privileges on database wikidata to wikidata;

\connect wikidata;
\i create_table.sql;
```