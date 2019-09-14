
-- CREATE DATABASE wikidata;
-- CREATE USER wikidata WITH ENCRYPTED PASSWORD 'wikidata';
-- GRANT ALL PRIVILEGES on DATABASE wikidata TO wikidata
-- \connect wikidata
-- \i create_tables_staging.sql
--\set autocommit off


DROP TABLE public.creative_works;
CREATE TABLE IF NOT EXISTS  public.creative_works (
	creative_work_id varchar(256) PRIMARY KEY ,
	creative_work_type varchar(256) NOT NULL,
    creative_work_name varchar(256) NOT NULL

);
GRANT ALL PRIVILEGES ON TABLE creative_works TO wikidata;


DROP TABLE public.participations;
CREATE TABLE IF NOT EXISTS  public.participations (
	creative_work_id  varchar(256),
	human_id varchar(256) NOT NULL,
	role_name varchar(256) NOT NULL,
	PRIMARY KEY (creative_work_id, human_id, role_name)
);
GRANT ALL PRIVILEGES ON TABLE participations TO wikidata;

COMMIT;

