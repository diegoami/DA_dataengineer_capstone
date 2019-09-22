

# query to insert all creative works in the DWH table
INSERT_CREATIVE_WORKS_SQL_QUERY = """
INSERT INTO public.creative_works (
	creative_work_id,
	creative_work_name,
	creative_work_type
)
SELECT DISTINCT movie_id as id, movie_name as name, 'MOVIE' AS work_type FROM movies
UNION
SELECT DISTINCT tvshow_id as id, tvshow_name, 'TVSHOW' AS work_type    FROM tvshows
UNION
SELECT DISTINCT animatedmovie_id as id, animatedmovie_name as name, 'ANIMATEDMOVIE' AS work_type FROM animatedmovies
UNION
SELECT DISTINCT videogame_id as id, videogame_name as name, 'VIDEOGAME' AS work_type  FROM videogames
UNION
SELECT DISTINCT song_id as id, song_name as name, 'SONG' AS work_type  FROM songs
UNION
SELECT DISTINCT book_id as id, book_name as name, 'BOOK' AS work_type  FROM books
ON CONFLICT (creative_work_id) DO NOTHING;
"""

# query to insert all participations in creative works in the DWH table
INSERT_PARTICIPATIONS_SQL_QUERY = """
INSERT INTO public.participations (
	creative_work_id,
	human_id,
	role_name
)
SELECT DISTINCT movie_id, human_id, role_name FROM movie_roles M, roles R WHERE M.role_id = R.role_id
UNION
SELECT DISTINCT tvshow_id, human_id, role_name FROM tvshow_roles T, roles R WHERE T.role_id = R.role_id
UNION
SELECT DISTINCT animatedmovie_id, human_id, role_name FROM animatedmovie_roles A, roles R WHERE A.role_id = R.role_id
UNION
SELECT DISTINCT videogame_id, human_id, role_name FROM videogame_roles V, roles R WHERE V.role_id = R.role_id
UNION
SELECT DISTINCT song_id, human_id, role_name FROM song_roles S, roles R WHERE S.role_id = R.role_id
UNION
SELECT DISTINCT book_id, human_id, role_name FROM book_roles B, roles R WHERE B.role_id = R.role_id
ON CONFLICT (creative_work_id, human_id, role_name) DO NOTHING
;
"""