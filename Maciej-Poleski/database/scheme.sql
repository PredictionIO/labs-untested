--
-- PostgreSQL database dump
--

-- Dumped from database version 9.4.5
-- Dumped by pg_dump version 9.4.5
-- Started on 2015-12-30 20:31:45 CET

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

DROP DATABASE "studia";
--
-- TOC entry 2088 (class 1262 OID 16385)
-- Name: studia; Type: DATABASE; Schema: -; Owner: -
--

CREATE DATABASE "studia" WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'pl_PL.utf8' LC_CTYPE = 'pl_PL.utf8';


\connect "studia"

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 5 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA "public";


--
-- TOC entry 2089 (class 0 OID 0)
-- Dependencies: 5
-- Name: SCHEMA "public"; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA "public" IS 'standard public schema';


--
-- TOC entry 188 (class 3079 OID 11867)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "plpgsql" WITH SCHEMA "pg_catalog";


--
-- TOC entry 2090 (class 0 OID 0)
-- Dependencies: 188
-- Name: EXTENSION "plpgsql"; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION "plpgsql" IS 'PL/pgSQL procedural language';


SET search_path = "public", pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 172 (class 1259 OID 16386)
-- Name: conversions; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE "conversions" (
    "userId" bigint NOT NULL,
    "itemId" bigint,
    "price" numeric,
    "quantity" bigint,
    "timestamp" timestamp without time zone
);


--
-- TOC entry 173 (class 1259 OID 16392)
-- Name: items; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE "items" (
    "itemId" bigint NOT NULL,
    "style" bigint,
    "personality" bigint,
    "color" bigint,
    "theme" bigint,
    "price" numeric,
    "category" bigint
);


--
-- TOC entry 175 (class 1259 OID 16401)
-- Name: users; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE "users" (
    "userId" bigint NOT NULL,
    "registerCountry" character varying,
    "signupTime" timestamp without time zone
);


--
-- TOC entry 187 (class 1259 OID 16568)
-- Name: time_ranges; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW "time_ranges" AS
 SELECT "users"."userId",
    "sum"(
        CASE
            WHEN (("conversions"."timestamp" <= ("users"."signupTime" + '30 days'::interval)) AND ("conversions"."timestamp" >= "users"."signupTime")) THEN ("conversions"."price" * ("conversions"."quantity")::numeric)
            ELSE (0)::numeric
        END) AS "revenue_in_30days",
    "sum"(
        CASE
            WHEN (("conversions"."timestamp" <= ("users"."signupTime" + '1 day'::interval)) AND ("conversions"."timestamp" >= "users"."signupTime")) THEN ("conversions"."price" * ("conversions"."quantity")::numeric)
            ELSE (0)::numeric
        END) AS "revenue_in_1day",
    "sum"(
        CASE
            WHEN (("conversions"."timestamp" <= ("users"."signupTime" + '2 days'::interval)) AND ("conversions"."timestamp" > ("users"."signupTime" + '1 day'::interval))) THEN ("conversions"."price" * ("conversions"."quantity")::numeric)
            ELSE (0)::numeric
        END) AS "revenue_in_2day",
    "sum"(
        CASE
            WHEN (("conversions"."timestamp" <= ("users"."signupTime" + '3 days'::interval)) AND ("conversions"."timestamp" > ("users"."signupTime" + '2 days'::interval))) THEN ("conversions"."price" * ("conversions"."quantity")::numeric)
            ELSE (0)::numeric
        END) AS "revenue_in_3day",
    "sum"(
        CASE
            WHEN (("conversions"."timestamp" <= ("users"."signupTime" + '4 days'::interval)) AND ("conversions"."timestamp" > ("users"."signupTime" + '3 days'::interval))) THEN ("conversions"."price" * ("conversions"."quantity")::numeric)
            ELSE (0)::numeric
        END) AS "revenue_in_4day",
    "sum"(
        CASE
            WHEN (("conversions"."timestamp" <= ("users"."signupTime" + '5 days'::interval)) AND ("conversions"."timestamp" > ("users"."signupTime" + '4 days'::interval))) THEN ("conversions"."price" * ("conversions"."quantity")::numeric)
            ELSE (0)::numeric
        END) AS "revenue_in_5day",
    "sum"(
        CASE
            WHEN (("conversions"."timestamp" <= ("users"."signupTime" + '6 days'::interval)) AND ("conversions"."timestamp" > ("users"."signupTime" + '5 days'::interval))) THEN ("conversions"."price" * ("conversions"."quantity")::numeric)
            ELSE (0)::numeric
        END) AS "revenue_in_6day",
    "sum"(
        CASE
            WHEN (("conversions"."timestamp" <= ("users"."signupTime" + '7 days'::interval)) AND ("conversions"."timestamp" > ("users"."signupTime" + '6 days'::interval))) THEN ("conversions"."price" * ("conversions"."quantity")::numeric)
            ELSE (0)::numeric
        END) AS "revenue_in_7day"
   FROM ("users"
     LEFT JOIN "conversions" ON (("users"."userId" = "conversions"."userId")))
  GROUP BY "users"."userId";


