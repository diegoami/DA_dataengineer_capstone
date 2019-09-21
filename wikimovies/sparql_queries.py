
# Sparql query to retrieve humans born in a given year from wikidata and having specific occupations, and their name in English
HUMANS_BY_YEAR_SPARQL_QUERY = """
    SELECT DISTINCT ?human ?humanLabel WHERE {{
      ?human wdt:P31 wd:Q5;
         wdt:P569 ?born .
      FILTER (?born >="{}-01-01"^^xsd:dateTime && ?born < "{}-01-01"^^xsd:dateTime) .
      FILTER (?occupation in  (
                wd:Q33999,
                wd:Q36180,
                wd:Q1930187,
                wd:Q177220,
                wd:Q2526255,
                wd:Q28389,
                wd:Q36834,
                wd:Q10800557,
                wd:Q639669,
                wd:Q43845,
                wd:Q1749879,
                wd:Q201788, 
                wd:Q49757,
                wd:Q3282637,
                wd:Q10798782,
                wd:Q188094,
                wd:Q33231,
                wd:Q81096,
                wd:Q483501,
                wd:Q855091,
                wd:Q482980,
                 wd:Q333634,
                 wd:Q6625963,
                 wd:Q488205,
                 wd:Q901,
                 wd:Q947873,
                 wd:Q753110,
                 wd:Q2259451,
                 wd:Q4964182,
                 wd:Q2306091,
                  wd:Q2722764,
                  wd:Q183945,
                  wd:Q131524,
                   wd:Q11481802,
                    wd:Q158852,
                    wd:Q3387717,
                    wd:Q2405480,
                    wd:Q4853732,
                    wd:Q715301,
                    wd:Q4610556,
                    wd:Q214917,
                    wd:Q7042855,
                    wd:Q644687,
                    wd:Q578109,
                    wd:Q4263842,
                    wd:Q2490358,
                    wd:Q128124,
                    wd:Q2516866,
                    wd:Q970153,
                    wd:Q3455803,
                    wd:Q245068,
                    wd:Q15980158,
                     wd:Q214917,
                     wd:Q5716684,
                     wd:Q822146,
                      wd:Q1114448
                
            ) 
      ) . 
      ?human wdt:P106 ?occupation 
      SERVICE wikibase:label {{
         bd:serviceParam wikibase:language "en" .
      }}
      
    }}
"""

# Sparql query to retrieve roles from wikidata in creative works, that we are interested id
ROLES_SPARQL_QUERY = """
    SELECT ?role ?realroleLabel WHERE {
      VALUES ?role { wdt:P50 wdt:P57 wdt:P58 wdt:P86 wdt:P98 wdt:P110 wdt:P161 wdt:P162 wdt:P170 wdt:P175 wdt:P344 wdt:P674 wdt:676 wdt:P725 wdt:P1040 wdt:P1431 wdt:P2515 wdt:p2554 wdt:P14318 }  .
       ?realrole wikibase:directClaim ?role
      SERVICE wikibase:label {
         bd:serviceParam wikibase:language "en" .
      }
     }
"""

# Sparql query to retrieve movies from wikidata and their name in English
MOVIES_BY_YEAR_SPARQL_QUERY = """
    SELECT DISTINCT ?film  ?filmLabel  WHERE {{
      ?film wdt:P31 wd:Q11424;
            wdt:P577 ?publicationDate .
      FILTER (?publicationDate >="{}-01-01"^^xsd:dateTime && ?publicationDate < "{}-01-01"^^xsd:dateTime) .
      SERVICE wikibase:label {{
         bd:serviceParam wikibase:language "en" .
      }}
    }}

"""

