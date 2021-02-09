# flink-stateful-example

### Docker-compose
Deployment using docker compose
`docker-compose up -d`
### Postgres DB
Need to create database flink and table users

I use https://www.pgadmin.org/ that helps easy manage database
```
-- Database: flink

-- DROP DATABASE flink;

CREATE DATABASE flink
WITH
OWNER = postgres
ENCODING = 'UTF8'
LC_COLLATE = 'en_US.utf8'
LC_CTYPE = 'en_US.utf8'
TABLESPACE = pg_default
CONNECTION LIMIT = -1;

-- Table: public.users

-- DROP TABLE public.users;

CREATE TABLE public.users
(
id integer NOT NULL DEFAULT nextval('users_id_seq'::regclass),
full_name text COLLATE pg_catalog."default",
name text COLLATE pg_catalog."default",
greeting text COLLATE pg_catalog."default",
CONSTRAINT users_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE public.users
OWNER to postgres;
```

### testing script

```
cd api/
./test.sh 10 #where 10 is number of users for creating 
```

