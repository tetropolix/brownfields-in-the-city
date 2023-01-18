--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5 (Ubuntu 14.5-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.5 (Ubuntu 14.5-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: auth; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA auth;


ALTER SCHEMA auth OWNER TO postgres;

--
-- Name: brownfields; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA brownfields;


ALTER SCHEMA brownfields OWNER TO postgres;

--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry and geography spatial types and functions';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: permissions; Type: TABLE; Schema: auth; Owner: postgres
--

CREATE TABLE auth.permissions (
    id integer NOT NULL,
    name character varying(64) NOT NULL
);


ALTER TABLE auth.permissions OWNER TO postgres;

--
-- Name: permissions_id_seq; Type: SEQUENCE; Schema: auth; Owner: postgres
--

CREATE SEQUENCE auth.permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth.permissions_id_seq OWNER TO postgres;

--
-- Name: permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: auth; Owner: postgres
--

ALTER SEQUENCE auth.permissions_id_seq OWNED BY auth.permissions.id;


--
-- Name: role_permissions; Type: TABLE; Schema: auth; Owner: postgres
--

CREATE TABLE auth.role_permissions (
    permission_id integer NOT NULL,
    role_id integer NOT NULL
);


ALTER TABLE auth.role_permissions OWNER TO postgres;

--
-- Name: roles; Type: TABLE; Schema: auth; Owner: postgres
--

CREATE TABLE auth.roles (
    id integer NOT NULL,
    name character varying(64) NOT NULL
);


ALTER TABLE auth.roles OWNER TO postgres;

--
-- Name: roles_id_seq; Type: SEQUENCE; Schema: auth; Owner: postgres
--

CREATE SEQUENCE auth.roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth.roles_id_seq OWNER TO postgres;

--
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: auth; Owner: postgres
--

ALTER SEQUENCE auth.roles_id_seq OWNED BY auth.roles.id;


--
-- Name: user_roles; Type: TABLE; Schema: auth; Owner: postgres
--

CREATE TABLE auth.user_roles (
    user_id integer NOT NULL,
    role_id integer NOT NULL
);


ALTER TABLE auth.user_roles OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: auth; Owner: postgres
--

CREATE TABLE auth.users (
    id integer NOT NULL,
    last_session character varying(64),
    email character varying(256) NOT NULL,
    phone character varying(32) NOT NULL,
    hashed_password character varying(256) NOT NULL,
    is_admin boolean DEFAULT false NOT NULL,
    is_active boolean NOT NULL
);


ALTER TABLE auth.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: auth; Owner: postgres
--

CREATE SEQUENCE auth.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: auth; Owner: postgres
--

ALTER SEQUENCE auth.users_id_seq OWNED BY auth.users.id;


--
-- Name: area_sizes; Type: TABLE; Schema: brownfields; Owner: postgres
--

CREATE TABLE brownfields.area_sizes (
    id integer NOT NULL,
    value character varying(128) NOT NULL
);


ALTER TABLE brownfields.area_sizes OWNER TO postgres;

--
-- Name: area_sizes_id_seq; Type: SEQUENCE; Schema: brownfields; Owner: postgres
--

CREATE SEQUENCE brownfields.area_sizes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE brownfields.area_sizes_id_seq OWNER TO postgres;

--
-- Name: area_sizes_id_seq; Type: SEQUENCE OWNED BY; Schema: brownfields; Owner: postgres
--

ALTER SEQUENCE brownfields.area_sizes_id_seq OWNED BY brownfields.area_sizes.id;


--
-- Name: brownfields; Type: TABLE; Schema: brownfields; Owner: postgres
--

CREATE TABLE brownfields.brownfields (
    id integer NOT NULL,
    image_directory_uuid character varying(128) NOT NULL,
    street character varying(256) NOT NULL,
    area_ha numeric(12,4) NOT NULL,
    mapping_year integer NOT NULL,
    altitude real NOT NULL,
    color_id integer NOT NULL,
    ownership_type_id integer NOT NULL,
    original_functional_utilization_id integer NOT NULL,
    utilization_id integer NOT NULL,
    area_size_id integer NOT NULL,
    location_id integer NOT NULL,
    degradation_level_id integer NOT NULL,
    residentional_area_category_id integer NOT NULL,
    settlement_id integer NOT NULL,
    infrastructure_availability_id integer NOT NULL,
    natural_and_architectural_value_id integer NOT NULL,
    revitalization_id integer NOT NULL,
    economic_potential_id integer,
    environmental_burden_inclusion_id integer,
    polygon public.geometry(Polygon)
);


ALTER TABLE brownfields.brownfields OWNER TO postgres;

--
-- Name: brownfields_id_seq; Type: SEQUENCE; Schema: brownfields; Owner: postgres
--

CREATE SEQUENCE brownfields.brownfields_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE brownfields.brownfields_id_seq OWNER TO postgres;

--
-- Name: brownfields_id_seq; Type: SEQUENCE OWNED BY; Schema: brownfields; Owner: postgres
--

ALTER SEQUENCE brownfields.brownfields_id_seq OWNED BY brownfields.brownfields.id;


--
-- Name: colors; Type: TABLE; Schema: brownfields; Owner: postgres
--

CREATE TABLE brownfields.colors (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    hex_value character varying(8) NOT NULL
);


ALTER TABLE brownfields.colors OWNER TO postgres;

--
-- Name: colors_id_seq; Type: SEQUENCE; Schema: brownfields; Owner: postgres
--

CREATE SEQUENCE brownfields.colors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE brownfields.colors_id_seq OWNER TO postgres;

--
-- Name: colors_id_seq; Type: SEQUENCE OWNED BY; Schema: brownfields; Owner: postgres
--

ALTER SEQUENCE brownfields.colors_id_seq OWNED BY brownfields.colors.id;


--
-- Name: degradation_levels; Type: TABLE; Schema: brownfields; Owner: postgres
--

CREATE TABLE brownfields.degradation_levels (
    id integer NOT NULL,
    value character varying(256) NOT NULL
);


ALTER TABLE brownfields.degradation_levels OWNER TO postgres;

--
-- Name: degradation_levels_id_seq; Type: SEQUENCE; Schema: brownfields; Owner: postgres
--

CREATE SEQUENCE brownfields.degradation_levels_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE brownfields.degradation_levels_id_seq OWNER TO postgres;

--
-- Name: degradation_levels_id_seq; Type: SEQUENCE OWNED BY; Schema: brownfields; Owner: postgres
--

ALTER SEQUENCE brownfields.degradation_levels_id_seq OWNED BY brownfields.degradation_levels.id;


--
-- Name: economic_potentials; Type: TABLE; Schema: brownfields; Owner: postgres
--

CREATE TABLE brownfields.economic_potentials (
    id integer NOT NULL,
    value character varying(256)
);


ALTER TABLE brownfields.economic_potentials OWNER TO postgres;

--
-- Name: economic_potentials_id_seq; Type: SEQUENCE; Schema: brownfields; Owner: postgres
--

CREATE SEQUENCE brownfields.economic_potentials_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE brownfields.economic_potentials_id_seq OWNER TO postgres;

--
-- Name: economic_potentials_id_seq; Type: SEQUENCE OWNED BY; Schema: brownfields; Owner: postgres
--

ALTER SEQUENCE brownfields.economic_potentials_id_seq OWNED BY brownfields.economic_potentials.id;


--
-- Name: environmental_burden_inclusions; Type: TABLE; Schema: brownfields; Owner: postgres
--

CREATE TABLE brownfields.environmental_burden_inclusions (
    id integer NOT NULL,
    value character varying(256)
);


ALTER TABLE brownfields.environmental_burden_inclusions OWNER TO postgres;

--
-- Name: environmental_burden_inclusions_id_seq; Type: SEQUENCE; Schema: brownfields; Owner: postgres
--

CREATE SEQUENCE brownfields.environmental_burden_inclusions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE brownfields.environmental_burden_inclusions_id_seq OWNER TO postgres;

--
-- Name: environmental_burden_inclusions_id_seq; Type: SEQUENCE OWNED BY; Schema: brownfields; Owner: postgres
--

ALTER SEQUENCE brownfields.environmental_burden_inclusions_id_seq OWNED BY brownfields.environmental_burden_inclusions.id;


--
-- Name: infrastructure_availabilities; Type: TABLE; Schema: brownfields; Owner: postgres
--

CREATE TABLE brownfields.infrastructure_availabilities (
    id integer NOT NULL,
    value character varying(256) NOT NULL
);


ALTER TABLE brownfields.infrastructure_availabilities OWNER TO postgres;

--
-- Name: infrastructure_availabilities_id_seq; Type: SEQUENCE; Schema: brownfields; Owner: postgres
--

CREATE SEQUENCE brownfields.infrastructure_availabilities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE brownfields.infrastructure_availabilities_id_seq OWNER TO postgres;

--
-- Name: infrastructure_availabilities_id_seq; Type: SEQUENCE OWNED BY; Schema: brownfields; Owner: postgres
--

ALTER SEQUENCE brownfields.infrastructure_availabilities_id_seq OWNED BY brownfields.infrastructure_availabilities.id;


--
-- Name: locations; Type: TABLE; Schema: brownfields; Owner: postgres
--

CREATE TABLE brownfields.locations (
    id integer NOT NULL,
    value character varying(256) NOT NULL
);


ALTER TABLE brownfields.locations OWNER TO postgres;

--
-- Name: locations_id_seq; Type: SEQUENCE; Schema: brownfields; Owner: postgres
--

CREATE SEQUENCE brownfields.locations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE brownfields.locations_id_seq OWNER TO postgres;

--
-- Name: locations_id_seq; Type: SEQUENCE OWNED BY; Schema: brownfields; Owner: postgres
--

ALTER SEQUENCE brownfields.locations_id_seq OWNED BY brownfields.locations.id;


--
-- Name: natural_and_architectural_values; Type: TABLE; Schema: brownfields; Owner: postgres
--

CREATE TABLE brownfields.natural_and_architectural_values (
    id integer NOT NULL,
    value character varying(256) NOT NULL
);


ALTER TABLE brownfields.natural_and_architectural_values OWNER TO postgres;

--
-- Name: natural_and_architectural_values_id_seq; Type: SEQUENCE; Schema: brownfields; Owner: postgres
--

CREATE SEQUENCE brownfields.natural_and_architectural_values_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE brownfields.natural_and_architectural_values_id_seq OWNER TO postgres;

--
-- Name: natural_and_architectural_values_id_seq; Type: SEQUENCE OWNED BY; Schema: brownfields; Owner: postgres
--

ALTER SEQUENCE brownfields.natural_and_architectural_values_id_seq OWNED BY brownfields.natural_and_architectural_values.id;


--
-- Name: original_functional_utilizations; Type: TABLE; Schema: brownfields; Owner: postgres
--

CREATE TABLE brownfields.original_functional_utilizations (
    id integer NOT NULL,
    value character varying(256) NOT NULL
);


ALTER TABLE brownfields.original_functional_utilizations OWNER TO postgres;

--
-- Name: original_functional_utilizations_id_seq; Type: SEQUENCE; Schema: brownfields; Owner: postgres
--

CREATE SEQUENCE brownfields.original_functional_utilizations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE brownfields.original_functional_utilizations_id_seq OWNER TO postgres;

--
-- Name: original_functional_utilizations_id_seq; Type: SEQUENCE OWNED BY; Schema: brownfields; Owner: postgres
--

ALTER SEQUENCE brownfields.original_functional_utilizations_id_seq OWNED BY brownfields.original_functional_utilizations.id;


--
-- Name: ownership_types; Type: TABLE; Schema: brownfields; Owner: postgres
--

CREATE TABLE brownfields.ownership_types (
    id integer NOT NULL,
    value character varying(128) NOT NULL
);


ALTER TABLE brownfields.ownership_types OWNER TO postgres;

--
-- Name: ownership_types_id_seq; Type: SEQUENCE; Schema: brownfields; Owner: postgres
--

CREATE SEQUENCE brownfields.ownership_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE brownfields.ownership_types_id_seq OWNER TO postgres;

--
-- Name: ownership_types_id_seq; Type: SEQUENCE OWNED BY; Schema: brownfields; Owner: postgres
--

ALTER SEQUENCE brownfields.ownership_types_id_seq OWNED BY brownfields.ownership_types.id;


--
-- Name: residentional_area_categories; Type: TABLE; Schema: brownfields; Owner: postgres
--

CREATE TABLE brownfields.residentional_area_categories (
    id integer NOT NULL,
    value character varying(256) NOT NULL
);


ALTER TABLE brownfields.residentional_area_categories OWNER TO postgres;

--
-- Name: residentional_area_categories_id_seq; Type: SEQUENCE; Schema: brownfields; Owner: postgres
--

CREATE SEQUENCE brownfields.residentional_area_categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE brownfields.residentional_area_categories_id_seq OWNER TO postgres;

--
-- Name: residentional_area_categories_id_seq; Type: SEQUENCE OWNED BY; Schema: brownfields; Owner: postgres
--

ALTER SEQUENCE brownfields.residentional_area_categories_id_seq OWNED BY brownfields.residentional_area_categories.id;


--
-- Name: revitalizations; Type: TABLE; Schema: brownfields; Owner: postgres
--

CREATE TABLE brownfields.revitalizations (
    id integer NOT NULL,
    value character varying(256) NOT NULL
);


ALTER TABLE brownfields.revitalizations OWNER TO postgres;

--
-- Name: revitalizations_id_seq; Type: SEQUENCE; Schema: brownfields; Owner: postgres
--

CREATE SEQUENCE brownfields.revitalizations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE brownfields.revitalizations_id_seq OWNER TO postgres;

--
-- Name: revitalizations_id_seq; Type: SEQUENCE OWNED BY; Schema: brownfields; Owner: postgres
--

ALTER SEQUENCE brownfields.revitalizations_id_seq OWNED BY brownfields.revitalizations.id;


--
-- Name: settlements; Type: TABLE; Schema: brownfields; Owner: postgres
--

CREATE TABLE brownfields.settlements (
    id integer NOT NULL,
    value character varying(256) NOT NULL
);


ALTER TABLE brownfields.settlements OWNER TO postgres;

--
-- Name: settlements_id_seq; Type: SEQUENCE; Schema: brownfields; Owner: postgres
--

CREATE SEQUENCE brownfields.settlements_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE brownfields.settlements_id_seq OWNER TO postgres;

--
-- Name: settlements_id_seq; Type: SEQUENCE OWNED BY; Schema: brownfields; Owner: postgres
--

ALTER SEQUENCE brownfields.settlements_id_seq OWNED BY brownfields.settlements.id;


--
-- Name: utilizations; Type: TABLE; Schema: brownfields; Owner: postgres
--

CREATE TABLE brownfields.utilizations (
    id integer NOT NULL,
    value character varying(256) NOT NULL
);


ALTER TABLE brownfields.utilizations OWNER TO postgres;

--
-- Name: utilizations_id_seq; Type: SEQUENCE; Schema: brownfields; Owner: postgres
--

CREATE SEQUENCE brownfields.utilizations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE brownfields.utilizations_id_seq OWNER TO postgres;

--
-- Name: utilizations_id_seq; Type: SEQUENCE OWNED BY; Schema: brownfields; Owner: postgres
--

ALTER SEQUENCE brownfields.utilizations_id_seq OWNED BY brownfields.utilizations.id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: permissions id; Type: DEFAULT; Schema: auth; Owner: postgres
--

ALTER TABLE ONLY auth.permissions ALTER COLUMN id SET DEFAULT nextval('auth.permissions_id_seq'::regclass);


--
-- Name: roles id; Type: DEFAULT; Schema: auth; Owner: postgres
--

ALTER TABLE ONLY auth.roles ALTER COLUMN id SET DEFAULT nextval('auth.roles_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: auth; Owner: postgres
--

ALTER TABLE ONLY auth.users ALTER COLUMN id SET DEFAULT nextval('auth.users_id_seq'::regclass);


--
-- Name: area_sizes id; Type: DEFAULT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.area_sizes ALTER COLUMN id SET DEFAULT nextval('brownfields.area_sizes_id_seq'::regclass);


--
-- Name: brownfields id; Type: DEFAULT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.brownfields ALTER COLUMN id SET DEFAULT nextval('brownfields.brownfields_id_seq'::regclass);


--
-- Name: colors id; Type: DEFAULT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.colors ALTER COLUMN id SET DEFAULT nextval('brownfields.colors_id_seq'::regclass);


--
-- Name: degradation_levels id; Type: DEFAULT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.degradation_levels ALTER COLUMN id SET DEFAULT nextval('brownfields.degradation_levels_id_seq'::regclass);


--
-- Name: economic_potentials id; Type: DEFAULT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.economic_potentials ALTER COLUMN id SET DEFAULT nextval('brownfields.economic_potentials_id_seq'::regclass);


--
-- Name: environmental_burden_inclusions id; Type: DEFAULT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.environmental_burden_inclusions ALTER COLUMN id SET DEFAULT nextval('brownfields.environmental_burden_inclusions_id_seq'::regclass);


--
-- Name: infrastructure_availabilities id; Type: DEFAULT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.infrastructure_availabilities ALTER COLUMN id SET DEFAULT nextval('brownfields.infrastructure_availabilities_id_seq'::regclass);


--
-- Name: locations id; Type: DEFAULT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.locations ALTER COLUMN id SET DEFAULT nextval('brownfields.locations_id_seq'::regclass);


--
-- Name: natural_and_architectural_values id; Type: DEFAULT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.natural_and_architectural_values ALTER COLUMN id SET DEFAULT nextval('brownfields.natural_and_architectural_values_id_seq'::regclass);


--
-- Name: original_functional_utilizations id; Type: DEFAULT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.original_functional_utilizations ALTER COLUMN id SET DEFAULT nextval('brownfields.original_functional_utilizations_id_seq'::regclass);


--
-- Name: ownership_types id; Type: DEFAULT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.ownership_types ALTER COLUMN id SET DEFAULT nextval('brownfields.ownership_types_id_seq'::regclass);


--
-- Name: residentional_area_categories id; Type: DEFAULT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.residentional_area_categories ALTER COLUMN id SET DEFAULT nextval('brownfields.residentional_area_categories_id_seq'::regclass);


--
-- Name: revitalizations id; Type: DEFAULT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.revitalizations ALTER COLUMN id SET DEFAULT nextval('brownfields.revitalizations_id_seq'::regclass);


--
-- Name: settlements id; Type: DEFAULT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.settlements ALTER COLUMN id SET DEFAULT nextval('brownfields.settlements_id_seq'::regclass);


--
-- Name: utilizations id; Type: DEFAULT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.utilizations ALTER COLUMN id SET DEFAULT nextval('brownfields.utilizations_id_seq'::regclass);


--
-- Name: permissions permissions_name_key; Type: CONSTRAINT; Schema: auth; Owner: postgres
--

ALTER TABLE ONLY auth.permissions
    ADD CONSTRAINT permissions_name_key UNIQUE (name);


--
-- Name: permissions permissions_pkey; Type: CONSTRAINT; Schema: auth; Owner: postgres
--

ALTER TABLE ONLY auth.permissions
    ADD CONSTRAINT permissions_pkey PRIMARY KEY (id);


--
-- Name: role_permissions role_permissions_pkey; Type: CONSTRAINT; Schema: auth; Owner: postgres
--

ALTER TABLE ONLY auth.role_permissions
    ADD CONSTRAINT role_permissions_pkey PRIMARY KEY (permission_id, role_id);


--
-- Name: roles roles_name_key; Type: CONSTRAINT; Schema: auth; Owner: postgres
--

ALTER TABLE ONLY auth.roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: auth; Owner: postgres
--

ALTER TABLE ONLY auth.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: user_roles user_roles_pkey; Type: CONSTRAINT; Schema: auth; Owner: postgres
--

ALTER TABLE ONLY auth.user_roles
    ADD CONSTRAINT user_roles_pkey PRIMARY KEY (user_id, role_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: auth; Owner: postgres
--

ALTER TABLE ONLY auth.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: area_sizes area_sizes_pkey; Type: CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.area_sizes
    ADD CONSTRAINT area_sizes_pkey PRIMARY KEY (id);


--
-- Name: area_sizes area_sizes_value_key; Type: CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.area_sizes
    ADD CONSTRAINT area_sizes_value_key UNIQUE (value);


--
-- Name: brownfields brownfields_pkey; Type: CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.brownfields
    ADD CONSTRAINT brownfields_pkey PRIMARY KEY (id);


--
-- Name: colors colors_name_key; Type: CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.colors
    ADD CONSTRAINT colors_name_key UNIQUE (name);


--
-- Name: colors colors_pkey; Type: CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.colors
    ADD CONSTRAINT colors_pkey PRIMARY KEY (id);


--
-- Name: degradation_levels degradation_levels_pkey; Type: CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.degradation_levels
    ADD CONSTRAINT degradation_levels_pkey PRIMARY KEY (id);


--
-- Name: degradation_levels degradation_levels_value_key; Type: CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.degradation_levels
    ADD CONSTRAINT degradation_levels_value_key UNIQUE (value);


--
-- Name: economic_potentials economic_potentials_pkey; Type: CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.economic_potentials
    ADD CONSTRAINT economic_potentials_pkey PRIMARY KEY (id);


--
-- Name: economic_potentials economic_potentials_value_key; Type: CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.economic_potentials
    ADD CONSTRAINT economic_potentials_value_key UNIQUE (value);


--
-- Name: environmental_burden_inclusions environmental_burden_inclusions_pkey; Type: CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.environmental_burden_inclusions
    ADD CONSTRAINT environmental_burden_inclusions_pkey PRIMARY KEY (id);


--
-- Name: environmental_burden_inclusions environmental_burden_inclusions_value_key; Type: CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.environmental_burden_inclusions
    ADD CONSTRAINT environmental_burden_inclusions_value_key UNIQUE (value);


--
-- Name: infrastructure_availabilities infrastructure_availabilities_pkey; Type: CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.infrastructure_availabilities
    ADD CONSTRAINT infrastructure_availabilities_pkey PRIMARY KEY (id);


--
-- Name: infrastructure_availabilities infrastructure_availabilities_value_key; Type: CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.infrastructure_availabilities
    ADD CONSTRAINT infrastructure_availabilities_value_key UNIQUE (value);


--
-- Name: locations locations_pkey; Type: CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.locations
    ADD CONSTRAINT locations_pkey PRIMARY KEY (id);


--
-- Name: locations locations_value_key; Type: CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.locations
    ADD CONSTRAINT locations_value_key UNIQUE (value);


--
-- Name: natural_and_architectural_values natural_and_architectural_values_pkey; Type: CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.natural_and_architectural_values
    ADD CONSTRAINT natural_and_architectural_values_pkey PRIMARY KEY (id);


--
-- Name: natural_and_architectural_values natural_and_architectural_values_value_key; Type: CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.natural_and_architectural_values
    ADD CONSTRAINT natural_and_architectural_values_value_key UNIQUE (value);


--
-- Name: original_functional_utilizations original_functional_utilizations_pkey; Type: CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.original_functional_utilizations
    ADD CONSTRAINT original_functional_utilizations_pkey PRIMARY KEY (id);


--
-- Name: original_functional_utilizations original_functional_utilizations_value_key; Type: CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.original_functional_utilizations
    ADD CONSTRAINT original_functional_utilizations_value_key UNIQUE (value);


--
-- Name: ownership_types ownership_types_pkey; Type: CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.ownership_types
    ADD CONSTRAINT ownership_types_pkey PRIMARY KEY (id);


--
-- Name: ownership_types ownership_types_value_key; Type: CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.ownership_types
    ADD CONSTRAINT ownership_types_value_key UNIQUE (value);


--
-- Name: residentional_area_categories residentional_area_categories_pkey; Type: CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.residentional_area_categories
    ADD CONSTRAINT residentional_area_categories_pkey PRIMARY KEY (id);


--
-- Name: residentional_area_categories residentional_area_categories_value_key; Type: CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.residentional_area_categories
    ADD CONSTRAINT residentional_area_categories_value_key UNIQUE (value);


--
-- Name: revitalizations revitalizations_pkey; Type: CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.revitalizations
    ADD CONSTRAINT revitalizations_pkey PRIMARY KEY (id);


--
-- Name: revitalizations revitalizations_value_key; Type: CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.revitalizations
    ADD CONSTRAINT revitalizations_value_key UNIQUE (value);


--
-- Name: settlements settlements_pkey; Type: CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.settlements
    ADD CONSTRAINT settlements_pkey PRIMARY KEY (id);


--
-- Name: settlements settlements_value_key; Type: CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.settlements
    ADD CONSTRAINT settlements_value_key UNIQUE (value);


--
-- Name: utilizations utilizations_pkey; Type: CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.utilizations
    ADD CONSTRAINT utilizations_pkey PRIMARY KEY (id);


--
-- Name: utilizations utilizations_value_key; Type: CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.utilizations
    ADD CONSTRAINT utilizations_value_key UNIQUE (value);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: ix_auth_permissions_id; Type: INDEX; Schema: auth; Owner: postgres
--

CREATE INDEX ix_auth_permissions_id ON auth.permissions USING btree (id);


--
-- Name: ix_auth_roles_id; Type: INDEX; Schema: auth; Owner: postgres
--

CREATE INDEX ix_auth_roles_id ON auth.roles USING btree (id);


--
-- Name: ix_auth_users_email; Type: INDEX; Schema: auth; Owner: postgres
--

CREATE UNIQUE INDEX ix_auth_users_email ON auth.users USING btree (email);


--
-- Name: ix_auth_users_id; Type: INDEX; Schema: auth; Owner: postgres
--

CREATE INDEX ix_auth_users_id ON auth.users USING btree (id);


--
-- Name: ix_auth_users_last_session; Type: INDEX; Schema: auth; Owner: postgres
--

CREATE UNIQUE INDEX ix_auth_users_last_session ON auth.users USING btree (last_session);


--
-- Name: idx_brownfields_polygon; Type: INDEX; Schema: brownfields; Owner: postgres
--

CREATE INDEX idx_brownfields_polygon ON brownfields.brownfields USING gist (polygon);


--
-- Name: ix_brownfields_area_sizes_id; Type: INDEX; Schema: brownfields; Owner: postgres
--

CREATE INDEX ix_brownfields_area_sizes_id ON brownfields.area_sizes USING btree (id);


--
-- Name: ix_brownfields_brownfields_id; Type: INDEX; Schema: brownfields; Owner: postgres
--

CREATE INDEX ix_brownfields_brownfields_id ON brownfields.brownfields USING btree (id);


--
-- Name: ix_brownfields_brownfields_image_directory_uuid; Type: INDEX; Schema: brownfields; Owner: postgres
--

CREATE INDEX ix_brownfields_brownfields_image_directory_uuid ON brownfields.brownfields USING btree (image_directory_uuid);


--
-- Name: ix_brownfields_colors_id; Type: INDEX; Schema: brownfields; Owner: postgres
--

CREATE INDEX ix_brownfields_colors_id ON brownfields.colors USING btree (id);


--
-- Name: ix_brownfields_degradation_levels_id; Type: INDEX; Schema: brownfields; Owner: postgres
--

CREATE INDEX ix_brownfields_degradation_levels_id ON brownfields.degradation_levels USING btree (id);


--
-- Name: ix_brownfields_economic_potentials_id; Type: INDEX; Schema: brownfields; Owner: postgres
--

CREATE INDEX ix_brownfields_economic_potentials_id ON brownfields.economic_potentials USING btree (id);


--
-- Name: ix_brownfields_environmental_burden_inclusions_id; Type: INDEX; Schema: brownfields; Owner: postgres
--

CREATE INDEX ix_brownfields_environmental_burden_inclusions_id ON brownfields.environmental_burden_inclusions USING btree (id);


--
-- Name: ix_brownfields_infrastructure_availabilities_id; Type: INDEX; Schema: brownfields; Owner: postgres
--

CREATE INDEX ix_brownfields_infrastructure_availabilities_id ON brownfields.infrastructure_availabilities USING btree (id);


--
-- Name: ix_brownfields_locations_id; Type: INDEX; Schema: brownfields; Owner: postgres
--

CREATE INDEX ix_brownfields_locations_id ON brownfields.locations USING btree (id);


--
-- Name: ix_brownfields_natural_and_architectural_values_id; Type: INDEX; Schema: brownfields; Owner: postgres
--

CREATE INDEX ix_brownfields_natural_and_architectural_values_id ON brownfields.natural_and_architectural_values USING btree (id);


--
-- Name: ix_brownfields_original_functional_utilizations_id; Type: INDEX; Schema: brownfields; Owner: postgres
--

CREATE INDEX ix_brownfields_original_functional_utilizations_id ON brownfields.original_functional_utilizations USING btree (id);


--
-- Name: ix_brownfields_ownership_types_id; Type: INDEX; Schema: brownfields; Owner: postgres
--

CREATE INDEX ix_brownfields_ownership_types_id ON brownfields.ownership_types USING btree (id);


--
-- Name: ix_brownfields_residentional_area_categories_id; Type: INDEX; Schema: brownfields; Owner: postgres
--

CREATE INDEX ix_brownfields_residentional_area_categories_id ON brownfields.residentional_area_categories USING btree (id);


--
-- Name: ix_brownfields_revitalizations_id; Type: INDEX; Schema: brownfields; Owner: postgres
--

CREATE INDEX ix_brownfields_revitalizations_id ON brownfields.revitalizations USING btree (id);


--
-- Name: ix_brownfields_settlements_id; Type: INDEX; Schema: brownfields; Owner: postgres
--

CREATE INDEX ix_brownfields_settlements_id ON brownfields.settlements USING btree (id);


--
-- Name: ix_brownfields_utilizations_id; Type: INDEX; Schema: brownfields; Owner: postgres
--

CREATE INDEX ix_brownfields_utilizations_id ON brownfields.utilizations USING btree (id);


--
-- Name: role_permissions role_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: postgres
--

ALTER TABLE ONLY auth.role_permissions
    ADD CONSTRAINT role_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth.permissions(id);


--
-- Name: role_permissions role_permissions_role_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: postgres
--

ALTER TABLE ONLY auth.role_permissions
    ADD CONSTRAINT role_permissions_role_id_fkey FOREIGN KEY (role_id) REFERENCES auth.roles(id);


--
-- Name: user_roles user_roles_role_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: postgres
--

ALTER TABLE ONLY auth.user_roles
    ADD CONSTRAINT user_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES auth.roles(id);


--
-- Name: user_roles user_roles_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: postgres
--

ALTER TABLE ONLY auth.user_roles
    ADD CONSTRAINT user_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id);


--
-- Name: brownfields brownfields_area_size_id_fkey; Type: FK CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.brownfields
    ADD CONSTRAINT brownfields_area_size_id_fkey FOREIGN KEY (area_size_id) REFERENCES brownfields.area_sizes(id);


--
-- Name: brownfields brownfields_color_id_fkey; Type: FK CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.brownfields
    ADD CONSTRAINT brownfields_color_id_fkey FOREIGN KEY (color_id) REFERENCES brownfields.colors(id);


--
-- Name: brownfields brownfields_degradation_level_id_fkey; Type: FK CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.brownfields
    ADD CONSTRAINT brownfields_degradation_level_id_fkey FOREIGN KEY (degradation_level_id) REFERENCES brownfields.degradation_levels(id);


--
-- Name: brownfields brownfields_economic_potential_id_fkey; Type: FK CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.brownfields
    ADD CONSTRAINT brownfields_economic_potential_id_fkey FOREIGN KEY (economic_potential_id) REFERENCES brownfields.economic_potentials(id);


--
-- Name: brownfields brownfields_environmental_burden_inclusion_id_fkey; Type: FK CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.brownfields
    ADD CONSTRAINT brownfields_environmental_burden_inclusion_id_fkey FOREIGN KEY (environmental_burden_inclusion_id) REFERENCES brownfields.environmental_burden_inclusions(id);


--
-- Name: brownfields brownfields_infrastructure_availability_id_fkey; Type: FK CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.brownfields
    ADD CONSTRAINT brownfields_infrastructure_availability_id_fkey FOREIGN KEY (infrastructure_availability_id) REFERENCES brownfields.infrastructure_availabilities(id);


--
-- Name: brownfields brownfields_location_id_fkey; Type: FK CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.brownfields
    ADD CONSTRAINT brownfields_location_id_fkey FOREIGN KEY (location_id) REFERENCES brownfields.locations(id);


--
-- Name: brownfields brownfields_natural_and_architectural_value_id_fkey; Type: FK CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.brownfields
    ADD CONSTRAINT brownfields_natural_and_architectural_value_id_fkey FOREIGN KEY (natural_and_architectural_value_id) REFERENCES brownfields.natural_and_architectural_values(id);


--
-- Name: brownfields brownfields_original_functional_utilization_id_fkey; Type: FK CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.brownfields
    ADD CONSTRAINT brownfields_original_functional_utilization_id_fkey FOREIGN KEY (original_functional_utilization_id) REFERENCES brownfields.original_functional_utilizations(id);


--
-- Name: brownfields brownfields_ownership_type_id_fkey; Type: FK CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.brownfields
    ADD CONSTRAINT brownfields_ownership_type_id_fkey FOREIGN KEY (ownership_type_id) REFERENCES brownfields.ownership_types(id);


--
-- Name: brownfields brownfields_residentional_area_category_id_fkey; Type: FK CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.brownfields
    ADD CONSTRAINT brownfields_residentional_area_category_id_fkey FOREIGN KEY (residentional_area_category_id) REFERENCES brownfields.residentional_area_categories(id);


--
-- Name: brownfields brownfields_revitalization_id_fkey; Type: FK CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.brownfields
    ADD CONSTRAINT brownfields_revitalization_id_fkey FOREIGN KEY (revitalization_id) REFERENCES brownfields.revitalizations(id);


--
-- Name: brownfields brownfields_settlement_id_fkey; Type: FK CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.brownfields
    ADD CONSTRAINT brownfields_settlement_id_fkey FOREIGN KEY (settlement_id) REFERENCES brownfields.settlements(id);


--
-- Name: brownfields brownfields_utilization_id_fkey; Type: FK CONSTRAINT; Schema: brownfields; Owner: postgres
--

ALTER TABLE ONLY brownfields.brownfields
    ADD CONSTRAINT brownfields_utilization_id_fkey FOREIGN KEY (utilization_id) REFERENCES brownfields.utilizations(id);


--
-- PostgreSQL database dump complete
--