# Sparql query to retrieve the relation between movies and people who participated in them in any role
MOVIE_ROLES_BY_YEAR_SPARQL_QUERY = """
    SELECT ?film  ?role  ?person  WHERE {{
      ?film wdt:P31 wd:Q11424;
        
        wdt:P57|wdt:P58|wdt:P86|wdt:P161|wdt:P162|wdt:P170|wdt:P175|wdt:P344|wdt:P725|wdt:P1040|wdt:P1431|wdt:P2515|wdt:p2554|wdt:P14318 ?person;
      wdt:P577 ?publicationDate .
      FILTER (?publicationDate >="{}-01-01"^^xsd:dateTime && ?publicationDate < "{}-01-01"^^xsd:dateTime) .
      ?film ?role ?person
}}
"""

# Sparql query to retrieve tv shows from wikidata and their name in English
TVSHOWS_BY_YEAR_SPARQL_QUERY = """
    SELECT ?tvShow  ?tvShowLabel WHERE {{
      ?tvShow wdt:P31 wd:Q5398426;
          wdt:P577 ?publicationDate .
          FILTER (?publicationDate >="{}-01-01"^^xsd:dateTime && ?publicationDate < "{}-01-01"^^xsd:dateTime) .
      SERVICE wikibase:label {{
         bd:serviceParam wikibase:language "en" .
      }}
}}
"""

# Sparql query to retrieve the relation between tv shows and people who participated in them in any role
TVSHOW_ROLES_BY_YEAR_SPARQL_QUERY = """
SELECT ?tvShow  ?role  ?person  WHERE {{
   ?tvShow wdt:P31 wd:Q5398426;
    wdt:P57|wdt:P58|wdt:P86|wdt:P161|wdt:P162|wdt:P170|wdt:P175|wdt:P344|wdt:P725|wdt:P1040|wdt:P1431|wdt:P2515|wdt:p2554|wdt:P14318  ?person ;
    wdt:P577 ?publicationDate .
    FILTER (?publicationDate >="{}-01-01"^^xsd:dateTime && ?publicationDate < "{}-01-01"^^xsd:dateTime) .
  ?tvShow ?role ?person
 }}
"""

# Sparql query to retrieve animated movies from wikidata and their name in English
ANIMATEDMOVIES_BY_YEAR_SPARQL_QUERY = """
SELECT ?animatedMovie  ?animatedMovieLabel WHERE {{
  ?animatedMovie wdt:P31/wdt:P279* wd:Q202866;
        wdt:P577 ?publicationDate .
  FILTER (?publicationDate >="{}-01-01"^^xsd:dateTime && ?publicationDate < "{}-01-01"^^xsd:dateTime) .      
  SERVICE wikibase:label {{
     bd:serviceParam wikibase:language "en" .
  }}
}}
"""

# Sparql query to retrieve the relation between animated movies and people who participated in them in any role
ANIMATEDMOVIE_ROLES_BY_YEAR_SPARQL_QUERY = """
SELECT ?animatedMovie  ?role  ?person  WHERE {{
   ?animatedMovie wdt:P31/wdt:P279* wd:Q202866;
  
    wdt:P57|wdt:P58|wdt:P86|wdt:P161|wdt:P162|wdt:P170|wdt:P175|wdt:P344|wdt:P725|wdt:P1040|wdt:P1431|wdt:P2515|wdt:p2554|wdt:P14318  ?person ;
    wdt:P577 ?publicationDate .
    FILTER (?publicationDate >="{}-01-01"^^xsd:dateTime && ?publicationDate < "{}-01-01"^^xsd:dateTime) .
  ?animatedMovie  ?role ?person
  
}}  
"""

# Sparql query to retrieve songs from wikidata and their name in English
SONGS_BY_YEAR_SPARQL_QUERY = """
SELECT ?song ?songLabel  WHERE {{
  {{?song wdt:P31 wd:Q7366; wdt:P577 ?publicationDate.   FILTER (?publicationDate >="{}-01-01"^^xsd:dateTime && ?publicationDate < "{}-01-01"^^xsd:dateTime) .  }}
  
  UNION
  {{?song wdt:P31 wd:Q134556; wdt:P577 ?publicationDate.   FILTER (?publicationDate >="{}-01-01"^^xsd:dateTime && ?publicationDate < "{}-01-01"^^xsd:dateTime) .  }}

  SERVICE wikibase:label {{
     bd:serviceParam wikibase:language "en" .
  }}
}}
"""