--
-- TOC entry 174 (class 1259 OID 16398)
-- Name: user_ads; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE "user_ads" (
    "userId" bigint NOT NULL,
    "utmSource" bigint,
    "utmCampaign" bigint,
    "utmMedium" bigint,
    "utmTerm" bigint,
    "utmContent" bigint
);


--
-- TOC entry 176 (class 1259 OID 16407)
-- Name: users_revenue_register; Type: MATERIALIZED VIEW; Schema: public; Owner: -; Tablespace: 
--

CREATE MATERIALIZED VIEW "users_revenue_register" AS
 SELECT "users"."userId",
    "sum"(
        CASE
            WHEN (("conversions"."timestamp" <= ("users"."signupTime" + '30 days'::interval)) AND ("conversions"."timestamp" >= "users"."signupTime")) THEN ("conversions"."price" * ("conversions"."quantity")::numeric)
            ELSE (0)::numeric
        END) AS "revenue_in_30days",
    "sum"(
        CASE
            WHEN (("conversions"."timestamp" <= ("users"."signupTime" + '7 days'::interval)) AND ("conversions"."timestamp" >= "users"."signupTime")) THEN ("conversions"."price" * ("conversions"."quantity")::numeric)
            ELSE (0)::numeric
        END) AS "revenue_in_7days"
   FROM ("users"
     LEFT JOIN "conversions" ON (("users"."userId" = "conversions"."userId")))
  GROUP BY "users"."userId"
  WITH NO DATA;


--
-- TOC entry 177 (class 1259 OID 16415)
-- Name: users_5000_month; Type: MATERIALIZED VIEW; Schema: public; Owner: -; Tablespace: 
--

CREATE MATERIALIZED VIEW "users_5000_month" AS
 SELECT "users_revenue_register"."userId",
    "users_revenue_register"."revenue_in_30days",
    "users_revenue_register"."revenue_in_7days"
   FROM "users_revenue_register"
  WHERE ("users_revenue_register"."revenue_in_30days" > (5000)::numeric)
  WITH NO DATA;


--
-- TOC entry 178 (class 1259 OID 16422)
-- Name: users_firstbuy; Type: MATERIALIZED VIEW; Schema: public; Owner: -; Tablespace: 
--

CREATE MATERIALIZED VIEW "users_firstbuy" AS
 SELECT "users"."userId",
    "min"("conversions"."timestamp") AS "first_buy"
   FROM ("users"
     LEFT JOIN "conversions" ON (("users"."userId" = "conversions"."userId")))
  GROUP BY "users"."userId"
  WITH NO DATA;


--
-- TOC entry 179 (class 1259 OID 16426)
-- Name: users_firstaction; Type: MATERIALIZED VIEW; Schema: public; Owner: -; Tablespace: 
--

CREATE MATERIALIZED VIEW "users_firstaction" AS
 SELECT "users"."userId",
    LEAST("users"."signupTime", "users_firstbuy"."first_buy") AS "first_action"
   FROM ("users"
     LEFT JOIN "users_firstbuy" ON (("users"."userId" = "users_firstbuy"."userId")))
  WITH NO DATA;


--
-- TOC entry 2091 (class 0 OID 0)
-- Dependencies: 179
-- Name: MATERIALIZED VIEW "users_firstaction"; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON MATERIALIZED VIEW "users_firstaction" IS 'na razie bez view.csv';


--
-- TOC entry 183 (class 1259 OID 16540)
-- Name: users_properties; Type: MATERIALIZED VIEW; Schema: public; Owner: -; Tablespace: 
--

CREATE MATERIALIZED VIEW "users_properties" AS
 SELECT "users"."userId",
    "user_ads"."utmContent",
    "user_ads"."utmSource",
    "users_firstaction"."first_action",
    "users_firstbuy"."first_buy",
    "users_revenue_register"."revenue_in_7days",
    "users_revenue_register"."revenue_in_30days"
   FROM (((("users"
     LEFT JOIN "users_revenue_register" ON (("users"."userId" = "users_revenue_register"."userId")))
     LEFT JOIN "user_ads" ON (("users"."userId" = "user_ads"."userId")))
     LEFT JOIN "users_firstaction" ON (("users"."userId" = "users_firstaction"."userId")))
     LEFT JOIN "users_firstbuy" ON (("users"."userId" = "users_firstbuy"."userId")))
  WITH NO DATA;


