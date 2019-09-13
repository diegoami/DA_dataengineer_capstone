

occupations_sparkql = """
SELECT ?occupation ?occupationLabel WHERE {
  ?occupation wdt:P31/wdt:P279* wd:Q12737077 .

  SERVICE wikibase:label {
     bd:serviceParam wikibase:language "en" .
  }
}
"""


humans_byyear_sparkql = """
SELECT ?human ?humanLabel ?occupation ?linkcount WHERE {
  ?human wdt:P31 wd:Q5;
     wdt:P569 ?born .

  FILTER (?born >={year}-01-01"^^xsd:dateTime && ?born < "{year+1}-01-01"^^xsd:dateTime) .
  FILTER (?occupation not in  ( wd:Q937857, wd:Q1650915, wd:Q3665646, wd:Q11774891, wd:Q11513337, wd:Q2309784, wd:Q2066131, wd:Q19204627, wd:Q14089670, wd:Q12299841, wd:Q10871364, wd:Q15117302, wd:Q13141064, wd:Q13365117,  wd:Q10873124) ) . 
   ?human wikibase:sitelinks ?linkcount .
  OPTIONAL { ?human wdt:P106 ?occupation } 
  SERVICE wikibase:label {
     bd:serviceParam wikibase:language "en" .
  }
  
}
"""

participants_sparkql = """
    SELECT ?participant ?participantLabel WHERE {
      ?occupation wdt:P31/wdt:P279* wd:Q12737077 .
    
      SERVICE wikibase:label {
         bd:serviceParam wikibase:language "en" .
      }
    }
"""

roles_sparkql = """
    SELECT ?role ?realroleLabel WHERE {
      VALUES ?role { wdt:P50 wdt:P57 wdt:P58 wdt:P86 wdt:P98 wdt:P110 wdt:P161 wdt:P162 wdt:P170 wdt:P175 wdt:P344 wdt:P674 wdt:676 wdt:P725 wdt:P1040 wdt:P1431 wdt:P2515 wdt:p2554 wdt:P14318 }  .
       ?realrole wikibase:directClaim ?role
      SERVICE wikibase:label {
         bd:serviceParam wikibase:language "en" .
      }
     }
"""

movies_sparkql = """
    SELECT ?film  ?filmLabel  WHERE {
      ?film wdt:P31 wd:Q11424;
      SERVICE wikibase:label {
         bd:serviceParam wikibase:language "en" .
      }
    }

"""

movies_with_roles_sparkql = """
    SELECT ?film  ?role  ?person  WHERE {
      ?film wdt:P31 wd:Q11424;
        wdt:P57|wdt:P58|wdt:P86|wdt:P161|wdt:P162|wdt:P170|wdt:P175|wdt:P344|wdt:P725|wdt:P1040|wdt:P1431|wdt:P2515|wdt:p2554|wdt:P14318 ?person.
      ?film ?role ?person
}
"""


tvshows_sparkql = """
    SELECT ?tvShow  ?tvShowLabel WHERE {
      ?tvShow wdt:P31 wd:Q5398426;
      SERVICE wikibase:label {
         bd:serviceParam wikibase:language "en" .
      }
}
"""

tvshows_with_roles_sparkql = """
SELECT ?tvShow  ?role  ?person  WHERE {
   ?tvShow wdt:P31 wd:Q5398426;
    wdt:P57|wdt:P58|wdt:P86|wdt:P161|wdt:P162|wdt:P170|wdt:P175|wdt:P344|wdt:P725|wdt:P1040|wdt:P1431|wdt:P2515|wdt:p2554|wdt:P14318  ?person.
  ?tvShow ?role ?person
 }
"""


animatedmovies_sparkql = """
SELECT ?animatedMovie  ?animatedMovieLabel WHERE {
  ?animatedMovie wdt:P31 wd:Q202866;
  SERVICE wikibase:label {
     bd:serviceParam wikibase:language "en" .
  }
}
"""

animatedmovies_with_roles_sparkql = """
SELECT ?animatedMovie  ?role  ?person  WHERE {
   ?animatedMovie wdt:P31 wd:Q5398426;
  
    wdt:P57|wdt:P58|wdt:P86|wdt:P161|wdt:P162|wdt:P170|wdt:P175|wdt:P344|wdt:P725|wdt:P1040|wdt:P1431|wdt:P2515|wdt:p2554|wdt:P14318  ?person.
  ?animatedMovie  ?role ?person
  
}  
"""

songs_sparkql = """
SELECT ?song  ?songLabel WHERE {
  ?song wdt:P31/wdt:P279* wd:Q2188189;
  SERVICE wikibase:label {
     bd:serviceParam wikibase:language "en" .
  }
}
"""

songs_with_roles_sparkql = """
SELECT ?person  ?role  ?song WHERE {
  ?person wdt:P50|wdt:P86|wdt:P87|wdt:P170|wdt:P175|wdt:p676 ?song;
          wdt:P31/wdt:P279* wd:Q2188189.
  ?person ?role ?song.
}
"""

videogames_sparkql = """
SELECT ?videogame ?videogameLabel WHERE {
  ?song wdt:P31/wdt:P279* wd:Q7889;
  SERVICE wikibase:label {
     bd:serviceParam wikibase:language "en" .
  }
}
"""

videogames_with_roles_sparkql = """
SELECT ?person ?role ?videogame WHERE {
  ?person wdt:P50|wdt:P86|wdt:P87|wdt:P162|wdt:P170|wdt:P175|wdt:P287|wdt:p676|wdt:P943 ?videogame;
          wdt:P31/wdt:P279* wd:Q7889.
  ?person ?role ?videogame.
  
}
"""

books_sparkql = """
SELECT ?videogame ?videogameLabel WHERE {
  ?song wdt:P31/wdt:P279* wd:Q7889;
  SERVICE wikibase:label {
     bd:serviceParam wikibase:language "en" .
  }
}
"""

books_with_roles_sparkql = """
SELECT ?person ?role ?videogame WHERE {
  ?person wdt:P50|wdt:P86|wdt:P87|wdt:P162|wdt:P170|wdt:P175|wdt:P287|wdt:p676|wdt:P943 ?videogame;
          wdt:P31/wdt:P279* wd:Q7889.
  ?person ?role ?videogame.

}
"""

