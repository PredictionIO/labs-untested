--
-- PostgreSQL database dump
--

-- Dumped from database version 9.4.5
-- Dumped by pg_dump version 9.4.5
-- Started on 2015-11-08 15:43:54 CET

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 2660 (class 1262 OID 16385)
-- Name: studia; Type: DATABASE; Schema: -; Owner: -
--

CREATE DATABASE studia WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'pl_PL.UTF-8' LC_CTYPE = 'pl_PL.UTF-8';


\connect studia

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 182 (class 3079 OID 12472)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2662 (class 0 OID 0)
-- Dependencies: 182
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 174 (class 1259 OID 16454)
-- Name: conversions; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE conversions (
    "userId" bigint NOT NULL,
    "itemId" bigint,
    price numeric,
    quantity bigint,
    "timestamp" timestamp without time zone
);


--
-- TOC entry 173 (class 1259 OID 16428)
-- Name: items; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE items (
    "itemId" bigint NOT NULL,
    style bigint,
    personality bigint,
    color bigint,
    theme bigint,
    price numeric,
    category bigint
);


--
-- TOC entry 172 (class 1259 OID 16394)
-- Name: user_ads; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE user_ads (
    "userId" bigint NOT NULL,
    "utmSource" bigint,
    "utmCampaign" bigint,
    "utmMedium" bigint,
    "utmTerm" bigint,
    "utmContent" bigint
);


--
-- TOC entry 176 (class 1259 OID 16475)
-- Name: users; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE users (
    "userId" bigint NOT NULL,
    "registerCountry" character varying,
    "signupTime" timestamp without time zone
);


--
-- TOC entry 180 (class 1259 OID 24594)
-- Name: users_revenue_register; Type: MATERIALIZED VIEW; Schema: public; Owner: -; Tablespace: 
--

CREATE MATERIALIZED VIEW users_revenue_register AS
 SELECT users."userId",
    sum(
        CASE
            WHEN ((conversions."timestamp" <= (users."signupTime" + '30 days'::interval)) AND (conversions."timestamp" >= users."signupTime")) THEN (conversions.price * (conversions.quantity)::numeric)
            ELSE (0)::numeric
        END) AS revenue_in_30days,
    sum(
        CASE
            WHEN ((conversions."timestamp" <= (users."signupTime" + '7 days'::interval)) AND (conversions."timestamp" >= users."signupTime")) THEN (conversions.price * (conversions.quantity)::numeric)
            ELSE (0)::numeric
        END) AS revenue_in_7days
   FROM (users
     LEFT JOIN conversions ON ((users."userId" = conversions."userId")))
  GROUP BY users."userId"
  WITH NO DATA;


--
-- TOC entry 181 (class 1259 OID 24602)
-- Name: users_5000_month; Type: MATERIALIZED VIEW; Schema: public; Owner: -; Tablespace: 
--

CREATE MATERIALIZED VIEW users_5000_month AS
 SELECT users_revenue_register."userId",
    users_revenue_register.revenue_in_30days,
    users_revenue_register.revenue_in_7days
   FROM users_revenue_register
  WHERE (users_revenue_register.revenue_in_30days > (5000)::numeric)
  WITH NO DATA;


--
-- TOC entry 178 (class 1259 OID 24585)
-- Name: users_firstbuy; Type: MATERIALIZED VIEW; Schema: public; Owner: -; Tablespace: 
--

CREATE MATERIALIZED VIEW users_firstbuy AS
 SELECT users."userId",
    min(conversions."timestamp") AS first_buy
   FROM (users
     LEFT JOIN conversions ON ((users."userId" = conversions."userId")))
  GROUP BY users."userId"
  WITH NO DATA;


--
-- TOC entry 179 (class 1259 OID 24590)
-- Name: users_firstaction; Type: MATERIALIZED VIEW; Schema: public; Owner: -; Tablespace: 
--

CREATE MATERIALIZED VIEW users_firstaction AS
 SELECT users."userId",
    LEAST(users."signupTime", users_firstbuy.first_buy) AS first_action
   FROM (users
     LEFT JOIN users_firstbuy ON ((users."userId" = users_firstbuy."userId")))
  WITH NO DATA;


--
-- TOC entry 2663 (class 0 OID 0)
-- Dependencies: 179
-- Name: MATERIALIZED VIEW users_firstaction; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON MATERIALIZED VIEW users_firstaction IS 'na razie bez view.csv';


--
-- TOC entry 175 (class 1259 OID 16468)
-- Name: views; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE views (
    "userId" character varying,
    "itemId" bigint,
    "timestamp" timestamp without time zone,
    pagetype character varying
);


--
-- TOC entry 177 (class 1259 OID 16483)
-- Name: views_users; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW views_users AS
 SELECT (views."userId")::bigint AS "userId",
    views."itemId",
    views."timestamp",
    views.pagetype
   FROM views
  WHERE ((views."userId")::text <> 'deleted'::text);


--
-- TOC entry 2539 (class 2606 OID 16432)
-- Name: item_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY items
    ADD CONSTRAINT item_pkey PRIMARY KEY ("itemId");


--
-- TOC entry 2537 (class 2606 OID 16400)
-- Name: user_ads_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY user_ads
    ADD CONSTRAINT user_ads_pkey PRIMARY KEY ("userId");


--
-- TOC entry 2541 (class 2606 OID 16482)
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY ("userId");


-- Completed on 2015-11-08 15:43:54 CET

--
-- PostgreSQL database dump complete
--

