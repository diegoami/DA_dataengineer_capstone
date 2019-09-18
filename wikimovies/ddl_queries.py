

# su - postgres
# createuser --interactive wikidata
# Shall the new role be a superuser? (y/n) y

# ALTER USER wikidata WITH PASSWORD 'wikidata';
# CREATE DATABASE wikidata;
# COMMIT
# FLUSH PRIVILEGES

humans_drop = "DROP TABLE IF EXISTS humans;"
staging_roles_drop = "DROP TABLE IF EXISTS roles;"

staging_movies_drop = "DROP TABLE IF EXISTS movies;"
staging_tvshows_drop = "DROP TABLE IF EXISTS tvshows;"
staging_animatedmovies_drop = "DROP TABLE IF EXISTS animatedmovies;"
staging_songs_drop = "DROP TABLE IF EXISTS songs;"
staging_videogames_drop = "DROP TABLE IF EXISTS videogames;"
staging_books_drop = "DROP TABLE IF EXISTS books;"

staging_movie_roles_drop = "DROP TABLE IF EXISTS movie_roles;"
staging_tvshow_roles_drop = "DROP TABLE IF EXISTS tvshow_roles;"
staging_animatedmovie_roles_drop = "DROP TABLE IF EXISTS animatedmovie_roles;"
staging_song_roles_drop = "DROP TABLE IF EXISTS song_roles;"
staging_videogame_roles_drop = "DROP TABLE IF EXISTS videogame_roles;"
staging_book_roles_drop = "DROP TABLE IF EXISTS book_roles;"

creative_works_drop = "DROP TABLE IF EXISTS creative_works;"
creative_works_participations = "DROP TABLE IF EXISTS participations;"




humans_create = """
CREATE TABLE IF NOT EXISTS  public.humans (
	human_id varchar(256) PRIMARY KEY,
	human_name varchar(256) NOT NULL
);
"""

staging_roles_create = """
CREATE TABLE  public.roles (
	role_id varchar(256) PRIMARY KEY,
	role_name varchar(256) NOT NULL
);
"""

staging_movies_create = """
CREATE TABLE IF NOT EXISTS  public.movies (
	movie_id varchar(256) PRIMARY KEY,
	movie_name varchar(256) NOT NULL
);
"""

staging_tvshows_create = """
CREATE TABLE IF NOT EXISTS  public.tvshows (
	tvshow_id varchar(256) PRIMARY KEY,
	tvshow_name varchar(256) NOT NULL
);
"""

staging_animatedmovies_create = """
CREATE TABLE IF NOT EXISTS public.animatedmovies (
	animatedmovie_id varchar(256) PRIMARY KEY,
	animatedmovie_name varchar(256) NOT NULL
);
"""

staging_songs_create = """
CREATE TABLE public.songs (
	song_id varchar(256) PRIMARY KEY,
	song_name varchar(256) NOT NULL
);
"""

staging_videogames_create = """
CREATE TABLE  public.videogames (
	videogame_id varchar(256) PRIMARY KEY,
	videogame_name varchar(256) NOT NULL
);
"""

staging_books_create = """
CREATE TABLE  public.books (
	book_id varchar(256) PRIMARY KEY,
	book_name varchar(256) NOT NULL
);
"""

staging_movie_roles_create = """
CREATE TABLE  public.movie_roles (
	movie_id varchar(256) NOT NULL,
	role_id varchar(256) NOT NULL,
    human_id varchar(256) NOT NULL,
    PRIMARY KEY(movie_id, role_id, human_id)
);
"""

staging_tvshow_roles_create = """
CREATE TABLE public.tvshow_roles (
	tvshow_id varchar(256) NOT NULL,
	role_id varchar(256) NOT NULL,
    human_id varchar(256) NOT NULL,
    PRIMARY KEY(tvshow_id, role_id, human_id)
);
"""

staging_animatedmovie_roles_create = """
CREATE TABLE public.animatedmovie_roles (
	animatedmovie_id varchar(256) NOT NULL,
	role_id varchar(256) NOT NULL,
    human_id varchar(256) NOT NULL,
    PRIMARY KEY(animatedmovie_id, role_id, human_id)
);
"""

staging_song_roles_create = """
CREATE TABLE public.song_roles (
	song_id varchar(256) NOT NULL,
	role_id varchar(256) NOT NULL,
    human_id varchar(256) NOT NULL,
    PRIMARY KEY(song_id , role_id, human_id)
);
"""

staging_videogame_roles_create = """
CREATE TABLE public.videogame_roles (
	videogame_id varchar(256) NOT NULL,
	role_id varchar(256) NOT NULL,
    human_id varchar(256)  NOT NULL,
    PRIMARY KEY(videogame_id, role_id, human_id)
);
"""

staging_book_roles_create = """
CREATE TABLE public.book_roles (	
	book_id varchar(256) NOT NULL,
	role_id varchar(256) NOT NULL,
    human_id varchar(256) NOT NULL,
    PRIMARY KEY(book_id, role_id, human_id)
);
"""

creative_works_create = """
CREATE TABLE IF NOT EXISTS  creative_works (
	creative_work_id varchar(256) PRIMARY KEY ,
	creative_work_type varchar(256) NOT NULL,
    creative_work_name varchar(256) NOT NULL

);
"""

participations_create = """
CREATE TABLE IF NOT EXISTS participations (
	creative_work_id  varchar(256),
	human_id varchar(256) NOT NULL,
	role_name varchar(256) NOT NULL,
	PRIMARY KEY (creative_work_id, human_id, role_name)
);
"""

create_table_queries = [humans_create, staging_roles_create, staging_movies_create, staging_tvshows_create, staging_animatedmovies_create, staging_songs_create, staging_videogames_create, staging_books_create, staging_movie_roles_create, staging_tvshow_roles_create, staging_animatedmovie_roles_create, staging_song_roles_create, staging_videogame_roles_create, staging_book_roles_create, creative_works_create, participations_create]

drop_table_queries = [humans_drop, staging_roles_drop, staging_movies_drop, staging_tvshows_drop, staging_animatedmovies_drop, staging_songs_drop, staging_videogames_drop, staging_books_drop, staging_movie_roles_drop, staging_tvshow_roles_drop, staging_animatedmovie_roles_drop, staging_song_roles_drop, staging_videogame_roles_drop, staging_book_roles_drop, creative_works_drop, creative_works_participations]


def create_schema(cur, conn):
	print("Creating schema....")
	for drop_table_query in drop_table_queries:
		cur.execute(drop_table_query)
	for create_table_query in create_table_queries:
		cur.execute(create_table_query)
	conn.commit()