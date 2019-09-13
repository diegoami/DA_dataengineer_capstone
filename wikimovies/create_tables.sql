CREATE TABLE  public.occupations (
	occupation_id varchar(256) NOT NULL,
	occupation_name varchar(256)
);
GRANT ALL PRIVILEGES ON TABLE occupations TO wikidata;

CREATE TABLE  public.humans (
	human_id varchar(256) NOT NULL,
	human_name varchar(256),
	occupation_id varchar(256) NOT NULL
);

CREATE TABLE  public.movies (
	movie_id varchar(256) NOT NULL,
	movie_name varchar(256)
);

CREATE TABLE  public.tvshows (
	tvshow_id varchar(256) NOT NULL,
	tvshow_name varchar(256)
);

CREATE TABLE public.animatedmovies (
	animatedmovie_id varchar(256) NOT NULL,
	animatedmovie_name varchar(256)
);

CREATE TABLE public.songs (
	song_id varchar(256) NOT NULL,
	song_name varchar(256)
);

CREATE TABLE  public.roles (
	role_id varchar(256) NOT NULL,
	role_name varchar(256)
);


CREATE TABLE  public.videogames (
	videogame_id varchar(256) NOT NULL,
	videogame_name varchar(256)
);

CREATE TABLE  public.books (
	book_id varchar(256) NOT NULL,
	book_name varchar(256)
);

CREATE TABLE  public.movie_roles (
	movie_id varchar(256) NOT NULL,
	role_id varchar(256),
    human_id varchar(256)
);


CREATE TABLE public.tvshow_role (
	tvshow_id varchar(256) NOT NULL,
	role_id varchar(256),
    human_id varchar(256)
);

CREATE TABLE public.animatedmovie_role (
	animatedmovie_id varchar(256) NOT NULL,
	role_id varchar(256),
    human_id varchar(256)
);

CREATE TABLE public.song_role (
	song_id varchar(256) NOT NULL,
	role_id varchar(256),
    human_id varchar(256)
);

CREATE TABLE public.videogame_role (
	videogame_id varchar(256) NOT NULL,
	role_id varchar(256),
    human_id varchar(256)
);

CREATE TABLE public.book_role (
	book_id varchar(256) NOT NULL,
	role_id varchar(256),
    human_id varchar(256)
);

