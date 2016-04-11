-- Database: "AnonChat_db"
-- DROP DATABASE "AnonChat_db";
CREATE DATABASE "AnonChat_db"
  WITH OWNER = postgres
       ENCODING = 'UTF8'
       TABLESPACE = pg_default
       LC_COLLATE = 'English_United States.1252'
       LC_CTYPE = 'English_United States.1252'
       CONNECTION LIMIT = -1;

-- Sequence: public.chat_log_id_seq
-- DROP SEQUENCE public.chat_log_id_seq;
CREATE SEQUENCE public.chat_log_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE public.chat_log_id_seq
  OWNER TO postgres;
GRANT ALL ON SEQUENCE public.chat_log_id_seq TO postgres;
GRANT ALL ON SEQUENCE public.chat_log_id_seq TO get_history;
GRANT ALL ON SEQUENCE public.chat_log_id_seq TO post_message;

-- Sequence: public.users_id_seq
-- DROP SEQUENCE public.users_id_seq;
CREATE SEQUENCE public.users_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 10
  CACHE 1;
ALTER TABLE public.users_id_seq
  OWNER TO postgres;
GRANT ALL ON SEQUENCE public.users_id_seq TO postgres;
GRANT ALL ON SEQUENCE public.users_id_seq TO chat_partners;
GRANT ALL ON SEQUENCE public.users_id_seq TO get_history;
GRANT ALL ON SEQUENCE public.users_id_seq TO post_message;

-- Table: public.chat_log
-- DROP TABLE public.chat_log;
CREATE TABLE public.chat_log
(
  id integer NOT NULL DEFAULT nextval('chat_log_id_seq'::regclass),
  chat_text text
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.chat_log
  OWNER TO postgres;
GRANT ALL ON TABLE public.chat_log TO postgres;
GRANT ALL ON TABLE public.chat_log TO get_history;
GRANT ALL ON TABLE public.chat_log TO post_message;

-- Table: public.user_connections
-- DROP TABLE public.user_connections;
CREATE TABLE public.user_connections
(
  id integer NOT NULL,
  second_id integer NOT NULL,
  chat_id integer NOT NULL
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.user_connections
  OWNER TO postgres;
GRANT ALL ON TABLE public.user_connections TO postgres;
GRANT SELECT ON TABLE public.user_connections TO chat_partners;
GRANT ALL ON TABLE public.user_connections TO get_history;
GRANT ALL ON TABLE public.user_connections TO post_message;

-- Table: public.users
-- DROP TABLE public.users;
CREATE TABLE public.users
(
  id integer NOT NULL DEFAULT nextval('users_id_seq'::regclass),
  username text NOT NULL
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.users
  OWNER TO postgres;
GRANT ALL ON TABLE public.users TO postgres;
GRANT ALL ON TABLE public.users TO chat_partners;
GRANT ALL ON TABLE public.users TO get_history;
GRANT ALL ON TABLE public.users TO post_message;
