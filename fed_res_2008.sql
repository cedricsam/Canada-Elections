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
-- Name: fed_res_2008; Type: TABLE; Schema: public; Owner: canada; Tablespace: 
--

CREATE TABLE fed_res_2008 (
    fed_num integer NOT NULL,
    ed_namee character varying(128),
    ed_namef character varying(128),
    pd_num character varying(16) NOT NULL,
    pd_name character varying(512),
    void boolean,
    nopoll boolean,
    mergedwith character varying(16),
    nb_rejected integer,
    nb_electors integer,
    cand_lastname character varying(128) NOT NULL,
    cand_middlename character varying(128),
    cand_firstname character varying(128) NOT NULL,
    party_namee character varying(64) NOT NULL,
    party_namef character varying(64) NOT NULL,
    incumbent boolean,
    elected boolean,
    nb_votes integer NOT NULL
);


ALTER TABLE public.fed_res_2008 OWNER TO canada;

--
-- Name: fed_res_2008_pkey; Type: CONSTRAINT; Schema: public; Owner: canada; Tablespace: 
--

ALTER TABLE ONLY fed_res_2008
    ADD CONSTRAINT fed_res_2008_pkey PRIMARY KEY (fed_num, pd_num, party_namee, cand_lastname, cand_firstname);


--
-- Name: fed_res_2008_votes_idx; Type: INDEX; Schema: public; Owner: canada; Tablespace: 
--

CREATE INDEX fed_res_2008_votes_idx ON fed_res_2008 USING btree (fed_num, pd_num, nb_votes DESC);


--
-- PostgreSQL database dump complete
--

