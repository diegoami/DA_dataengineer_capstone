

# query to insert all creative works in the DWH table
INSERT_CREATIVE_WORKS_SQL_QUERY = """
INSERT INTO public.creative_works (
	creative_work_id,
	creative_work_name,
	creative_work_type
)
SELECT DISTINCT movie_id, movie_name, 'MOVIE' AS creative_work_type FROM movies
UNION
SELECT DISTINCT tvshow_id, tvshow_name, 'TVSHOW' AS creative_work_type   FROM tvshows
UNION
SELECT DISTINCT animatedmovie_id, animatedmovie_name, 'ANIMATEDMOVIE' AS creative_work_type FROM animatedmovies
UNION
SELECT DISTINCT videogame_id, videogame_name, 'VIDEOGAME' AS creative_work_type FROM videogames
UNION
SELECT DISTINCT song_id, song_name, 'SONG' AS creative_work_type FROM songs
UNION
SELECT DISTINCT book_id, book_name, 'BOOK' AS creative_work_type FROM books
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