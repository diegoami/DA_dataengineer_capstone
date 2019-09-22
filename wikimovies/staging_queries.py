from collections import OrderedDict

# Sql Query to insert a role
INSERT_ROLE_SQL_QUERY = """
INSERT INTO public.roles (
	role_id,
	role_name
) VALUES (%s, %s) ON CONFLICT (role_id) DO UPDATE
SET role_name = EXCLUDED.role_name;
"""

# maps between columns in Sparql and columns in insert role SQL query
INSERT_ROLE_MAP_COLUMNS = OrderedDict({"role": "role_id", "realroleLabel": "role_name"})

# Sql Query to insert a person
INSERT_HUMAN_SQL_QUERY = """
INSERT INTO public.humans (
	human_id,
	human_name
) VALUES (%s, %s) ON CONFLICT (human_id) DO UPDATE
SET human_name = EXCLUDED.human_name;
"""

# maps between columns in Sparql and columns in insert human SQL query
INSERT_HUMAN_MAP_COLUMNS = OrderedDict({"human": "human_id", "humanLabel": "human_name"})

# Sql Query to insert a movie
INSERT_MOVIE_SQL_QUERY = """
INSERT INTO public.movies (
	movie_id,
	movie_name
) VALUES (%s, %s) ON CONFLICT (movie_id) DO UPDATE
SET movie_name = EXCLUDED.movie_name;
"""

# maps between columns in Sparql and columns in insert movie SQL query
INSERT_MOVIE_MAP_COLUMNS = OrderedDict({"film": "movie_id", "filmLabel": "movie_name"})

# Sql Query to insert a tv show
INSERT_TVSHOW_SQL_QUERY = """
INSERT INTO public.tvshows (
	tvshow_id,
	tvshow_name
) VALUES (%s, %s) ON CONFLICT (tvshow_id) DO UPDATE
SET tvshow_name = EXCLUDED.tvshow_name;
"""

# maps between columns in Sparql and columns in insert tv show SQL query
INSERT_TVSHOW_MAP_COLUMNS = OrderedDict({"tvShow": "tvshow_id", "tvShowLabel": "tvshow_name"})


# Sql Query to insert an animated movie
INSERT_ANIMATEDMOVIE_SQL_QUERY = """
INSERT INTO public.animatedmovies (
	animatedmovie_id,
	animatedmovie_name
) VALUES (%s, %s) ON CONFLICT (animatedmovie_id) DO UPDATE
SET animatedmovie_name = EXCLUDED.animatedmovie_name;
"""

# maps between columns in Sparql and columns in insert animated movie SQL query
INSERT_ANIMATEDMOVIE_MAP_COLUMNS = OrderedDict({"animatedMovie": "animatedmovie_id", "animatedMovieLabel": "animatedmovie_name"})

# Sql Query to insert a song
INSERT_SONG_SQL_QUERY = """
INSERT INTO public.songs (
	song_id,
	song_name
) VALUES (%s, %s) ON CONFLICT (song_id) DO UPDATE
SET song_name = EXCLUDED.song_name;
"""

# maps between columns in Sparql and columns in insert song SQL query
INSERT_SONG_MAP_COLUMNS = OrderedDict({"song": "song_id", "songLabel": "song_name"})

# Sql Query to insert a video game
INSERT_VIDEOGAME_SQL_QUERY = """
INSERT INTO public.videogames (
	videogame_id,
	videogame_name
) VALUES (%s, %s) ON CONFLICT(videogame_id) DO UPDATE
SET videogame_name = EXCLUDED.videogame_name;
"""

# maps between columns in Sparql and columns in insert video game SQL query
INSERT_VIDEOGAME_MAP_COLUMNS = OrderedDict({"videogame": "videogame_id", "videogameLabel": "videogame_name"})

# Sql Query to insert a book
INSERT_BOOK_SQL_QUERY = """
INSERT INTO public.books (
	book_id,
	book_name
) VALUES (%s, %s) ON CONFLICT (book_id) DO UPDATE
SET book_name = EXCLUDED.book_name;
"""

# maps between columns in Sparql and columns in insert book SQL query
INSERT_BOOK_MAP_COLUMNS = OrderedDict({"book": "book_id", "bookLabel": "book_name"})

# Sql Query to insert a movie role of some human
INSERT_MOVIE_ROLE_SQL_QUERY = """
INSERT INTO public.movie_roles (
	movie_id,
	role_id,
	human_id
) VALUES (%s, %s, %s) ON CONFLICT (movie_id, role_id, human_id) DO NOTHING;
"""

# maps between columns in Sparql and columns in insert movie role SQL query
INSERT_MOVIE_ROLE_MAP_COLUMNS = OrderedDict({"film": "movie_id", "role": "role_id", "person": "human_id"})

# Sql Query to insert a tv role of some human
INSERT_TVSHOW_ROLE_SQL_QUERY = """
INSERT INTO public.tvshow_roles (
	tvshow_id,
	role_id,
	human_id
) VALUES (%s, %s, %s) ON CONFLICT (tvshow_id, role_id, human_id) DO NOTHING;
"""

# maps between columns in Sparql and columns in insert tvshow role SQL query
INSERT_TVSHOW_ROLE_MAP_COLUMNS = OrderedDict({"tvShow": "tvshow_id", "role": "role_id", "person": "human_id"})

# Sql Query to insert an animated movie role of some human
INSERT_ANIMATEDMOVIE_ROLE_SQL_QUERY = """
INSERT INTO public.animatedmovie_roles (
	animatedmovie_id,
	role_id,
	human_id
) VALUES (%s, %s, %s) ON CONFLICT (animatedmovie_id, role_id, human_id) DO NOTHING;
"""

# maps between columns in Sparql and columns in insert animated movie role SQL query
INSERT_ANIMATEDMOVIE_ROLE_MAP_COLUMNS = OrderedDict({"animatedMovie": "animatedmovie_id", "role": "role_id", "person": "human_id"})

# Sql Query to insert a role in a song of some human
INSERT_SONG_ROLE_SQL_QUERY = """
INSERT INTO public.song_roles (
	song_id,
	role_id,
	human_id
) VALUES (%s, %s, %s) ON CONFLICT (song_id, role_id, human_id) DO NOTHING;
"""

# maps between columns in Sparql and columns in insert song role SQL query
INSERT_SONG_ROLE_MAP_COLUMNS = OrderedDict({"song": "song_id", "role": "role_id", "person": "human_id"})

# Sql Query to insert a role in a videogame of some human
INSERT_VIDEOGAME_ROLE_SQL_QUERY = """
INSERT INTO public.videogame_roles (
	videogame_id,
	role_id,
	human_id
) VALUES (%s, %s, %s) ON CONFLICT (videogame_id, role_id, human_id) DO NOTHING;
"""

# maps between columns in Sparql and columns in insert video game role SQL query
INSERT_VIDEOGAME_ROLE_MAP_COLUMNS = OrderedDict({"videogame": "videogame_id", "role": "role_id", "person": "human_id"})

# Sql Query to insert a role in a book of some human
INSERT_BOOK_ROLE_SQL_QUERY = """
INSERT INTO public.book_roles (
	book_id,
	role_id,
	human_id
) VALUES (%s, %s, %s) ON CONFLICT (book_id, role_id, human_id) DO NOTHING;
"""

# maps between columns in Sparql and columns in insert book role SQL query
INSERT_BOOk_ROLE_SQL_QUERY = OrderedDict({"book": "book_id", "role": "role_id", "person": "human_id"})