--
-- TOC entry 180 (class 1259 OID 16430)
-- Name: views; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE "views" (
    "userId" character varying,
    "itemId" bigint,
    "timestamp" timestamp without time zone,
    "pagetype" character varying
);


--
-- TOC entry 182 (class 1259 OID 16524)
-- Name: users_views_distribution; Type: MATERIALIZED VIEW; Schema: public; Owner: -; Tablespace: 
--

CREATE MATERIALIZED VIEW "users_views_distribution" AS
 SELECT "views"."userId",
    ("count"(NULLIF('Product'::"text", ("views"."pagetype")::"text")))::integer AS "views_product",
    ("count"(NULLIF('Collection'::"text", ("views"."pagetype")::"text")))::integer AS "views_collection",
    ("count"(NULLIF('Category'::"text", ("views"."pagetype")::"text")))::integer AS "views_category",
    "count"(*) AS "views_any"
   FROM "views"
  GROUP BY "views"."userId"
  WITH NO DATA;


--
-- TOC entry 184 (class 1259 OID 16548)
-- Name: users_features; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW "users_features" AS
 SELECT "users_properties"."userId",
    COALESCE("users_properties"."utmContent", ((-1))::bigint) AS "utmContent",
    COALESCE("users_properties"."utmSource", ((-1))::bigint) AS "utmSource",
    "date_part"('epoch'::"text", ("users_properties"."first_buy" - "users_properties"."first_action")) AS "time_to_buy",
    "users_properties"."revenue_in_7days",
    "users_properties"."revenue_in_30days",
    "users_views_distribution"."views_product",
    "users_views_distribution"."views_collection",
    "users_views_distribution"."views_category"
   FROM ("users_properties"
     JOIN "users_views_distribution" ON (((("users_properties"."userId")::character varying)::"text" = ("users_views_distribution"."userId")::"text")))
  WHERE ("users_properties"."first_buy" IS NOT NULL);


--
-- TOC entry 185 (class 1259 OID 16553)
-- Name: users_features_reduced; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW "users_features_reduced" AS
 SELECT ("users_features"."time_to_buy" / (1000000)::double precision) AS "time_to_buy_normalized",
    "users_features"."revenue_in_7days",
    "users_features"."revenue_in_30days",
    "users_features"."views_product",
    "users_features"."views_collection",
    "users_features"."views_category",
    "users_features"."utmSource",
    "time_ranges"."revenue_in_1day",
    "time_ranges"."revenue_in_2day",
    "time_ranges"."revenue_in_3day",
    "time_ranges"."revenue_in_4day",
    "time_ranges"."revenue_in_5day",
    "time_ranges"."revenue_in_6day",
    "time_ranges"."revenue_in_7day"
   FROM ("users_features"
     LEFT JOIN "time_ranges" ON (("time_ranges"."userId" = "users_features"."userId")));


--
-- TOC entry 186 (class 1259 OID 16558)
-- Name: utm_sources; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW "utm_sources" AS
 SELECT DISTINCT "user_ads"."utmSource"
   FROM "user_ads";


--
-- TOC entry 181 (class 1259 OID 16436)
-- Name: views_users; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW "views_users" AS
 SELECT ("views"."userId")::bigint AS "userId",
    "views"."itemId",
    "views"."timestamp",
    "views"."pagetype"
   FROM "views"
  WHERE (("views"."userId")::"text" <> 'deleted'::"text");


--
-- TOC entry 1958 (class 2606 OID 16441)
-- Name: item_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY "items"
    ADD CONSTRAINT "item_pkey" PRIMARY KEY ("itemId");


--
-- TOC entry 1960 (class 2606 OID 16443)
-- Name: user_ads_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY "user_ads"
    ADD CONSTRAINT "user_ads_pkey" PRIMARY KEY ("userId");


--
-- TOC entry 1962 (class 2606 OID 16445)
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY "users"
    ADD CONSTRAINT "users_pkey" PRIMARY KEY ("userId");


--
-- TOC entry 1963 (class 1259 OID 16523)
-- Name: views_userId_index; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX "views_userId_index" ON "views" USING "btree" ("userId" COLLATE "C");


-- Completed on 2015-12-30 20:31:45 CET

--
-- PostgreSQL database dump complete
--

