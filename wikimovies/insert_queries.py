

insert_occupation =  """
INSERT INTO public.occupations (
	occupation_id,
	occupation_name
) VALUES (%s, %s) ON CONFLICT (occupation_id) DO NOTHING;
"""

insert_occupation_columns = ["occupation", "occupationLabel"]
map_occupation_columns = {"occupation": "occupation_id", "occupationLabel": "occupation_name"}


insert_role =  """
INSERT INTO public.roles (
	role_id,
	role_name
) VALUES (%s, %s) ON CONFLICT (role_id) DO NOTHING;
"""

insert_role_columns = ["role", "realroleLabel"]
map_role_columns = {"role": "role_id", "realroleLabel": "role_name" }

insert_human = """
INSERT INTO public.humans (
	human_id,
	human_name
) VALUES (%s, %s) ON CONFLICT (human_id) DO NOTHING;
"""

insert_human_columns = ["human", "humanLabel"]
map_human_columns = {"human": "human_id", "humanLabel": "human_name"}

insert_movie = """
INSERT INTO public.movies (
	movie_id,
	movie_name
) VALUES (%s, %s) ON CONFLICT (movie_id) DO NOTHING;
"""

insert_movie_columns = ["film", "filmLabel"]
map_movie_columns = {"film": "movie_id", "filmLabel": "movie_name"}


insert_tvshow = """
INSERT INTO public.tvshows (
	tvshow_id,
	tvshow_name
) VALUES (%s, %s) ON CONFLICT (tvshow_id) DO NOTHING;
"""

insert_tvshow_columns = ["tvShow", "tvShowLabel"]
map_tvshow_columns = {"tvShow": "tvshow_id", "tvShowLabel": "tvshow_name"}

insert_animatedmovie = """
INSERT INTO public.animatedmovies (
	animatedmovie_id,
	animatedmovie_name
) VALUES (%s, %s) ON CONFLICT (animatedmovie_id) DO NOTHING;
"""

insert_animatedmovie_columns = ["animatedMovie", "animatedMovieLabel"]
map_animatedmovie_columns = {"animatedMovie": "animatedmovie_id", "animatedMovieLabel": "animatedmovie_name"}


insert_song = """
INSERT INTO public.songs (
	song_id,
	song_name
) VALUES (%s, %s) ON CONFLICT (song_id) DO NOTHING;
"""

insert_song_columns = ["song", "songLabel"]
map_song_columns = {"song": "song_id", "songLabel": "song_name"}

insert_videogame = """
INSERT INTO public.videogames (
	videogame_id,
	videogame_name
) VALUES (%s, %s) ON CONFLICT (videogame_id) DO NOTHING;
"""

insert_videogame_columns = ["videogame", "videogameLabel"]
map_videogame_columns = {"videogame": "videogame_id", "videogameLabel": "videogame_name"}

insert_book = """
INSERT INTO public.books (
	book_id,
	book_name
) VALUES (%s, %s) ON CONFLICT (book_id) DO NOTHING;
"""

insert_book_columns = ["book", "bookLabel"]
map_book_columns = {"book": "book_id", "bookLabel": "book_name"}