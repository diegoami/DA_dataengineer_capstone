

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


insert_movie_role = """
INSERT INTO public.movie_roles (
	movie_id,
	role_id,
	human_id
) VALUES (%s, %s, %S) ON CONFLICT (movie_id, role_id, human_id) DO NOTHING;
"""

insert_movie_role_columns = ["film", "role", "person"]
map_movie_role_columns = {"film": "movie_id", "role": "role_id", "person": "human_id"}


insert_tvshow_role = """
INSERT INTO public.movie_roles (
	tvshow_id,
	role_id,
	human_id
) VALUES (%s, %s, %S) ON CONFLICT (tvshow_id, role_id, human_id) DO NOTHING;
"""

insert_tvshow_role_columns = ["tvshow", "role", "person"]
map_tvshow_role_columns = {"tvshow": "tvshow_id", "role": "role_id", "person": "human_id"}


insert_animatedmovie_role = """
INSERT INTO public.animatedmovie_roles (
	animatedmovie_id,
	role_id,
	human_id
) VALUES (%s, %s, %S) ON CONFLICT (animatedmovie_id, role_id, human_id) DO NOTHING;
"""

insert_animatedmovie_role_columns = ["animatedmovie", "role", "person"]
map_animatedmovie_role_columns = {"animatedmovie": "animatedmovie_id", "role": "role_id", "person": "human_id"}


insert_song_role = """
INSERT INTO public.song_roles (
	song_id,
	role_id,
	human_id
) VALUES (%s, %s, %S) ON CONFLICT (song_id, role_id, human_id) DO NOTHING;
"""

insert_song_role_columns = ["song", "role", "person"]
map_song_role_columns = {"song": "song_id", "role": "role_id", "person": "human_id"}

insert_videogame_role = """
INSERT INTO public.videogame_roles (
	videogame_id,
	role_id,
	human_id
) VALUES (%s, %s, %S) ON CONFLICT (videogame_id, role_id, human_id) DO NOTHING;
"""

insert_videogame_role_columns = ["videogame", "role", "person"]
map_videogame_role_columns = {"videogame": "videogame_id", "role": "role_id", "person": "human_id"}


insert_book_role = """
INSERT INTO public.book_roles (
	book_id,
	role_id,
	human_id
) VALUES (%s, %s, %S) ON CONFLICT (book_id, role_id, human_id) DO NOTHING;
"""

insert_book_role_columns = ["book", "role", "person"]
map_book_role_columns = {"book": "book_id", "role": "role_id", "person": "human_id"}