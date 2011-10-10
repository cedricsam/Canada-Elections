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
-- Name: pd308_p_2011; Type: TABLE; Schema: public; Owner: canada; Tablespace: 
--

CREATE TABLE pd308_p_2011 (
    gid integer NOT NULL,
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
    mobile_pol integer,
    sbpd_addre integer,
    address_id numeric(10,0),
    st_adr_nbr character varying(6),
    st_adr_n_1 character varying(1),
    street_id integer,
    st_nme character varying(50),
    st_typ_cde character varying(6),
    st_drctn_c character varying(3),
    from_ste_n character varying(6),
    to_ste_nbr character varying(6),
    from_floor character varying(5),
    to_floor character varying(5),
    bldg_namee character varying(60),
    bldg_namef character varying(60),
    old_pd_id integer,
    poll_name character varying(100),
    pn_updt_dt date,
    ad_updt_dt date,
    urban_rura character varying(2),
    the_geom geometry,
    CONSTRAINT enforce_dims_the_geom CHECK ((st_ndims(the_geom) = 2)),
    CONSTRAINT enforce_geotype_the_geom CHECK (((geometrytype(the_geom) = 'POINT'::text) OR (the_geom IS NULL))),
    CONSTRAINT enforce_srid_the_geom CHECK ((st_srid(the_geom) = 3347))
);


ALTER TABLE public.pd308_p_2011 OWNER TO canada;

--
-- Name: pd308_p_2011_gid_seq; Type: SEQUENCE; Schema: public; Owner: canada
--

CREATE SEQUENCE pd308_p_2011_gid_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.pd308_p_2011_gid_seq OWNER TO canada;

--
-- Name: pd308_p_2011_gid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: canada
--

ALTER SEQUENCE pd308_p_2011_gid_seq OWNED BY pd308_p_2011.gid;


--
-- Name: gid; Type: DEFAULT; Schema: public; Owner: canada
--

ALTER TABLE pd308_p_2011 ALTER COLUMN gid SET DEFAULT nextval('pd308_p_2011_gid_seq'::regclass);


--
-- Name: pd308_p_2011_pkey; Type: CONSTRAINT; Schema: public; Owner: canada; Tablespace: 
--

ALTER TABLE ONLY pd308_p_2011
    ADD CONSTRAINT pd308_p_2011_pkey PRIMARY KEY (gid);


--
-- Name: pd308_p_2011_the_geom_gist; Type: INDEX; Schema: public; Owner: canada; Tablespace: 
--

CREATE INDEX pd308_p_2011_the_geom_gist ON pd308_p_2011 USING gist (the_geom);


--
-- PostgreSQL database dump complete
--

