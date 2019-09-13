
-- CREATE DATABASE wikidata;
-- CREATE USER wikidata WITH ENCRYPTED PASSWORD 'wikidata';
-- GRANT ALL PRIVILEGES on DATABASE wikidata TO wikidata;
-- \connect wikidata
-- \i create_tables.sql

DROP TABLE public.occupations;
CREATE TABLE public.occupations (
	occupation_id varchar(256) PRIMARY KEY,
	occupation_name varchar(256) NOT NULL
);
GRANT ALL PRIVILEGES ON TABLE occupations TO wikidata;

DROP TABLE public.humans;
CREATE TABLE IF NOT EXISTS  public.humans (
	human_id varchar(256) PRIMARY KEY,
	human_name varchar(256) NOT NULL,
	occupation_id varchar(256) NOT NULL
);
GRANT ALL PRIVILEGES ON TABLE humans TO wikidata;

DROP TABLE public.movies;
CREATE TABLE IF NOT EXISTS  public.movies (
	movie_id varchar(256) PRIMARY KEY,
	movie_name varchar(256) NOT NULL
);
GRANT ALL PRIVILEGES ON TABLE movies TO wikidata;

DROP TABLE public.tvshows;
CREATE TABLE IF NOT EXISTS  public.tvshows (
	tvshow_id varchar(256) PRIMARY KEY,
	tvshow_name varchar(256) NOT NULL
);
GRANT ALL PRIVILEGES ON TABLE tvshows TO wikidata;

DROP TABLE public.animatedmovies ;
CREATE TABLE IF NOT EXISTS public.animatedmovies (
	animatedmovie_id varchar(256) PRIMARY KEY,
	animatedmovie_name varchar(256) NOT NULL
);
GRANT ALL PRIVILEGES ON TABLE animatedmovies TO wikidata;

DROP TABLE public.songs;
CREATE TABLE public.songs (
	song_id varchar(256) PRIMARY KEY,
	song_name varchar(256) NOT NULL
);
GRANT ALL PRIVILEGES ON TABLE songs TO wikidata;

DROP TABLE public.roles;
CREATE TABLE  public.roles (
	role_id varchar(256) PRIMARY KEY,
	role_name varchar(256) NOT NULL
);
GRANT ALL PRIVILEGES ON TABLE roles TO wikidata;

DROP TABLE public.videogames ;
CREATE TABLE  public.videogames (
	videogame_id varchar(256) PRIMARY KEY,
	videogame_name varchar(256) NOT NULL
);
GRANT ALL PRIVILEGES ON TABLE videogames TO wikidata;

DROP TABLE public.books  ;
CREATE TABLE  public.books (
	book_id varchar(256) PRIMARY KEY,
	book_name varchar(256) NOT NULL
);
GRANT ALL PRIVILEGES ON TABLE books TO wikidata;

DROP TABLE public.movie_roles;
CREATE TABLE  public.movie_roles (
	movie_id varchar(256) NOT NULL,
	role_id varchar(256) NOT NULL,
    human_id varchar(256) NOT NULL,
    PRIMARY KEY(movie_id, role_id, human_id)
);
GRANT ALL PRIVILEGES ON TABLE movie_roles TO wikidata;

DROP TABLE public.tvshow_roles;
CREATE TABLE public.tvshow_roles (
	tvshow_id varchar(256) NOT NULL,
	role_id varchar(256) NOT NULL,
    human_id varchar(256) NOT NULL,
    PRIMARY KEY(tvshow_id, role_id, human_id)

);
GRANT ALL PRIVILEGES ON TABLE tvshow_roles TO wikidata;

DROP TABLE public.animatedmovie_roles;
CREATE TABLE public.animatedmovie_roles (
	animatedmovie_id varchar(256) NOT NULL,
	role_id varchar(256) NOT NULL,
    human_id varchar(256) NOT NULL,
    PRIMARY KEY(animatedmovie_id, role_id, human_id)
);
GRANT ALL PRIVILEGES ON TABLE animatedmovie_roles TO wikidata;

DROP TABLE public.song_roles;
CREATE TABLE public.song_roles (
	song_id varchar(256) NOT NULL,
	role_id varchar(256) NOT NULL,
    human_id varchar(256) NOT NULL,
    PRIMARY KEY(song_id , role_id, human_id)
);
GRANT ALL PRIVILEGES ON TABLE song_roles  TO wikidata;


DROP TABLE videogame_roles;
CREATE TABLE public.videogame_roles (
	videogame_id varchar(256) NOT NULL,
	role_id varchar(256) NOT NULL,
    human_id varchar(256)  NOT NULL,
    PRIMARY KEY(videogame_id, role_id, human_id)
);
GRANT ALL PRIVILEGES ON TABLE videogame_roles  TO wikidata;


DROP TABLE public.book_roles ;
CREATE TABLE public.book_roles (
	book_id varchar(256) NOT NULL,
	role_id varchar(256) NOT NULL,
    human_id varchar(256) NOT NULL,
    PRIMARY KEY(book_id, role_id, human_id)
);
GRANT ALL PRIVILEGES ON TABLE book_roles  TO wikidata;

COMMIT;