# Sparql query to retrieve the relation between songs and people who participated in them in any role
SONG_ROLES_BY_YEAR_SPARQL_QUERY = """
SELECT ?song   ?role  ?person WHERE {{
  {{?song wdt:P50|wdt:P86|wdt:P87|wdt:P170|wdt:P175|wdt:p676 ?person;
          wdt:P31 wd:Q7366; wdt:P577 ?publicationDate.   FILTER (?publicationDate >="{}-01-01"^^xsd:dateTime && ?publicationDate < "{}-01-01"^^xsd:dateTime) .  }}
   UNION
     {{?song wdt:P50|wdt:P86|wdt:P87|wdt:P170|wdt:P175|wdt:p676 ?person;
          wdt:P31 wd:Q134556; wdt:P577 ?publicationDate.   FILTER (?publicationDate >="{}-01-01"^^xsd:dateTime && ?publicationDate < "{}-01-01"^^xsd:dateTime) .  }}.             
  ?song ?role ?person.
}}
"""

# Sparql query to retrieve video games from wikidata and their name in English
VIDEOGAMES_SPARQL_QUERY = """
SELECT ?videogame ?videogameLabel WHERE {
  ?videogame wdt:P31/wdt:P279* wd:Q7889;
  SERVICE wikibase:label {
     bd:serviceParam wikibase:language "en" .
  }
}
"""

# Sparql query to retrieve the relation between videogames and people who participated in them in any role
VIDEOGAME_ROLES_SPARQL_QUERY = """
SELECT ?videogame ?role  ?person WHERE {
  ?videogame wdt:P31/wdt:P279* wd:Q7889.
  { ?videogame wdt:P674 ?character.
    ?character wdt:P725 ?person.
    ?character ?role ?person.
   }
  UNION 
  { ?videogame wdt:P725 ?person.
    ?videogame ?role ?person.
   }
}
"""

# Sparql query to retrieve books from wikidata and their name in English
BOOKS_SPARQL_QUERY = """
SELECT DISTINCT ?book ?bookLabel WHERE {
  {?book wdt:P31/wdt:P279* wd:Q571}
  UNION
  {?book wdt:P31/wdt:P279* wd:Q8261}
  SERVICE wikibase:label {
     bd:serviceParam wikibase:language "en" .
  }
}
"""

# Sparql query to retrieve the relation between videogames and people who participated in them in any role
BOOK_ROLES_SPARQL_QUERY = """
SELECT ?book ?role  ?person WHERE {
  {?book wdt:P50|wdt:P86|wdt:P87|wdt:P162|wdt:P170|wdt:P175|wdt:P287|wdt:p676|wdt:P943 ?person;
          wdt:P31/wdt:P279* wd:Q571}
  UNION
  {?book wdt:P50|wdt:P86|wdt:P87|wdt:P162|wdt:P170|wdt:P175|wdt:P287|wdt:p676|wdt:P943 ?person;
          wdt:P31/wdt:P279* wd:Q8261}.
  ?book ?role ?person.

}
"""

# Utility query to retrieve occupations in Wikidata
FIND_RELEVANT_OCCUPATIONS = """
SELECT (COUNT(?human) AS ?humanC) ?occupation ?occupationLabel WHERE {
  ?human wdt:P31 wd:Q5;
     wdt:P569 ?born .
  
 FILTER (?born >="2013-01-01"^^xsd:dateTime && ?born < "2014-01-01"^^xsd:dateTime) .
 OPTIONAL { ?human wdt:P106 ?occupation } 
  
 SERVICE wikibase:label {
     bd:serviceParam wikibase:language "en" .
  } 
  
}
GROUP BY ?occupation ?occupationLabel
ORDER BY DESC (?humanC) 
"""
