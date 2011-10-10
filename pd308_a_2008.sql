--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: pd308_a_2008; Type: TABLE; Schema: public; Owner: canada; Tablespace: 
--

CREATE TABLE pd308_a_2008 (
    gid integer NOT NULL,
    area numeric,
    perimeter numeric,
    pd_id integer,
    pd_num integer,
    pd_nbr_sfx character varying(6),
    pd_type character varying(1),
    adv_poll character varying(3),
    ed_id integer,
    fed_num integer,
    a_updt_dte date,
    g_updt_dte date,
    emrp_name character varying(120),
    objectid numeric(10,0),
    shape_area numeric,
    shape_len numeric,
    the_geom geometry,
    the_geom_nowater geometry,
    CONSTRAINT enforce_dims_the_geom CHECK ((st_ndims(the_geom) = 2)),
    CONSTRAINT enforce_dims_the_geom_nowater CHECK ((st_ndims(the_geom_nowater) = 2)),
    CONSTRAINT enforce_geotype_the_geom CHECK (((geometrytype(the_geom) = 'MULTIPOLYGON'::text) OR (the_geom IS NULL))),
    CONSTRAINT enforce_srid_the_geom CHECK ((st_srid(the_geom) = 3347)),
    CONSTRAINT enforce_srid_the_geom_nowater CHECK ((st_srid(the_geom_nowater) = 4326))
);


ALTER TABLE public.pd308_a_2008 OWNER TO canada;

--
-- Name: pd308_a_2008_gid_seq; Type: SEQUENCE; Schema: public; Owner: canada
--

CREATE SEQUENCE pd308_a_2008_gid_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.pd308_a_2008_gid_seq OWNER TO canada;

--
-- Name: pd308_a_2008_gid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: canada
--

ALTER SEQUENCE pd308_a_2008_gid_seq OWNED BY pd308_a_2008.gid;


--
-- Name: gid; Type: DEFAULT; Schema: public; Owner: canada
--

ALTER TABLE pd308_a_2008 ALTER COLUMN gid SET DEFAULT nextval('pd308_a_2008_gid_seq'::regclass);


--
-- Name: pd308_a_pkey; Type: CONSTRAINT; Schema: public; Owner: canada; Tablespace: 
--

ALTER TABLE ONLY pd308_a_2008
    ADD CONSTRAINT pd308_a_pkey PRIMARY KEY (gid);


--
-- Name: pd308_a_the_geom_gist; Type: INDEX; Schema: public; Owner: canada; Tablespace: 
--

CREATE INDEX pd308_a_the_geom_gist ON pd308_a_2008 USING gist (the_geom);


--
-- PostgreSQL database dump complete
--

