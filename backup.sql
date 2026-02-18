pg_dump: warning: there are circular foreign-key constraints on this table:
pg_dump: detail: hypertable
pg_dump: hint: You might not be able to restore the dump without using --disable-triggers or temporarily dropping the constraints.
pg_dump: hint: Consider using a full dump instead of a --data-only dump to avoid this problem.
pg_dump: warning: there are circular foreign-key constraints on this table:
pg_dump: detail: chunk
pg_dump: hint: You might not be able to restore the dump without using --disable-triggers or temporarily dropping the constraints.
pg_dump: hint: Consider using a full dump instead of a --data-only dump to avoid this problem.
pg_dump: warning: there are circular foreign-key constraints on this table:
pg_dump: detail: continuous_agg
pg_dump: hint: You might not be able to restore the dump without using --disable-triggers or temporarily dropping the constraints.
pg_dump: hint: Consider using a full dump instead of a --data-only dump to avoid this problem.
--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13
-- Dumped by pg_dump version 15.13

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
-- Name: timescaledb; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS timescaledb WITH SCHEMA public;


--
-- Name: EXTENSION timescaledb; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION timescaledb IS 'Enables scalable inserts and complex queries for time-series data (Community Edition)';


--
-- Name: codemethod; Type: TYPE; Schema: public; Owner: wifi_user
--

CREATE TYPE public.codemethod AS ENUM (
    'SMS',
    'CALL'
);


ALTER TYPE public.codemethod OWNER TO wifi_user;

--
-- Name: crmprovidertype; Type: TYPE; Schema: public; Owner: wifi_user
--

CREATE TYPE public.crmprovidertype AS ENUM (
    'BITRIX24'
);


ALTER TYPE public.crmprovidertype OWNER TO wifi_user;

--
-- Name: nasdevicetype; Type: TYPE; Schema: public; Owner: wifi_user
--

CREATE TYPE public.nasdevicetype AS ENUM (
    'MIKROTIK',
    'OPENWRT',
    'UBIQUITI'
);


ALTER TYPE public.nasdevicetype OWNER TO wifi_user;

--
-- Name: smsprovidertype; Type: TYPE; Schema: public; Owner: wifi_user
--

CREATE TYPE public.smsprovidertype AS ENUM (
    'ROCKETSMS',
    'CALLPASSWORD',
    'WEBSMS'
);


ALTER TYPE public.smsprovidertype OWNER TO wifi_user;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: wifi_user
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO wifi_user;

--
-- Name: audit_logs; Type: TABLE; Schema: public; Owner: wifi_user
--

CREATE TABLE public.audit_logs (
    user_id integer,
    action character varying NOT NULL,
    resource_type character varying NOT NULL,
    resource_id integer,
    details json,
    ip_address character varying(45),
    created_at timestamp with time zone DEFAULT now(),
    id integer NOT NULL,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.audit_logs OWNER TO wifi_user;

--
-- Name: audit_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: wifi_user
--

CREATE SEQUENCE public.audit_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.audit_logs_id_seq OWNER TO wifi_user;

--
-- Name: audit_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wifi_user
--

ALTER SEQUENCE public.audit_logs_id_seq OWNED BY public.audit_logs.id;


--
-- Name: banners; Type: TABLE; Schema: public; Owner: wifi_user
--

CREATE TABLE public.banners (
    venue_id integer NOT NULL,
    image_url character varying,
    target_url character varying NOT NULL,
    clicks_count integer,
    impressions_count integer,
    is_active boolean,
    id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.banners OWNER TO wifi_user;

--
-- Name: banners_id_seq; Type: SEQUENCE; Schema: public; Owner: wifi_user
--

CREATE SEQUENCE public.banners_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.banners_id_seq OWNER TO wifi_user;

--
-- Name: banners_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wifi_user
--

ALTER SEQUENCE public.banners_id_seq OWNED BY public.banners.id;


--
-- Name: crm_providers; Type: TABLE; Schema: public; Owner: wifi_user
--

CREATE TABLE public.crm_providers (
    id integer NOT NULL,
    name character varying NOT NULL,
    type character varying NOT NULL,
    config json DEFAULT '{}'::json NOT NULL,
    is_active boolean DEFAULT true,
    priority integer DEFAULT 0,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    CONSTRAINT crm_providers_type_check CHECK (((type)::text = 'BITRIX24'::text))
);


ALTER TABLE public.crm_providers OWNER TO wifi_user;

--
-- Name: crm_providers_id_seq; Type: SEQUENCE; Schema: public; Owner: wifi_user
--

CREATE SEQUENCE public.crm_providers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.crm_providers_id_seq OWNER TO wifi_user;

--
-- Name: crm_providers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wifi_user
--

ALTER SEQUENCE public.crm_providers_id_seq OWNED BY public.crm_providers.id;


--
-- Name: events; Type: TABLE; Schema: public; Owner: wifi_user
--

CREATE TABLE public.events (
    user_profile_id integer,
    venue_id integer NOT NULL,
    type character varying NOT NULL,
    data json,
    created_at timestamp with time zone DEFAULT now(),
    id integer NOT NULL,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.events OWNER TO wifi_user;

--
-- Name: events_id_seq; Type: SEQUENCE; Schema: public; Owner: wifi_user
--

CREATE SEQUENCE public.events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.events_id_seq OWNER TO wifi_user;

--
-- Name: events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wifi_user
--

ALTER SEQUENCE public.events_id_seq OWNED BY public.events.id;


--
-- Name: local_users; Type: TABLE; Schema: public; Owner: wifi_user
--

CREATE TABLE public.local_users (
    username character varying NOT NULL,
    password_hash character varying NOT NULL,
    venue_id integer NOT NULL,
    user_profile_id integer,
    is_active boolean,
    id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.local_users OWNER TO wifi_user;

--
-- Name: local_users_id_seq; Type: SEQUENCE; Schema: public; Owner: wifi_user
--

CREATE SEQUENCE public.local_users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.local_users_id_seq OWNER TO wifi_user;

--
-- Name: local_users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wifi_user
--

ALTER SEQUENCE public.local_users_id_seq OWNED BY public.local_users.id;


--
-- Name: nas_devices; Type: TABLE; Schema: public; Owner: wifi_user
--

CREATE TABLE public.nas_devices (
    id integer NOT NULL,
    venue_id integer NOT NULL,
    name character varying NOT NULL,
    type public.nasdevicetype NOT NULL,
    ip_address character varying NOT NULL,
    secret bytea NOT NULL,
    api_username character varying,
    api_password bytea,
    wireguard_pubkey character varying,
    wireguard_ip character varying,
    is_active boolean,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    last_seen timestamp with time zone,
    status character varying,
    last_check timestamp with time zone,
    config json
);


ALTER TABLE public.nas_devices OWNER TO wifi_user;

--
-- Name: nas_devices_id_seq; Type: SEQUENCE; Schema: public; Owner: wifi_user
--

CREATE SEQUENCE public.nas_devices_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.nas_devices_id_seq OWNER TO wifi_user;

--
-- Name: nas_devices_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wifi_user
--

ALTER SEQUENCE public.nas_devices_id_seq OWNED BY public.nas_devices.id;


--
-- Name: nas_status_history; Type: TABLE; Schema: public; Owner: wifi_user
--

CREATE TABLE public.nas_status_history (
    nas_device_id integer NOT NULL,
    status character varying NOT NULL,
    checked_at timestamp with time zone DEFAULT now(),
    id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.nas_status_history OWNER TO wifi_user;

--
-- Name: nas_status_history_id_seq; Type: SEQUENCE; Schema: public; Owner: wifi_user
--

CREATE SEQUENCE public.nas_status_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.nas_status_history_id_seq OWNER TO wifi_user;

--
-- Name: nas_status_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wifi_user
--

ALTER SEQUENCE public.nas_status_history_id_seq OWNED BY public.nas_status_history.id;


--
-- Name: netflow_records; Type: TABLE; Schema: public; Owner: wifi_user
--

CREATE TABLE public.netflow_records (
    "time" timestamp with time zone DEFAULT now() NOT NULL,
    session_id integer,
    src_ip character varying(45) NOT NULL,
    dst_ip character varying(45) NOT NULL,
    bytes bigint NOT NULL,
    packets bigint NOT NULL,
    src_port integer,
    dst_port integer,
    protocol integer,
    flow_start timestamp with time zone,
    flow_end timestamp with time zone,
    id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.netflow_records OWNER TO wifi_user;

--
-- Name: netflow_records_id_seq; Type: SEQUENCE; Schema: public; Owner: wifi_user
--

CREATE SEQUENCE public.netflow_records_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.netflow_records_id_seq OWNER TO wifi_user;

--
-- Name: netflow_records_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wifi_user
--

ALTER SEQUENCE public.netflow_records_id_seq OWNED BY public.netflow_records.id;


--
-- Name: portal_templates; Type: TABLE; Schema: public; Owner: wifi_user
--

CREATE TABLE public.portal_templates (
    venue_id integer NOT NULL,
    type character varying NOT NULL,
    html_content text NOT NULL,
    css_files json,
    js_files json,
    images json,
    is_active boolean,
    id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.portal_templates OWNER TO wifi_user;

--
-- Name: portal_templates_id_seq; Type: SEQUENCE; Schema: public; Owner: wifi_user
--

CREATE SEQUENCE public.portal_templates_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.portal_templates_id_seq OWNER TO wifi_user;

--
-- Name: portal_templates_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wifi_user
--

ALTER SEQUENCE public.portal_templates_id_seq OWNED BY public.portal_templates.id;


--
-- Name: sessions; Type: TABLE; Schema: public; Owner: wifi_user
--

CREATE TABLE public.sessions (
    user_profile_id integer,
    venue_id integer NOT NULL,
    nas_id integer NOT NULL,
    mac_address character varying(17) NOT NULL,
    ip_address character varying(45),
    session_start timestamp with time zone DEFAULT now(),
    session_end timestamp with time zone,
    traffic_in_bytes bigint,
    traffic_out_bytes bigint,
    is_active boolean,
    id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.sessions OWNER TO wifi_user;

--
-- Name: sessions_id_seq; Type: SEQUENCE; Schema: public; Owner: wifi_user
--

CREATE SEQUENCE public.sessions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sessions_id_seq OWNER TO wifi_user;

--
-- Name: sessions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wifi_user
--

ALTER SEQUENCE public.sessions_id_seq OWNED BY public.sessions.id;


--
-- Name: settings; Type: TABLE; Schema: public; Owner: wifi_user
--

CREATE TABLE public.settings (
    id integer NOT NULL,
    key character varying NOT NULL,
    value text,
    description character varying,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.settings OWNER TO wifi_user;

--
-- Name: settings_id_seq; Type: SEQUENCE; Schema: public; Owner: wifi_user
--

CREATE SEQUENCE public.settings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.settings_id_seq OWNER TO wifi_user;

--
-- Name: settings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wifi_user
--

ALTER SEQUENCE public.settings_id_seq OWNED BY public.settings.id;


--
-- Name: sms_codes; Type: TABLE; Schema: public; Owner: wifi_user
--

CREATE TABLE public.sms_codes (
    phone_number character varying(15) NOT NULL,
    code character varying(6) NOT NULL,
    is_used boolean,
    expires_at timestamp with time zone NOT NULL,
    attempts integer,
    id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    venue_id integer,
    method public.codemethod DEFAULT 'SMS'::public.codemethod NOT NULL,
    call_id character varying,
    provider_id integer
);


ALTER TABLE public.sms_codes OWNER TO wifi_user;

--
-- Name: sms_codes_id_seq; Type: SEQUENCE; Schema: public; Owner: wifi_user
--

CREATE SEQUENCE public.sms_codes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sms_codes_id_seq OWNER TO wifi_user;

--
-- Name: sms_codes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wifi_user
--

ALTER SEQUENCE public.sms_codes_id_seq OWNED BY public.sms_codes.id;


--
-- Name: sms_providers; Type: TABLE; Schema: public; Owner: wifi_user
--

CREATE TABLE public.sms_providers (
    name character varying NOT NULL,
    is_active boolean,
    config json NOT NULL,
    id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    type public.smsprovidertype DEFAULT 'ROCKETSMS'::public.smsprovidertype NOT NULL,
    priority integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.sms_providers OWNER TO wifi_user;

--
-- Name: sms_providers_id_seq; Type: SEQUENCE; Schema: public; Owner: wifi_user
--

CREATE SEQUENCE public.sms_providers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sms_providers_id_seq OWNER TO wifi_user;

--
-- Name: sms_providers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wifi_user
--

ALTER SEQUENCE public.sms_providers_id_seq OWNED BY public.sms_providers.id;


--
-- Name: tariff_plans; Type: TABLE; Schema: public; Owner: wifi_user
--

CREATE TABLE public.tariff_plans (
    id integer NOT NULL,
    name character varying NOT NULL,
    description character varying,
    price double precision NOT NULL,
    currency character varying NOT NULL,
    duration_hours integer NOT NULL,
    speed_limit_up_kbps integer,
    speed_limit_down_kbps integer,
    is_active boolean,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.tariff_plans OWNER TO wifi_user;

--
-- Name: tariff_plans_id_seq; Type: SEQUENCE; Schema: public; Owner: wifi_user
--

CREATE SEQUENCE public.tariff_plans_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tariff_plans_id_seq OWNER TO wifi_user;

--
-- Name: tariff_plans_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wifi_user
--

ALTER SEQUENCE public.tariff_plans_id_seq OWNED BY public.tariff_plans.id;


--
-- Name: user_profiles; Type: TABLE; Schema: public; Owner: wifi_user
--

CREATE TABLE public.user_profiles (
    mac_address character varying(17) NOT NULL,
    phone_number character varying(15),
    email character varying,
    first_seen timestamp with time zone DEFAULT now(),
    last_seen timestamp with time zone,
    total_sessions integer,
    total_traffic_bytes bigint,
    is_blocked boolean,
    is_vip boolean,
    device_oui character varying(8),
    id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    venue_id integer,
    current_tariff_id integer,
    tariff_expires_at timestamp with time zone,
    full_name character varying,
    marketing_consent boolean DEFAULT false NOT NULL
);


ALTER TABLE public.user_profiles OWNER TO wifi_user;

--
-- Name: user_profiles_id_seq; Type: SEQUENCE; Schema: public; Owner: wifi_user
--

CREATE SEQUENCE public.user_profiles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_profiles_id_seq OWNER TO wifi_user;

--
-- Name: user_profiles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wifi_user
--

ALTER SEQUENCE public.user_profiles_id_seq OWNED BY public.user_profiles.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: wifi_user
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying NOT NULL,
    hashed_password character varying NOT NULL,
    is_active boolean,
    is_superuser boolean,
    role character varying,
    created_at timestamp with time zone DEFAULT now(),
    venue_id integer
);


ALTER TABLE public.users OWNER TO wifi_user;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: wifi_user
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO wifi_user;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wifi_user
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: venue_crm; Type: TABLE; Schema: public; Owner: wifi_user
--

CREATE TABLE public.venue_crm (
    venue_id integer NOT NULL,
    crm_provider_id integer NOT NULL,
    is_active boolean DEFAULT true,
    config_override json,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.venue_crm OWNER TO wifi_user;

--
-- Name: venue_tariff; Type: TABLE; Schema: public; Owner: wifi_user
--

CREATE TABLE public.venue_tariff (
    venue_id integer NOT NULL,
    tariff_id integer NOT NULL,
    priority integer DEFAULT 0 NOT NULL,
    is_available boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.venue_tariff OWNER TO wifi_user;

--
-- Name: venues; Type: TABLE; Schema: public; Owner: wifi_user
--

CREATE TABLE public.venues (
    id integer NOT NULL,
    name character varying NOT NULL,
    description character varying,
    address character varying,
    contact_phone character varying,
    contact_email character varying,
    is_active boolean,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    domain character varying,
    ssl_enabled boolean
);


ALTER TABLE public.venues OWNER TO wifi_user;

--
-- Name: venues_id_seq; Type: SEQUENCE; Schema: public; Owner: wifi_user
--

CREATE SEQUENCE public.venues_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.venues_id_seq OWNER TO wifi_user;

--
-- Name: venues_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wifi_user
--

ALTER SEQUENCE public.venues_id_seq OWNED BY public.venues.id;


--
-- Name: wireguard_peers; Type: TABLE; Schema: public; Owner: wifi_user
--

CREATE TABLE public.wireguard_peers (
    nas_device_id integer NOT NULL,
    public_key character varying NOT NULL,
    allowed_ips character varying NOT NULL,
    endpoint character varying,
    is_active boolean,
    id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.wireguard_peers OWNER TO wifi_user;

--
-- Name: wireguard_peers_id_seq; Type: SEQUENCE; Schema: public; Owner: wifi_user
--

CREATE SEQUENCE public.wireguard_peers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wireguard_peers_id_seq OWNER TO wifi_user;

--
-- Name: wireguard_peers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wifi_user
--

ALTER SEQUENCE public.wireguard_peers_id_seq OWNED BY public.wireguard_peers.id;


--
-- Name: audit_logs id; Type: DEFAULT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.audit_logs ALTER COLUMN id SET DEFAULT nextval('public.audit_logs_id_seq'::regclass);


--
-- Name: banners id; Type: DEFAULT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.banners ALTER COLUMN id SET DEFAULT nextval('public.banners_id_seq'::regclass);


--
-- Name: crm_providers id; Type: DEFAULT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.crm_providers ALTER COLUMN id SET DEFAULT nextval('public.crm_providers_id_seq'::regclass);


--
-- Name: events id; Type: DEFAULT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.events ALTER COLUMN id SET DEFAULT nextval('public.events_id_seq'::regclass);


--
-- Name: local_users id; Type: DEFAULT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.local_users ALTER COLUMN id SET DEFAULT nextval('public.local_users_id_seq'::regclass);


--
-- Name: nas_devices id; Type: DEFAULT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.nas_devices ALTER COLUMN id SET DEFAULT nextval('public.nas_devices_id_seq'::regclass);


--
-- Name: nas_status_history id; Type: DEFAULT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.nas_status_history ALTER COLUMN id SET DEFAULT nextval('public.nas_status_history_id_seq'::regclass);


--
-- Name: netflow_records id; Type: DEFAULT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.netflow_records ALTER COLUMN id SET DEFAULT nextval('public.netflow_records_id_seq'::regclass);


--
-- Name: portal_templates id; Type: DEFAULT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.portal_templates ALTER COLUMN id SET DEFAULT nextval('public.portal_templates_id_seq'::regclass);


--
-- Name: sessions id; Type: DEFAULT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.sessions ALTER COLUMN id SET DEFAULT nextval('public.sessions_id_seq'::regclass);


--
-- Name: settings id; Type: DEFAULT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.settings ALTER COLUMN id SET DEFAULT nextval('public.settings_id_seq'::regclass);


--
-- Name: sms_codes id; Type: DEFAULT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.sms_codes ALTER COLUMN id SET DEFAULT nextval('public.sms_codes_id_seq'::regclass);


--
-- Name: sms_providers id; Type: DEFAULT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.sms_providers ALTER COLUMN id SET DEFAULT nextval('public.sms_providers_id_seq'::regclass);


--
-- Name: tariff_plans id; Type: DEFAULT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.tariff_plans ALTER COLUMN id SET DEFAULT nextval('public.tariff_plans_id_seq'::regclass);


--
-- Name: user_profiles id; Type: DEFAULT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.user_profiles ALTER COLUMN id SET DEFAULT nextval('public.user_profiles_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: venues id; Type: DEFAULT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.venues ALTER COLUMN id SET DEFAULT nextval('public.venues_id_seq'::regclass);


--
-- Name: wireguard_peers id; Type: DEFAULT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.wireguard_peers ALTER COLUMN id SET DEFAULT nextval('public.wireguard_peers_id_seq'::regclass);


--
-- Data for Name: hypertable; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: wifi_user
--

COPY _timescaledb_catalog.hypertable (id, schema_name, table_name, associated_schema_name, associated_table_prefix, num_dimensions, chunk_sizing_func_schema, chunk_sizing_func_name, chunk_target_size, compression_state, compressed_hypertable_id, status) FROM stdin;
1	public	netflow_records	_timescaledb_internal	_hyper_1	1	_timescaledb_functions	calculate_chunk_interval	0	0	\N	0
\.


--
-- Data for Name: bgw_job; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: wifi_user
--

COPY _timescaledb_catalog.bgw_job (id, application_name, schedule_interval, max_runtime, max_retries, retry_period, proc_schema, proc_name, owner, scheduled, fixed_schedule, initial_start, hypertable_id, config, check_schema, check_name, timezone) FROM stdin;
\.


--
-- Data for Name: chunk; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: wifi_user
--

COPY _timescaledb_catalog.chunk (id, hypertable_id, schema_name, table_name, compressed_chunk_id, dropped, status, osm_chunk, creation_time) FROM stdin;
\.


--
-- Data for Name: chunk_column_stats; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: wifi_user
--

COPY _timescaledb_catalog.chunk_column_stats (id, hypertable_id, chunk_id, column_name, range_start, range_end, valid) FROM stdin;
\.


--
-- Data for Name: dimension; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: wifi_user
--

COPY _timescaledb_catalog.dimension (id, hypertable_id, column_name, column_type, aligned, num_slices, partitioning_func_schema, partitioning_func, interval_length, compress_interval_length, integer_now_func_schema, integer_now_func) FROM stdin;
1	1	time	timestamp with time zone	t	\N	\N	\N	604800000000	\N	\N	\N
\.


--
-- Data for Name: dimension_slice; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: wifi_user
--

COPY _timescaledb_catalog.dimension_slice (id, dimension_id, range_start, range_end) FROM stdin;
\.


--
-- Data for Name: chunk_constraint; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: wifi_user
--

COPY _timescaledb_catalog.chunk_constraint (chunk_id, dimension_slice_id, constraint_name, hypertable_constraint_name) FROM stdin;
\.


--
-- Data for Name: compression_chunk_size; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: wifi_user
--

COPY _timescaledb_catalog.compression_chunk_size (chunk_id, compressed_chunk_id, uncompressed_heap_size, uncompressed_toast_size, uncompressed_index_size, compressed_heap_size, compressed_toast_size, compressed_index_size, numrows_pre_compression, numrows_post_compression, numrows_frozen_immediately) FROM stdin;
\.


--
-- Data for Name: compression_settings; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: wifi_user
--

COPY _timescaledb_catalog.compression_settings (relid, compress_relid, segmentby, orderby, orderby_desc, orderby_nullsfirst, index) FROM stdin;
\.


--
-- Data for Name: continuous_agg; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: wifi_user
--

COPY _timescaledb_catalog.continuous_agg (mat_hypertable_id, raw_hypertable_id, parent_mat_hypertable_id, user_view_schema, user_view_name, partial_view_schema, partial_view_name, direct_view_schema, direct_view_name, materialized_only) FROM stdin;
\.


--
-- Data for Name: continuous_agg_migrate_plan; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: wifi_user
--

COPY _timescaledb_catalog.continuous_agg_migrate_plan (mat_hypertable_id, start_ts, end_ts, user_view_definition) FROM stdin;
\.


--
-- Data for Name: continuous_agg_migrate_plan_step; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: wifi_user
--

COPY _timescaledb_catalog.continuous_agg_migrate_plan_step (mat_hypertable_id, step_id, status, start_ts, end_ts, type, config) FROM stdin;
\.


--
-- Data for Name: continuous_aggs_bucket_function; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: wifi_user
--

COPY _timescaledb_catalog.continuous_aggs_bucket_function (mat_hypertable_id, bucket_func, bucket_width, bucket_origin, bucket_offset, bucket_timezone, bucket_fixed_width) FROM stdin;
\.


--
-- Data for Name: continuous_aggs_hypertable_invalidation_log; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: wifi_user
--

COPY _timescaledb_catalog.continuous_aggs_hypertable_invalidation_log (hypertable_id, lowest_modified_value, greatest_modified_value) FROM stdin;
\.


--
-- Data for Name: continuous_aggs_invalidation_threshold; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: wifi_user
--

COPY _timescaledb_catalog.continuous_aggs_invalidation_threshold (hypertable_id, watermark) FROM stdin;
\.


--
-- Data for Name: continuous_aggs_materialization_invalidation_log; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: wifi_user
--

COPY _timescaledb_catalog.continuous_aggs_materialization_invalidation_log (materialization_id, lowest_modified_value, greatest_modified_value) FROM stdin;
\.


--
-- Data for Name: continuous_aggs_materialization_ranges; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: wifi_user
--

COPY _timescaledb_catalog.continuous_aggs_materialization_ranges (materialization_id, lowest_modified_value, greatest_modified_value) FROM stdin;
\.


--
-- Data for Name: continuous_aggs_watermark; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: wifi_user
--

COPY _timescaledb_catalog.continuous_aggs_watermark (mat_hypertable_id, watermark) FROM stdin;
\.


--
-- Data for Name: metadata; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: wifi_user
--

COPY _timescaledb_catalog.metadata (key, value, include_in_telemetry) FROM stdin;
install_timestamp	2026-02-14 18:00:17.377373+00	t
timescaledb_version	2.25.0	f
exported_uuid	b591e2bb-09c3-4166-a63b-687a12de4cee	t
\.


--
-- Data for Name: tablespace; Type: TABLE DATA; Schema: _timescaledb_catalog; Owner: wifi_user
--

COPY _timescaledb_catalog.tablespace (id, hypertable_id, tablespace_name) FROM stdin;
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: wifi_user
--

COPY public.alembic_version (version_num) FROM stdin;
9928f569915c
\.


--
-- Data for Name: audit_logs; Type: TABLE DATA; Schema: public; Owner: wifi_user
--

COPY public.audit_logs (user_id, action, resource_type, resource_id, details, ip_address, created_at, id, updated_at, deleted_at) FROM stdin;
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.12	2026-02-15 18:56:30.149194+00	1	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.12	2026-02-15 19:02:34.109685+00	2	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.12	2026-02-15 19:07:24.82208+00	3	\N	\N
1	POST	venues	\N	{"path": "/api/v1/venues", "method": "POST", "query_params": {}}	172.18.0.12	2026-02-15 19:10:24.120986+00	4	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.12	2026-02-15 19:21:34.069504+00	5	\N	\N
1	POST	users	\N	{"path": "/api/v1/users", "method": "POST", "query_params": {}}	172.18.0.12	2026-02-15 19:27:48.01853+00	6	\N	\N
1	POST	users	\N	{"path": "/api/v1/users", "method": "POST", "query_params": {}}	172.18.0.12	2026-02-15 19:28:25.139665+00	7	\N	\N
1	DELETE	users	\N	{"path": "/api/v1/users/3", "method": "DELETE", "query_params": {}}	172.18.0.12	2026-02-15 19:29:17.807339+00	8	\N	\N
1	POST	users	\N	{"path": "/api/v1/users", "method": "POST", "query_params": {}}	172.18.0.12	2026-02-15 19:31:07.2211+00	9	\N	\N
1	POST	users	\N	{"path": "/api/v1/users", "method": "POST", "query_params": {}}	172.18.0.12	2026-02-15 19:31:29.889468+00	10	\N	\N
1	POST	users	\N	{"path": "/api/v1/users", "method": "POST", "query_params": {}}	172.18.0.12	2026-02-15 19:32:02.289483+00	11	\N	\N
1	POST	banners	\N	{"path": "/api/v1/banners", "method": "POST", "query_params": {}}	172.18.0.12	2026-02-15 19:41:25.287868+00	12	\N	\N
1	DELETE	banners	\N	{"path": "/api/v1/banners/2", "method": "DELETE", "query_params": {}}	172.18.0.12	2026-02-15 19:41:50.056333+00	13	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.12	2026-02-15 19:51:04.742069+00	14	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.12	2026-02-15 19:51:21.176988+00	15	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.12	2026-02-15 19:51:47.180249+00	16	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.12	2026-02-15 19:52:02.612806+00	17	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.12	2026-02-15 20:00:29.361997+00	18	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.12	2026-02-15 20:01:18.376303+00	19	\N	\N
1	POST	wireguard	\N	{"path": "/api/v1/wireguard/peers", "method": "POST", "query_params": {}}	172.18.0.12	2026-02-15 20:01:57.454991+00	20	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.12	2026-02-15 20:12:11.633693+00	21	\N	\N
1	POST	nas-devices	\N	{"path": "/api/v1/nas-devices", "method": "POST", "query_params": {}}	172.18.0.12	2026-02-15 20:28:30.839083+00	22	\N	\N
1	PUT	nas-devices	\N	{"path": "/api/v1/nas-devices/15", "method": "PUT", "query_params": {}}	172.18.0.12	2026-02-15 20:28:45.758865+00	23	\N	\N
1	POST	portal-templates	\N	{"path": "/api/v1/portal-templates", "method": "POST", "query_params": {}}	172.18.0.12	2026-02-15 20:30:42.061564+00	24	\N	\N
1	DELETE	portal-templates	\N	{"path": "/api/v1/portal-templates/1", "method": "DELETE", "query_params": {}}	172.18.0.12	2026-02-15 20:31:06.307079+00	25	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.12	2026-02-15 20:52:18.221711+00	26	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-16 09:27:24.72839+00	27	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.9	2026-02-16 09:27:37.449143+00	28	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.9	2026-02-16 09:28:14.546729+00	29	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-16 09:30:14.821907+00	30	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/sms/request", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-16 09:36:12.400937+00	31	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.9	2026-02-16 09:38:30.345672+00	32	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.14	2026-02-16 11:32:10.968389+00	33	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.14	2026-02-16 11:38:03.030836+00	34	\N	\N
1	POST	portal-templates	\N	{"path": "/api/v1/portal-templates", "method": "POST", "query_params": {}}	172.18.0.14	2026-02-16 11:38:30.28904+00	35	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.14	2026-02-16 12:42:53.19633+00	36	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.14	2026-02-16 12:45:47.877208+00	37	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.14	2026-02-16 13:19:26.923212+00	38	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.14	2026-02-16 13:22:13.124649+00	39	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.14	2026-02-16 13:25:43.932341+00	40	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.14	2026-02-16 13:26:51.742107+00	41	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.14	2026-02-16 13:28:45.402192+00	42	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.14	2026-02-16 13:31:22.835688+00	43	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.14	2026-02-16 13:35:25.124209+00	44	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.14	2026-02-16 13:37:38.856293+00	45	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.14	2026-02-16 13:41:05.851999+00	46	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.14	2026-02-16 13:44:10.719057+00	47	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-16 13:51:53.663022+00	48	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-16 14:00:15.092258+00	49	\N	\N
1	POST	sms-providers	\N	{"path": "/api/v1/sms-providers", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-16 14:05:39.410486+00	50	\N	\N
1	POST	sms-providers	\N	{"path": "/api/v1/sms-providers", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-16 14:10:23.934817+00	51	\N	\N
1	POST	sms-providers	\N	{"path": "/api/v1/sms-providers", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-16 14:11:26.185161+00	52	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/telegram/init", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-16 14:21:41.932809+00	53	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-16 14:48:48.440007+00	55	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/telegram/init", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-16 14:21:41.976258+00	54	\N	\N
1	PUT	settings	\N	{"path": "/api/v1/settings/telegram_bot_token", "method": "PUT", "query_params": {}}	172.18.0.1	2026-02-16 14:56:41.468161+00	58	\N	\N
1	PUT	settings	\N	{"path": "/api/v1/settings/telegram_bot_webhook_url", "method": "PUT", "query_params": {}}	172.18.0.1	2026-02-16 14:57:20.999006+00	65	\N	\N
1	PUT	settings	\N	{"path": "/api/v1/settings/telegram_bot_webhook_url", "method": "PUT", "query_params": {}}	172.18.0.1	2026-02-16 14:57:22.473809+00	67	\N	\N
1	PUT	settings	\N	{"path": "/api/v1/settings/telegram_bot_username", "method": "PUT", "query_params": {}}	172.18.0.1	2026-02-16 15:05:19.399241+00	73	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.14	2026-02-16 14:54:16.265458+00	56	\N	\N
1	PUT	settings	\N	{"path": "/api/v1/settings/telegram_bot_username", "method": "PUT", "query_params": {}}	172.18.0.1	2026-02-16 14:56:41.457038+00	57	\N	\N
1	PUT	settings	\N	{"path": "/api/v1/settings/telegram_bot_webhook_url", "method": "PUT", "query_params": {}}	172.18.0.1	2026-02-16 14:56:41.487149+00	59	\N	\N
1	PUT	settings	\N	{"path": "/api/v1/settings/telegram_bot_token", "method": "PUT", "query_params": {}}	172.18.0.1	2026-02-16 14:57:10.40269+00	60	\N	\N
1	PUT	settings	\N	{"path": "/api/v1/settings/telegram_bot_webhook_url", "method": "PUT", "query_params": {}}	172.18.0.1	2026-02-16 14:57:10.417921+00	61	\N	\N
1	PUT	settings	\N	{"path": "/api/v1/settings/telegram_bot_username", "method": "PUT", "query_params": {}}	172.18.0.1	2026-02-16 14:57:11.116525+00	62	\N	\N
1	PUT	settings	\N	{"path": "/api/v1/settings/telegram_bot_username", "method": "PUT", "query_params": {}}	172.18.0.1	2026-02-16 14:57:20.974178+00	63	\N	\N
1	PUT	settings	\N	{"path": "/api/v1/settings/telegram_bot_token", "method": "PUT", "query_params": {}}	172.18.0.1	2026-02-16 14:57:20.993035+00	64	\N	\N
1	PUT	settings	\N	{"path": "/api/v1/settings/telegram_bot_username", "method": "PUT", "query_params": {}}	172.18.0.1	2026-02-16 14:57:22.462855+00	66	\N	\N
1	PUT	settings	\N	{"path": "/api/v1/settings/telegram_bot_token", "method": "PUT", "query_params": {}}	172.18.0.1	2026-02-16 14:57:22.483785+00	68	\N	\N
1	PUT	settings	\N	{"path": "/api/v1/settings/telegram_bot_token", "method": "PUT", "query_params": {}}	172.18.0.1	2026-02-16 15:02:06.070415+00	69	\N	\N
1	PUT	settings	\N	{"path": "/api/v1/settings/telegram_bot_webhook_url", "method": "PUT", "query_params": {}}	172.18.0.1	2026-02-16 15:02:06.114038+00	70	\N	\N
1	PUT	settings	\N	{"path": "/api/v1/settings/telegram_bot_username", "method": "PUT", "query_params": {}}	172.18.0.1	2026-02-16 15:02:06.133451+00	71	\N	\N
1	PUT	settings	\N	{"path": "/api/v1/settings/telegram_bot_webhook_url", "method": "PUT", "query_params": {}}	172.18.0.1	2026-02-16 15:05:19.384159+00	72	\N	\N
1	PUT	settings	\N	{"path": "/api/v1/settings/telegram_bot_token", "method": "PUT", "query_params": {}}	172.18.0.1	2026-02-16 15:05:19.404188+00	74	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/telegram/init", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-16 15:18:29.052585+00	75	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/telegram/init", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-16 15:18:29.075157+00	76	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/telegram/init", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-16 15:21:18.561009+00	77	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/telegram/init", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-16 15:21:18.576784+00	78	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-16 15:22:50.397588+00	79	\N	\N
1	PUT	settings	\N	{"path": "/api/v1/settings/telegram_bot_username", "method": "PUT", "query_params": {}}	172.18.0.1	2026-02-16 15:23:02.164898+00	80	\N	\N
1	PUT	settings	\N	{"path": "/api/v1/settings/telegram_bot_webhook_url", "method": "PUT", "query_params": {}}	172.18.0.1	2026-02-16 15:23:02.176482+00	81	\N	\N
1	PUT	settings	\N	{"path": "/api/v1/settings/telegram_bot_token", "method": "PUT", "query_params": {}}	172.18.0.1	2026-02-16 15:23:02.180159+00	82	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/telegram/init", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-16 15:30:14.373203+00	83	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/telegram/init", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-16 15:30:14.373019+00	84	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/telegram/init", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-16 15:40:20.005741+00	85	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/telegram/init", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-16 15:40:20.011857+00	86	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/telegram/init", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-16 15:42:29.998453+00	87	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/telegram/init", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-16 15:42:30.006292+00	88	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/telegram/init", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-16 15:45:01.920228+00	89	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/telegram/init", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-16 15:45:01.929077+00	90	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/telegram/init", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-16 15:52:03.036833+00	91	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/telegram/init", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-16 15:52:03.04699+00	92	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/telegram/callback", "method": "POST", "query_params": {}}	172.18.0.10	2026-02-16 15:52:11.283404+00	93	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/telegram/init", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-16 15:54:57.055755+00	94	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/telegram/init", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-16 15:54:57.152953+00	95	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/telegram/callback", "method": "POST", "query_params": {}}	172.18.0.10	2026-02-16 15:55:06.476218+00	96	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/telegram/init", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-16 18:16:25.871642+00	97	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/telegram/init", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-16 18:16:25.871642+00	98	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/telegram/callback", "method": "POST", "query_params": {}}	172.18.0.12	2026-02-16 18:16:35.253074+00	99	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-16 18:21:58.968598+00	100	\N	\N
1	POST	builtin-templates	\N	{"path": "/api/v1/builtin-templates/dark/import", "method": "POST", "query_params": {"venue_id": "1"}}	172.18.0.1	2026-02-16 18:27:19.023304+00	101	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-17 05:49:24.77711+00	102	\N	\N
1	POST	builtin-templates	\N	{"path": "/api/v1/builtin-templates/hotel/import", "method": "POST", "query_params": {"venue_id": "1"}}	172.18.0.1	2026-02-17 05:49:55.919223+00	103	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-17 05:54:56.594886+00	104	\N	\N
1	POST	builtin-templates	\N	{"path": "/api/v1/builtin-templates/dark/import", "method": "POST", "query_params": {"venue_id": "1"}}	172.18.0.1	2026-02-17 05:55:21.163965+00	105	\N	\N
1	POST	builtin-templates	\N	{"path": "/api/v1/builtin-templates/light/import", "method": "POST", "query_params": {"venue_id": "1"}}	172.18.0.1	2026-02-17 05:59:59.549999+00	106	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-17 08:51:04.396509+00	107	\N	\N
1	DELETE	portal-templates	\N	{"path": "/api/v1/portal-templates/2", "method": "DELETE", "query_params": {}}	172.18.0.1	2026-02-17 08:51:36.937601+00	108	\N	\N
1	DELETE	portal-templates	\N	{"path": "/api/v1/portal-templates/3", "method": "DELETE", "query_params": {}}	172.18.0.1	2026-02-17 08:51:39.419913+00	109	\N	\N
1	DELETE	portal-templates	\N	{"path": "/api/v1/portal-templates/4", "method": "DELETE", "query_params": {}}	172.18.0.1	2026-02-17 08:51:41.762955+00	110	\N	\N
1	DELETE	portal-templates	\N	{"path": "/api/v1/portal-templates/5", "method": "DELETE", "query_params": {}}	172.18.0.1	2026-02-17 08:51:43.986202+00	111	\N	\N
1	DELETE	portal-templates	\N	{"path": "/api/v1/portal-templates/6", "method": "DELETE", "query_params": {}}	172.18.0.1	2026-02-17 08:51:46.105095+00	112	\N	\N
1	DELETE	portal-templates	\N	{"path": "/api/v1/portal-templates/7", "method": "DELETE", "query_params": {}}	172.18.0.1	2026-02-17 08:51:48.081819+00	113	\N	\N
1	DELETE	portal-templates	\N	{"path": "/api/v1/portal-templates/8", "method": "DELETE", "query_params": {}}	172.18.0.1	2026-02-17 08:51:49.958489+00	114	\N	\N
1	DELETE	portal-templates	\N	{"path": "/api/v1/portal-templates/9", "method": "DELETE", "query_params": {}}	172.18.0.1	2026-02-17 08:51:51.65029+00	115	\N	\N
1	DELETE	portal-templates	\N	{"path": "/api/v1/portal-templates/10", "method": "DELETE", "query_params": {}}	172.18.0.1	2026-02-17 08:51:54.031622+00	116	\N	\N
1	POST	builtin-templates	\N	{"path": "/api/v1/builtin-templates/light/import", "method": "POST", "query_params": {"venue_id": "1"}}	172.18.0.1	2026-02-17 08:51:57.975252+00	117	\N	\N
1	POST	builtin-templates	\N	{"path": "/api/v1/builtin-templates/dark/import", "method": "POST", "query_params": {"venue_id": "1"}}	172.18.0.1	2026-02-17 08:52:03.022584+00	118	\N	\N
1	DELETE	portal-templates	\N	{"path": "/api/v1/portal-templates/11", "method": "DELETE", "query_params": {}}	172.18.0.1	2026-02-17 09:08:40.474816+00	119	\N	\N
1	POST	builtin-templates	\N	{"path": "/api/v1/builtin-templates/dark/import", "method": "POST", "query_params": {"venue_id": "1"}}	172.18.0.1	2026-02-17 09:08:45.600067+00	120	\N	\N
1	POST	builtin-templates	\N	{"path": "/api/v1/builtin-templates/dark/import", "method": "POST", "query_params": {"venue_id": "1"}}	172.18.0.1	2026-02-17 09:17:29.35385+00	121	\N	\N
1	PUT	sms-providers	\N	{"path": "/api/v1/sms-providers/3", "method": "PUT", "query_params": {}}	172.18.0.1	2026-02-17 09:18:01.606251+00	122	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-17 09:48:49.820332+00	123	\N	\N
1	POST	portal-templates	\N	{"path": "/api/v1/portal-templates", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-17 09:49:27.416898+00	124	\N	\N
1	DELETE	portal-templates	\N	{"path": "/api/v1/portal-templates/19", "method": "DELETE", "query_params": {}}	172.18.0.1	2026-02-17 09:49:34.945584+00	125	\N	\N
1	PUT	portal-templates	\N	{"path": "/api/v1/portal-templates/18", "method": "PUT", "query_params": {}}	172.18.0.1	2026-02-17 09:49:44.770728+00	126	\N	\N
1	PUT	portal-templates	\N	{"path": "/api/v1/portal-templates/17", "method": "PUT", "query_params": {}}	172.18.0.1	2026-02-17 09:49:51.136544+00	127	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-17 10:57:03.181185+00	128	\N	\N
1	POST	builtin-templates	\N	{"path": "/api/v1/builtin-templates/dark/import", "method": "POST", "query_params": {"venue_id": "1"}}	172.18.0.1	2026-02-17 10:57:18.471929+00	129	\N	\N
1	DELETE	portal-templates	\N	{"path": "/api/v1/portal-templates/12", "method": "DELETE", "query_params": {}}	172.18.0.1	2026-02-17 10:57:26.256399+00	130	\N	\N
1	DELETE	portal-templates	\N	{"path": "/api/v1/portal-templates/14", "method": "DELETE", "query_params": {}}	172.18.0.1	2026-02-17 10:57:28.426391+00	131	\N	\N
1	DELETE	portal-templates	\N	{"path": "/api/v1/portal-templates/13", "method": "DELETE", "query_params": {}}	172.18.0.1	2026-02-17 10:57:30.923091+00	132	\N	\N
1	DELETE	portal-templates	\N	{"path": "/api/v1/portal-templates/15", "method": "DELETE", "query_params": {}}	172.18.0.1	2026-02-17 10:57:32.80794+00	133	\N	\N
1	DELETE	portal-templates	\N	{"path": "/api/v1/portal-templates/16", "method": "DELETE", "query_params": {}}	172.18.0.1	2026-02-17 10:57:34.865995+00	134	\N	\N
1	DELETE	portal-templates	\N	{"path": "/api/v1/portal-templates/18", "method": "DELETE", "query_params": {}}	172.18.0.1	2026-02-17 10:57:37.260972+00	135	\N	\N
1	DELETE	portal-templates	\N	{"path": "/api/v1/portal-templates/17", "method": "DELETE", "query_params": {}}	172.18.0.1	2026-02-17 10:57:39.575069+00	136	\N	\N
1	DELETE	portal-templates	\N	{"path": "/api/v1/portal-templates/20", "method": "DELETE", "query_params": {}}	172.18.0.1	2026-02-17 10:57:41.351533+00	137	\N	\N
1	DELETE	portal-templates	\N	{"path": "/api/v1/portal-templates/21", "method": "DELETE", "query_params": {}}	172.18.0.1	2026-02-17 10:57:44.811822+00	138	\N	\N
1	POST	builtin-templates	\N	{"path": "/api/v1/builtin-templates/hotel/import", "method": "POST", "query_params": {"venue_id": "1"}}	172.18.0.1	2026-02-17 10:57:50.228972+00	139	\N	\N
1	PUT	portal-templates	\N	{"path": "/api/v1/portal-templates/22", "method": "PUT", "query_params": {}}	172.18.0.1	2026-02-17 10:58:02.338561+00	140	\N	\N
1	PUT	portal-templates	\N	{"path": "/api/v1/portal-templates/23", "method": "PUT", "query_params": {}}	172.18.0.1	2026-02-17 10:58:13.288035+00	141	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-17 14:34:07.766207+00	142	\N	\N
1	POST	sms-providers	\N	{"path": "/api/v1/sms-providers", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-17 14:34:32.601055+00	143	\N	\N
\N	POST	auth	\N	{"path": "/api/v1/auth/login", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-17 14:51:57.405793+00	144	\N	\N
1	POST	sms-providers	\N	{"path": "/api/v1/sms-providers", "method": "POST", "query_params": {}}	172.18.0.1	2026-02-17 14:52:14.64474+00	145	\N	\N
\.


--
-- Data for Name: banners; Type: TABLE DATA; Schema: public; Owner: wifi_user
--

COPY public.banners (venue_id, image_url, target_url, clicks_count, impressions_count, is_active, id, created_at, updated_at, deleted_at) FROM stdin;
1	\N	https://avatars.mds.yandex.net/i?id=370a1cb9905678f74518075bc6f0e29b2e03555d-5326574-images-thumbs&n=13	0	0	t	2	2026-02-15 19:41:25.235522+00	2026-02-15 19:41:50.043833+00	2026-02-15 19:41:50.046171+00
\.


--
-- Data for Name: crm_providers; Type: TABLE DATA; Schema: public; Owner: wifi_user
--

COPY public.crm_providers (id, name, type, config, is_active, priority, created_at, updated_at, deleted_at) FROM stdin;
\.


--
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: wifi_user
--

COPY public.events (user_profile_id, venue_id, type, data, created_at, id, updated_at, deleted_at) FROM stdin;
\.


--
-- Data for Name: local_users; Type: TABLE DATA; Schema: public; Owner: wifi_user
--

COPY public.local_users (username, password_hash, venue_id, user_profile_id, is_active, id, created_at, updated_at, deleted_at) FROM stdin;
\.


--
-- Data for Name: nas_devices; Type: TABLE DATA; Schema: public; Owner: wifi_user
--

COPY public.nas_devices (id, venue_id, name, type, ip_address, secret, api_username, api_password, wireguard_pubkey, wireguard_ip, is_active, created_at, updated_at, deleted_at, last_seen, status, last_check, config) FROM stdin;
1	1	мвы	MIKROTIK	8.8.8.8	\\x67414141414142706b6873496d6f6f35705331794c6c4e465f5642496b54355a53684758444e4a4471534b48463039646f36617543704c3854355037505a4f4b66444475642d613344366872425577766273467255637868725458596a44774950513d3d	мв	\\x67414141414142706b68734945764873435f34413346376142747a566e6453357a486633556a636e316c475a54685546796f6f48765f485247493149394544576e5333514d64336e6f4249632d5a72676b685731665a7643344658575277665f35513d3d	мвы	мв	t	2026-02-15 19:14:16.406989+00	2026-02-15 19:14:16.421987+00	2026-02-15 19:14:16.426851+00	\N	unknown	\N	\N
5	1	ffff	MIKROTIK	37.212.27.187	\\x67414141414142706b6948413857624e765644466b61785a3341585072465170693253796b324c3644716d48526b505558366531645665333574535747435144756b6e774378504e70496a4b6755707a6c5938476642504c436a654e6566384661513d3d	gsfddfhfgkjhk	\\x67414141414142706b694841394c6e6e32486c7666496a51726a4c62727550677a766770464670684b4d4e57754356456f712d682d5837737a576645676577414c7378765644307959533832793549644e485a77583155743535395a7372426963673d3d	dtshdfjgfkh	192.168.50.1	t	2026-02-15 19:42:56.446565+00	2026-02-15 19:42:56.455088+00	2026-02-15 19:42:56.456197+00	\N	unknown	\N	\N
9	1	ggggggg	MIKROTIK	37.11.55.65	\\x67414141414142706b6969336969537a39577a6a5a4864694c376843653042334b703239494b335859395643785645523355764843566b5164576a5a6f4e4a78624d756f4f506d4e32435f7a3270386d3033436a54303458766a75424e79385f43673d3d	hg	\\x67414141414142706b696933716a663070553662384d5a6f6861697665394e6936384865313156706b506a6e5466744748317176536377652d344732374a2d455039353563586f5655484a726961375658676855446762476a31436c5f6a347547673d3d	gh	192.168.50.1	t	2026-02-15 20:12:39.815997+00	2026-02-15 20:12:39.825434+00	2026-02-15 20:12:39.826661+00	\N	unknown	\N	\N
\.


--
-- Data for Name: nas_status_history; Type: TABLE DATA; Schema: public; Owner: wifi_user
--

COPY public.nas_status_history (nas_device_id, status, checked_at, id, created_at, updated_at, deleted_at) FROM stdin;
\.


--
-- Data for Name: netflow_records; Type: TABLE DATA; Schema: public; Owner: wifi_user
--

COPY public.netflow_records ("time", session_id, src_ip, dst_ip, bytes, packets, src_port, dst_port, protocol, flow_start, flow_end, id, created_at, updated_at, deleted_at) FROM stdin;
\.


--
-- Data for Name: portal_templates; Type: TABLE DATA; Schema: public; Owner: wifi_user
--

COPY public.portal_templates (venue_id, type, html_content, css_files, js_files, images, is_active, id, created_at, updated_at, deleted_at) FROM stdin;
1	welcome	kljhkl	[]	[]	[]	t	1	2026-02-15 20:30:41.967024+00	2026-02-15 20:31:06.295658+00	2026-02-15 20:31:06.297343+00
1	auth	ч мми	[]	[]	[]	t	2	2026-02-16 11:38:30.274202+00	2026-02-17 08:51:36.922339+00	2026-02-17 08:51:36.925341+00
1	welcome	<!DOCTYPE html>\n<html lang="ru">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>Добро пожаловать - $(venue_name)</title>\n    <link rel="stylesheet" href="/static/templates/dark/style.css">\n</head>\n<body>\n    <div class="container">\n        <div class="card">\n            <div class="logo">\n                <img src="$(banner_url)" alt="Логотип" onerror="this.style.display='none'">\n            </div>\n            <h1>Вы успешно авторизованы!</h1>\n            <p class="sub">Приятного использования интернета</p>\n            <p>MAC: $(mac)</p>\n        </div>\n    </div>\n</body>\n</html>	[]	[]	[]	f	4	2026-02-16 18:27:18.949186+00	2026-02-17 08:51:41.750945+00	2026-02-17 08:51:41.752633+00
1	auth	<!DOCTYPE html>\n<html lang="ru">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>$(venue_name) - Wi-Fi гостя</title>\n    <link rel="stylesheet" href="/static/templates/hotel/style.css">\n</head>\n<body>\n    <div class="header">\n        <div class="hotel-name">$(venue_name)</div>\n    </div>\n    <div class="container">\n        <div class="welcome-card">\n            <h1>Добро пожаловать!</h1>\n            <p class="subtitle">Для доступа в интернет подтвердите ваш номер телефона</p>\n            \n            $(if error_text)\n            <div class="error">$(error_text)</div>\n            $(endif)\n            \n            <form method="post" action="/portal/$(venue_id)/auth">\n                <input type="hidden" name="mac" value="$(mac)">\n                <div class="form-group">\n                    <label for="phone">Номер телефона</label>\n                    <input type="tel" id="phone" name="phone" placeholder="+375 (29) XXX-XX-XX" value="$(phone)" required>\n                </div>\n                <button type="submit">Получить SMS с кодом</button>\n            </form>\n            <p class="legal">Нажимая кнопку, вы соглашаетесь с <a href="#">правилами отеля</a></p>\n        </div>\n    </div>\n    <div class="footer">\n        <img src="$(banner_url)" alt="Партнеры" class="partners">\n    </div>\n</body>\n</html>	[]	[]	[]	f	5	2026-02-17 05:49:55.89534+00	2026-02-17 08:51:43.973562+00	2026-02-17 08:51:43.9755+00
1	welcome	<!DOCTYPE html>\n<html lang="ru">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>Добро пожаловать - $(venue_name)</title>\n    <link rel="stylesheet" href="/static/templates/hotel/style.css">\n</head>\n<body>\n    <div class="header">\n        <div class="hotel-name">$(venue_name)</div>\n    </div>\n    <div class="container">\n        <div class="welcome-card">\n            <h1>Вы успешно авторизованы!</h1>\n            <p class="subtitle">Приятного отдыха в нашем отеле</p>\n            <p>MAC адрес: $(mac)</p>\n        </div>\n    </div>\n    <div class="footer">\n        <img src="$(banner_url)" alt="Партнеры" class="partners">\n    </div>\n</body>\n</html>	[]	[]	[]	f	6	2026-02-17 05:49:55.89534+00	2026-02-17 08:51:46.094154+00	2026-02-17 08:51:46.095847+00
1	auth	<!DOCTYPE html>\n<html lang="ru">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>$(venue_name) - Авторизация</title>\n    <link rel="stylesheet" href="/static/templates/dark/style.css">\n</head>\n<body>\n    <div class="container">\n        <div class="card">\n            <div class="logo">\n                <img src="$(banner_url)" alt="Логотип" onerror="this.style.display='none'">\n            </div>\n            <h1>Добро пожаловать</h1>\n            <p class="sub">Подтвердите номер телефона для доступа в интернет</p>\n            \n            $(if error_text)\n            <div class="error">$(error_text)</div>\n            $(endif)\n            \n            <form method="post" action="/portal/$(venue_id)/auth">\n                <input type="hidden" name="mac" value="$(mac)">\n                <div class="form-group">\n                    <input type="tel" name="phone" placeholder="+375 (29) XXX-XX-XX" value="$(phone)" required>\n                </div>\n                <button type="submit">Получить код</button>\n            </form>\n            <p class="hint">Код придет в SMS в течение минуты</p>\n        </div>\n    </div>\n</body>\n</html>	[]	[]	[]	f	7	2026-02-17 05:55:21.026233+00	2026-02-17 08:51:48.071707+00	2026-02-17 08:51:48.07342+00
1	welcome	<!DOCTYPE html>\n<html lang="ru">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>Добро пожаловать - $(venue_name)</title>\n    <link rel="stylesheet" href="/static/templates/dark/style.css">\n</head>\n<body>\n    <div class="container">\n        <div class="card">\n            <div class="logo">\n                <img src="$(banner_url)" alt="Логотип" onerror="this.style.display='none'">\n            </div>\n            <h1>Вы успешно авторизованы!</h1>\n            <p class="sub">Приятного использования интернета</p>\n            <p>MAC: $(mac)</p>\n        </div>\n    </div>\n</body>\n</html>	[]	[]	[]	f	8	2026-02-17 05:55:21.026233+00	2026-02-17 08:51:49.948202+00	2026-02-17 08:51:49.949863+00
1	auth	<!DOCTYPE html>\n<html lang="ru">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>$(venue_name) - Авторизация</title>\n    <link rel="stylesheet" href="/static/templates/dark/style.css">\n</head>\n<body>\n    <div class="container">\n        <div class="card">\n            <div class="logo">\n                <img src="$(banner_url)" alt="Логотип" onerror="this.style.display='none'">\n            </div>\n            <h1>Добро пожаловать</h1>\n            <p class="sub">Подтвердите номер телефона для доступа в интернет</p>\n            \n            $(if error_text)\n            <div class="error">$(error_text)</div>\n            $(endif)\n            \n            <form method="post" action="/portal/$(venue_id)/auth">\n                <input type="hidden" name="mac" value="$(mac)">\n                <div class="form-group">\n                    <input type="tel" name="phone" placeholder="+375 (29) XXX-XX-XX" value="$(phone)" required>\n                </div>\n                <button type="submit">Получить код</button>\n            </form>\n            <p class="hint">Код придет в SMS в течение минуты</p>\n        </div>\n    </div>\n</body>\n</html>	[]	[]	[]	f	3	2026-02-16 18:27:18.949186+00	2026-02-17 08:51:39.406673+00	2026-02-17 08:51:39.408469+00
1	auth	<!DOCTYPE html>\n<html lang="ru">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>$(venue_name) - Wi-Fi</title>\n    <link rel="stylesheet" href="/static/templates/light/style.css">\n</head>\n<body>\n    <div class="container">\n        <div class="card">\n            <div class="logo">\n                <img src="$(banner_url)" alt="Логотип" onerror="this.style.display='none'">\n            </div>\n            <h1>Добро пожаловать!</h1>\n            <p class="sub">Для доступа в интернет введите номер телефона</p>\n            \n            $(if error_text)\n            <div class="error">$(error_text)</div>\n            $(endif)\n            \n            <form method="post" action="/portal/$(venue_id)/auth">\n                <input type="hidden" name="mac" value="$(mac)">\n                <div class="form-group">\n                    <input type="tel" name="phone" placeholder="+375 (29) XXX-XX-XX" value="$(phone)" required>\n                </div>\n                <button type="submit">Продолжить</button>\n            </form>\n            <p class="info">Мы отправим SMS с кодом подтверждения</p>\n        </div>\n    </div>\n</body>\n</html>\n	[]	[]	[]	f	9	2026-02-17 05:59:59.534149+00	2026-02-17 08:51:51.639316+00	2026-02-17 08:51:51.641058+00
1	welcome	<!DOCTYPE html>\n<html lang="ru">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>Добро пожаловать - $(venue_name)</title>\n    <link rel="stylesheet" href="/static/templates/light/style.css">\n</head>\n<body>\n    <div class="container">\n        <div class="card">\n            <div class="logo">\n                <img src="$(banner_url)" alt="Логотип" onerror="this.style.display='none'">\n            </div>\n            <h1>Вы успешно авторизованы!</h1>\n            <p class="sub">Приятного пользования интернетом</p>\n            <p>MAC: $(mac)</p>\n        </div>\n    </div>\n</body>\n</html>	[]	[]	[]	f	10	2026-02-17 05:59:59.534149+00	2026-02-17 08:51:54.021515+00	2026-02-17 08:51:54.023193+00
1	welcome	<!DOCTYPE html>\n<html lang="ru">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>Добро пожаловать - $(venue_name)</title>\n    <link rel="stylesheet" href="/static/templates/light/style.css">\n</head>\n<body>\n    <div class="container">\n        <div class="card">\n            <div class="logo">\n                <img src="$(banner_url)" alt="Логотип" onerror="this.style.display='none'">\n            </div>\n            <h1>Вы успешно авторизованы!</h1>\n            <p class="sub">Приятного пользования интернетом</p>\n            <p>MAC: $(mac)</p>\n        </div>\n    </div>\n</body>\n</html>	[]	[]	[]	f	12	2026-02-17 08:51:57.898589+00	2026-02-17 10:57:26.242751+00	2026-02-17 10:57:26.244994+00
1	welcome	<!DOCTYPE html>\n<html lang="ru">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>Добро пожаловать - $(venue_name)</title>\n    <link rel="stylesheet" href="/static/templates/dark/style.css">\n</head>\n<body>\n    <div class="container">\n        <div class="card">\n            <div class="logo">\n                <img src="$(banner_url)" alt="Логотип" onerror="this.style.display='none'">\n            </div>\n            <h1>Вы успешно авторизованы!</h1>\n            <p class="sub">Приятного использования интернета</p>\n            <p>MAC: $(mac)</p>\n        </div>\n    </div>\n</body>\n</html>	[]	[]	[]	f	14	2026-02-17 08:52:03.009403+00	2026-02-17 10:57:28.414675+00	2026-02-17 10:57:28.416713+00
1	auth	<!DOCTYPE html>\n<html lang="ru">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>$(venue_name) - Авторизация</title>\n    <link rel="stylesheet" href="/static/templates/dark/style.css">\n</head>\n<body>\n    <div class="container">\n        <div class="card">\n            <div class="logo">\n                <img src="$(banner_url)" alt="Логотип" onerror="this.style.display='none'">\n            </div>\n            <h1>Добро пожаловать</h1>\n            <p class="sub">Подтвердите номер телефона для доступа в интернет</p>\n            \n            $(if error_text)\n            <div class="error">$(error_text)</div>\n            $(endif)\n            \n            <form method="post" action="/portal/$(venue_id)/auth">\n                <input type="hidden" name="mac" value="$(mac)">\n                <div class="form-group">\n                    <input type="tel" name="phone" placeholder="+375 (29) XXX-XX-XX" value="$(phone)" required>\n                </div>\n                <button type="submit">Получить код</button>\n            </form>\n            <p class="hint">Код придет в SMS в течение минуты</p>\n        </div>\n    </div>\n</body>\n</html>	[]	[]	[]	f	13	2026-02-17 08:52:03.009403+00	2026-02-17 10:57:30.912558+00	2026-02-17 10:57:30.914187+00
1	auth	<!DOCTYPE html>\n<html lang="ru">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>$(venue_name) - Wi-Fi</title>\n    <link rel="stylesheet" href="/static/templates/light/style.css">\n</head>\n<body>\n    <div class="container">\n        <div class="card">\n            <div class="logo">\n                <img src="$(banner_url)" alt="Логотип" onerror="this.style.display='none'">\n            </div>\n            <h1>Добро пожаловать!</h1>\n            <p class="sub">Для доступа в интернет введите номер телефона</p>\n            \n            $(if error_text)\n            <div class="error">$(error_text)</div>\n            $(endif)\n            \n            <form method="post" action="/portal/$(venue_id)/auth">\n                <input type="hidden" name="mac" value="$(mac)">\n                <div class="form-group">\n                    <input type="tel" name="phone" placeholder="+375 (29) XXX-XX-XX" value="$(phone)" required>\n                </div>\n                <button type="submit">Продолжить</button>\n            </form>\n            <p class="info">Мы отправим SMS с кодом подтверждения</p>\n        </div>\n    </div>\n</body>\n</html>\n	[]	[]	[]	f	11	2026-02-17 08:51:57.898589+00	2026-02-17 09:08:40.414639+00	2026-02-17 09:08:40.418017+00
1	auth	квераноп	[]	[]	[]	t	19	2026-02-17 09:49:27.377903+00	2026-02-17 09:49:34.931586+00	2026-02-17 09:49:34.934091+00
1	auth	<!DOCTYPE html>\n<html lang="ru">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>$(venue_name) - Авторизация</title>\n    <link rel="stylesheet" href="/static/templates/dark/style.css">\n</head>\n<body>\n    <div class="container">\n        <div class="card">\n            <div class="logo">\n                <img src="$(banner_url)" alt="Логотип" onerror="this.style.display='none'">\n            </div>\n            <h1>Добро пожаловать</h1>\n            <p class="sub">Подтвердите номер телефона для доступа в интернет</p>\n            \n            $(if error_text)\n            <div class="error">$(error_text)</div>\n            $(endif)\n            \n            <form method="post" action="/portal/$(venue_id)/auth">\n                <input type="hidden" name="mac" value="$(mac)">\n                <div class="form-group">\n                    <input type="tel" name="phone" placeholder="+375 (29) XXX-XX-XX" value="$(phone)" required>\n                </div>\n                <button type="submit">Получить код</button>\n            </form>\n            <p class="hint">Код придет в SMS в течение минуты</p>\n        </div>\n    </div>\n</body>\n</html>	[]	[]	[]	f	15	2026-02-17 09:08:45.583019+00	2026-02-17 10:57:32.796813+00	2026-02-17 10:57:32.798753+00
1	welcome	<!DOCTYPE html>\n<html lang="ru">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>Добро пожаловать - $(venue_name)</title>\n    <link rel="stylesheet" href="/static/templates/dark/style.css">\n</head>\n<body>\n    <div class="container">\n        <div class="card">\n            <div class="logo">\n                <img src="$(banner_url)" alt="Логотип" onerror="this.style.display='none'">\n            </div>\n            <h1>Вы успешно авторизованы!</h1>\n            <p class="sub">Приятного использования интернета</p>\n            <p>MAC: $(mac)</p>\n        </div>\n    </div>\n</body>\n</html>	[]	[]	[]	f	16	2026-02-17 09:08:45.583019+00	2026-02-17 10:57:34.855828+00	2026-02-17 10:57:34.857737+00
1	welcome	<!DOCTYPE html>\n<html lang="ru">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>Добро пожаловать - $(venue_name)</title>\n    <link rel="stylesheet" href="/static/templates/dark/style.css">\n</head>\n<body>\n    <div class="container">\n        <div class="card">\n            <div class="logo">\n                <img src="$(banner_url)" alt="Логотип" onerror="this.style.display='none'">\n            </div>\n            <h1>Вы успешно авторизованы!</h1>\n            <p class="sub">Приятного использования интернета</p>\n            <p>MAC: $(mac)</p>\n        </div>\n    </div>\n</body>\n</html>	[]	[]	[]	t	18	2026-02-17 09:17:29.265085+00	2026-02-17 10:57:37.250695+00	2026-02-17 10:57:37.252328+00
1	auth	<!DOCTYPE html>\n<html lang="ru">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>$(venue_name) - Авторизация</title>\n    <link rel="stylesheet" href="/static/templates/dark/style.css">\n</head>\n<body>\n    <div class="container">\n        <div class="card">\n            <div class="logo">\n                <img src="$(banner_url)" alt="Логотип" onerror="this.style.display='none'">\n            </div>\n            <h1>Добро пожаловать</h1>\n            <p class="sub">Подтвердите номер телефона для доступа в интернет</p>\n            \n            $(if error_text)\n            <div class="error">$(error_text)</div>\n            $(endif)\n            \n            <form method="post" action="/portal/$(venue_id)/auth">\n                <input type="hidden" name="mac" value="$(mac)">\n                <div class="form-group">\n                    <input type="tel" name="phone" placeholder="+375 (29) XXX-XX-XX" value="$(phone)" required>\n                </div>\n                <button type="submit">Получить код</button>\n            </form>\n            <p class="hint">Код придет в SMS в течение минуты</p>\n        </div>\n    </div>\n</body>\n</html>	[]	[]	[]	t	17	2026-02-17 09:17:29.265085+00	2026-02-17 10:57:39.558411+00	2026-02-17 10:57:39.561802+00
1	auth	<!DOCTYPE html>\n<html lang="ru">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>$(venue_name) - Авторизация</title>\n    <link rel="stylesheet" href="/static/templates/dark/style.css">\n</head>\n<body>\n    <div class="container">\n        <div class="card">\n            <div class="logo">\n                <img src="$(banner_url)" alt="Логотип" onerror="this.style.display='none'">\n            </div>\n            <h1>Добро пожаловать</h1>\n            <p class="sub">Подтвердите номер телефона для доступа в интернет</p>\n            \n            $(if error_text)\n            <div class="error">$(error_text)</div>\n            $(endif)\n            \n            <form method="post" action="/portal/$(venue_id)/auth">\n                <input type="hidden" name="mac" value="$(mac)">\n                <div class="form-group">\n                    <input type="tel" name="phone" placeholder="+375 (29) XXX-XX-XX" value="$(phone)" required>\n                </div>\n                <button type="submit">Получить код</button>\n            </form>\n            <p class="hint">Код придет в SMS в течение минуты</p>\n        </div>\n    </div>\n</body>\n</html>	[]	[]	[]	f	20	2026-02-17 10:57:18.452256+00	2026-02-17 10:57:41.34156+00	2026-02-17 10:57:41.343279+00
1	welcome	<!DOCTYPE html>\n<html lang="ru">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>Добро пожаловать - $(venue_name)</title>\n    <link rel="stylesheet" href="/static/templates/dark/style.css">\n</head>\n<body>\n    <div class="container">\n        <div class="card">\n            <div class="logo">\n                <img src="$(banner_url)" alt="Логотип" onerror="this.style.display='none'">\n            </div>\n            <h1>Вы успешно авторизованы!</h1>\n            <p class="sub">Приятного использования интернета</p>\n            <p>MAC: $(mac)</p>\n        </div>\n    </div>\n</body>\n</html>	[]	[]	[]	f	21	2026-02-17 10:57:18.452256+00	2026-02-17 10:57:44.801158+00	2026-02-17 10:57:44.802796+00
1	auth	<!DOCTYPE html>\n<html lang="ru">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>$(venue_name) - Wi-Fi гостя</title>\n    <link rel="stylesheet" href="/static/templates/hotel/style.css">\n</head>\n<body>\n    <div class="header">\n        <div class="hotel-name">$(venue_name)</div>\n    </div>\n    <div class="container">\n        <div class="welcome-card">\n            <h1>Добро пожаловать!</h1>\n            <p class="subtitle">Для доступа в интернет подтвердите ваш номер телефона</p>\n            \n            $(if error_text)\n            <div class="error">$(error_text)</div>\n            $(endif)\n            \n            <form method="post" action="/portal/$(venue_id)/auth">\n                <input type="hidden" name="mac" value="$(mac)">\n                <div class="form-group">\n                    <label for="phone">Номер телефона</label>\n                    <input type="tel" id="phone" name="phone" placeholder="+375 (29) XXX-XX-XX" value="$(phone)" required>\n                </div>\n                <button type="submit">Получить SMS с кодом</button>\n            </form>\n            <p class="legal">Нажимая кнопку, вы соглашаетесь с <a href="#">правилами отеля</a></p>\n        </div>\n    </div>\n    <div class="footer">\n        <img src="$(banner_url)" alt="Партнеры" class="partners">\n    </div>\n</body>\n</html>	[]	[]	[]	t	22	2026-02-17 10:57:50.215354+00	2026-02-17 10:58:02.325433+00	\N
1	welcome	<!DOCTYPE html>\n<html lang="ru">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>Добро пожаловать - $(venue_name)</title>\n    <link rel="stylesheet" href="/static/templates/hotel/style.css">\n</head>\n<body>\n    <div class="header">\n        <div class="hotel-name">$(venue_name)</div>\n    </div>\n    <div class="container">\n        <div class="welcome-card">\n            <h1>Вы успешно авторизованы!</h1>\n            <p class="subtitle">Приятного отдыха в нашем отеле</p>\n            <p>MAC адрес: $(mac)</p>\n        </div>\n    </div>\n    <div class="footer">\n        <img src="$(banner_url)" alt="Партнеры" class="partners">\n    </div>\n</body>\n</html>	[]	[]	[]	t	23	2026-02-17 10:57:50.215354+00	2026-02-17 10:58:13.270817+00	\N
\.


--
-- Data for Name: sessions; Type: TABLE DATA; Schema: public; Owner: wifi_user
--

COPY public.sessions (user_profile_id, venue_id, nas_id, mac_address, ip_address, session_start, session_end, traffic_in_bytes, traffic_out_bytes, is_active, id, created_at, updated_at, deleted_at) FROM stdin;
\.


--
-- Data for Name: settings; Type: TABLE DATA; Schema: public; Owner: wifi_user
--

COPY public.settings (id, key, value, description, created_at, updated_at, deleted_at) FROM stdin;
1	telegram_bot_token	8514356755:AAEgQP1fFR3SIdc72_h7tr_iSrsRFlkTwY4	\N	2026-02-16 14:56:41.397438+00	2026-02-16 15:02:06.052335+00	\N
3	telegram_bot_webhook_url	https://supreme-space-palm-tree-94pw9444xpf779j-8080.app.github.dev/webhook	\N	2026-02-16 14:56:41.415627+00	2026-02-16 15:02:06.096087+00	\N
2	telegram_bot_username	wifi_multiauth_bot	\N	2026-02-16 14:56:41.404042+00	2026-02-16 15:02:06.120053+00	\N
\.


--
-- Data for Name: sms_codes; Type: TABLE DATA; Schema: public; Owner: wifi_user
--

COPY public.sms_codes (phone_number, code, is_used, expires_at, attempts, id, created_at, updated_at, deleted_at, venue_id, method, call_id, provider_id) FROM stdin;
71234567890	8810	f	2026-02-16 09:41:12.363718+00	0	1	2026-02-16 09:36:12.359086+00	\N	\N	1	SMS	\N	\N
\.


--
-- Data for Name: sms_providers; Type: TABLE DATA; Schema: public; Owner: wifi_user
--

COPY public.sms_providers (name, is_active, config, id, created_at, updated_at, deleted_at, type, priority) FROM stdin;
ау	t	{"username": "dsf", "password_md5": "dff", "sender": "dfs"}	3	2026-02-16 14:11:26.175596+00	2026-02-17 09:18:01.593089+00	\N	ROCKETSMS	0
масм	t	{"api_key": "\\u0432\\u0430\\u0432\\u043f", "api_secret": "\\u044b\\u043f\\u0432\\u0440"}	4	2026-02-17 14:34:32.583355+00	\N	\N	CALLPASSWORD	0
ef	t	{"user": "ef", "apikey": "fe", "sender": "few"}	5	2026-02-17 14:52:14.631597+00	\N	\N	WEBSMS	0
\.


--
-- Data for Name: tariff_plans; Type: TABLE DATA; Schema: public; Owner: wifi_user
--

COPY public.tariff_plans (id, name, description, price, currency, duration_hours, speed_limit_up_kbps, speed_limit_down_kbps, is_active, created_at, updated_at, deleted_at) FROM stdin;
\.


--
-- Data for Name: user_profiles; Type: TABLE DATA; Schema: public; Owner: wifi_user
--

COPY public.user_profiles (mac_address, phone_number, email, first_seen, last_seen, total_sessions, total_traffic_bytes, is_blocked, is_vip, device_oui, id, created_at, updated_at, deleted_at, venue_id, current_tariff_id, tariff_expires_at, full_name, marketing_consent) FROM stdin;
AA:BB:CC:DD:EE:FF	+375444677737	\N	2026-02-16 15:52:11.265489+00	2026-02-16 18:16:35.23833+00	0	0	f	f	\N	1	2026-02-16 15:52:11.263067+00	2026-02-16 18:16:35.232719+00	\N	1	\N	\N	\N	f
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: wifi_user
--

COPY public.users (id, email, hashed_password, is_active, is_superuser, role, created_at, venue_id) FROM stdin;
1	admin@example.com	$2b$12$paOCBSUOUeijvcK3g1sXqO8UfZolY5DTAk68pHRb1y5CwWhp7aqEO	t	t	admin	2026-02-14 19:59:32.678067+00	\N
2	user@example.com	$2b$12$9cFhChgAljbxic1g0XMNZu07C6k8cPsxyPN5D6wDzzrMPV1El9tKm	t	f	admin	2026-02-15 19:27:47.707443+00	\N
4	owner@we.by	$2b$12$p.ZWLjul3THHTchg2GsDbOgm0f6ujX2aKIOiQGoVm0nP9qr1DcV3u	t	f	venue_owner	2026-02-15 19:31:06.933494+00	1
5	tex@dfdddg.fb	$2b$12$GZrlvaDKsV.XwDjxO0B2BeWsqEF410CUY5hCJenEVHcQZ3X35gab6	t	f	support	2026-02-15 19:31:29.647838+00	\N
6	mar@dfdf.jhg	$2b$12$wtasEP./aC6/BtzHBbH3geoJxrqyXFkRZY3Gtr8WKGqVR9xh67j4O	t	f	marketing	2026-02-15 19:32:02.04611+00	\N
\.


--
-- Data for Name: venue_crm; Type: TABLE DATA; Schema: public; Owner: wifi_user
--

COPY public.venue_crm (venue_id, crm_provider_id, is_active, config_override, created_at) FROM stdin;
\.


--
-- Data for Name: venue_tariff; Type: TABLE DATA; Schema: public; Owner: wifi_user
--

COPY public.venue_tariff (venue_id, tariff_id, priority, is_available, created_at) FROM stdin;
\.


--
-- Data for Name: venues; Type: TABLE DATA; Schema: public; Owner: wifi_user
--

COPY public.venues (id, name, description, address, contact_phone, contact_email, is_active, created_at, updated_at, deleted_at, domain, ssl_enabled) FROM stdin;
1	test frjhмпвввв	jncdjn	nljnl	jlnln	ljnlkn@nl.rt	t	2026-02-15 19:10:24.057056+00	\N	\N	exampli.com	f
\.


--
-- Data for Name: wireguard_peers; Type: TABLE DATA; Schema: public; Owner: wifi_user
--

COPY public.wireguard_peers (nas_device_id, public_key, allowed_ips, endpoint, is_active, id, created_at, updated_at, deleted_at) FROM stdin;
\.


--
-- Name: bgw_job_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: wifi_user
--

SELECT pg_catalog.setval('_timescaledb_catalog.bgw_job_id_seq', 1000, false);


--
-- Name: chunk_column_stats_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: wifi_user
--

SELECT pg_catalog.setval('_timescaledb_catalog.chunk_column_stats_id_seq', 1, false);


--
-- Name: chunk_constraint_name; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: wifi_user
--

SELECT pg_catalog.setval('_timescaledb_catalog.chunk_constraint_name', 1, false);


--
-- Name: chunk_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: wifi_user
--

SELECT pg_catalog.setval('_timescaledb_catalog.chunk_id_seq', 1, false);


--
-- Name: continuous_agg_migrate_plan_step_step_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: wifi_user
--

SELECT pg_catalog.setval('_timescaledb_catalog.continuous_agg_migrate_plan_step_step_id_seq', 1, false);


--
-- Name: dimension_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: wifi_user
--

SELECT pg_catalog.setval('_timescaledb_catalog.dimension_id_seq', 1, true);


--
-- Name: dimension_slice_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: wifi_user
--

SELECT pg_catalog.setval('_timescaledb_catalog.dimension_slice_id_seq', 1, false);


--
-- Name: hypertable_id_seq; Type: SEQUENCE SET; Schema: _timescaledb_catalog; Owner: wifi_user
--

SELECT pg_catalog.setval('_timescaledb_catalog.hypertable_id_seq', 1, true);


--
-- Name: audit_logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wifi_user
--

SELECT pg_catalog.setval('public.audit_logs_id_seq', 145, true);


--
-- Name: banners_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wifi_user
--

SELECT pg_catalog.setval('public.banners_id_seq', 2, true);


--
-- Name: crm_providers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wifi_user
--

SELECT pg_catalog.setval('public.crm_providers_id_seq', 1, false);


--
-- Name: events_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wifi_user
--

SELECT pg_catalog.setval('public.events_id_seq', 1, false);


--
-- Name: local_users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wifi_user
--

SELECT pg_catalog.setval('public.local_users_id_seq', 1, false);


--
-- Name: nas_devices_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wifi_user
--

SELECT pg_catalog.setval('public.nas_devices_id_seq', 15, true);


--
-- Name: nas_status_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wifi_user
--

SELECT pg_catalog.setval('public.nas_status_history_id_seq', 1, false);


--
-- Name: netflow_records_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wifi_user
--

SELECT pg_catalog.setval('public.netflow_records_id_seq', 1, false);


--
-- Name: portal_templates_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wifi_user
--

SELECT pg_catalog.setval('public.portal_templates_id_seq', 23, true);


--
-- Name: sessions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wifi_user
--

SELECT pg_catalog.setval('public.sessions_id_seq', 1, false);


--
-- Name: settings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wifi_user
--

SELECT pg_catalog.setval('public.settings_id_seq', 3, true);


--
-- Name: sms_codes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wifi_user
--

SELECT pg_catalog.setval('public.sms_codes_id_seq', 1, true);


--
-- Name: sms_providers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wifi_user
--

SELECT pg_catalog.setval('public.sms_providers_id_seq', 5, true);


--
-- Name: tariff_plans_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wifi_user
--

SELECT pg_catalog.setval('public.tariff_plans_id_seq', 1, false);


--
-- Name: user_profiles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wifi_user
--

SELECT pg_catalog.setval('public.user_profiles_id_seq', 1, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wifi_user
--

SELECT pg_catalog.setval('public.users_id_seq', 6, true);


--
-- Name: venues_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wifi_user
--

SELECT pg_catalog.setval('public.venues_id_seq', 1, true);


--
-- Name: wireguard_peers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: wifi_user
--

SELECT pg_catalog.setval('public.wireguard_peers_id_seq', 2, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: audit_logs audit_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT audit_logs_pkey PRIMARY KEY (id);


--
-- Name: banners banners_pkey; Type: CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.banners
    ADD CONSTRAINT banners_pkey PRIMARY KEY (id);


--
-- Name: crm_providers crm_providers_pkey; Type: CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.crm_providers
    ADD CONSTRAINT crm_providers_pkey PRIMARY KEY (id);


--
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (id);


--
-- Name: local_users local_users_pkey; Type: CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.local_users
    ADD CONSTRAINT local_users_pkey PRIMARY KEY (id);


--
-- Name: nas_devices nas_devices_ip_address_key; Type: CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.nas_devices
    ADD CONSTRAINT nas_devices_ip_address_key UNIQUE (ip_address);


--
-- Name: nas_devices nas_devices_pkey; Type: CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.nas_devices
    ADD CONSTRAINT nas_devices_pkey PRIMARY KEY (id);


--
-- Name: nas_status_history nas_status_history_pkey; Type: CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.nas_status_history
    ADD CONSTRAINT nas_status_history_pkey PRIMARY KEY (id);


--
-- Name: netflow_records netflow_records_pkey; Type: CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.netflow_records
    ADD CONSTRAINT netflow_records_pkey PRIMARY KEY ("time", id);


--
-- Name: portal_templates portal_templates_pkey; Type: CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.portal_templates
    ADD CONSTRAINT portal_templates_pkey PRIMARY KEY (id);


--
-- Name: sessions sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_pkey PRIMARY KEY (id);


--
-- Name: settings settings_key_key; Type: CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.settings
    ADD CONSTRAINT settings_key_key UNIQUE (key);


--
-- Name: settings settings_pkey; Type: CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.settings
    ADD CONSTRAINT settings_pkey PRIMARY KEY (id);


--
-- Name: sms_codes sms_codes_pkey; Type: CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.sms_codes
    ADD CONSTRAINT sms_codes_pkey PRIMARY KEY (id);


--
-- Name: sms_providers sms_providers_pkey; Type: CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.sms_providers
    ADD CONSTRAINT sms_providers_pkey PRIMARY KEY (id);


--
-- Name: tariff_plans tariff_plans_pkey; Type: CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.tariff_plans
    ADD CONSTRAINT tariff_plans_pkey PRIMARY KEY (id);


--
-- Name: user_profiles user_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.user_profiles
    ADD CONSTRAINT user_profiles_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: venue_crm venue_crm_pkey; Type: CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.venue_crm
    ADD CONSTRAINT venue_crm_pkey PRIMARY KEY (venue_id, crm_provider_id);


--
-- Name: venue_tariff venue_tariff_pkey; Type: CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.venue_tariff
    ADD CONSTRAINT venue_tariff_pkey PRIMARY KEY (venue_id, tariff_id);


--
-- Name: venues venues_domain_key; Type: CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.venues
    ADD CONSTRAINT venues_domain_key UNIQUE (domain);


--
-- Name: venues venues_pkey; Type: CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.venues
    ADD CONSTRAINT venues_pkey PRIMARY KEY (id);


--
-- Name: wireguard_peers wireguard_peers_nas_device_id_key; Type: CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.wireguard_peers
    ADD CONSTRAINT wireguard_peers_nas_device_id_key UNIQUE (nas_device_id);


--
-- Name: wireguard_peers wireguard_peers_pkey; Type: CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.wireguard_peers
    ADD CONSTRAINT wireguard_peers_pkey PRIMARY KEY (id);


--
-- Name: ix_audit_logs_id; Type: INDEX; Schema: public; Owner: wifi_user
--

CREATE INDEX ix_audit_logs_id ON public.audit_logs USING btree (id);


--
-- Name: ix_banners_id; Type: INDEX; Schema: public; Owner: wifi_user
--

CREATE INDEX ix_banners_id ON public.banners USING btree (id);


--
-- Name: ix_crm_providers_id; Type: INDEX; Schema: public; Owner: wifi_user
--

CREATE INDEX ix_crm_providers_id ON public.crm_providers USING btree (id);


--
-- Name: ix_events_id; Type: INDEX; Schema: public; Owner: wifi_user
--

CREATE INDEX ix_events_id ON public.events USING btree (id);


--
-- Name: ix_local_users_id; Type: INDEX; Schema: public; Owner: wifi_user
--

CREATE INDEX ix_local_users_id ON public.local_users USING btree (id);


--
-- Name: ix_local_users_username; Type: INDEX; Schema: public; Owner: wifi_user
--

CREATE UNIQUE INDEX ix_local_users_username ON public.local_users USING btree (username);


--
-- Name: ix_nas_devices_id; Type: INDEX; Schema: public; Owner: wifi_user
--

CREATE INDEX ix_nas_devices_id ON public.nas_devices USING btree (id);


--
-- Name: ix_nas_status_history_id; Type: INDEX; Schema: public; Owner: wifi_user
--

CREATE INDEX ix_nas_status_history_id ON public.nas_status_history USING btree (id);


--
-- Name: ix_netflow_records_id; Type: INDEX; Schema: public; Owner: wifi_user
--

CREATE INDEX ix_netflow_records_id ON public.netflow_records USING btree (id);


--
-- Name: ix_portal_templates_id; Type: INDEX; Schema: public; Owner: wifi_user
--

CREATE INDEX ix_portal_templates_id ON public.portal_templates USING btree (id);


--
-- Name: ix_sessions_id; Type: INDEX; Schema: public; Owner: wifi_user
--

CREATE INDEX ix_sessions_id ON public.sessions USING btree (id);


--
-- Name: ix_sessions_mac_address; Type: INDEX; Schema: public; Owner: wifi_user
--

CREATE INDEX ix_sessions_mac_address ON public.sessions USING btree (mac_address);


--
-- Name: ix_settings_id; Type: INDEX; Schema: public; Owner: wifi_user
--

CREATE INDEX ix_settings_id ON public.settings USING btree (id);


--
-- Name: ix_settings_key; Type: INDEX; Schema: public; Owner: wifi_user
--

CREATE UNIQUE INDEX ix_settings_key ON public.settings USING btree (key);


--
-- Name: ix_sms_codes_id; Type: INDEX; Schema: public; Owner: wifi_user
--

CREATE INDEX ix_sms_codes_id ON public.sms_codes USING btree (id);


--
-- Name: ix_sms_codes_phone_number; Type: INDEX; Schema: public; Owner: wifi_user
--

CREATE INDEX ix_sms_codes_phone_number ON public.sms_codes USING btree (phone_number);


--
-- Name: ix_sms_providers_id; Type: INDEX; Schema: public; Owner: wifi_user
--

CREATE INDEX ix_sms_providers_id ON public.sms_providers USING btree (id);


--
-- Name: ix_tariff_plans_id; Type: INDEX; Schema: public; Owner: wifi_user
--

CREATE INDEX ix_tariff_plans_id ON public.tariff_plans USING btree (id);


--
-- Name: ix_user_profiles_id; Type: INDEX; Schema: public; Owner: wifi_user
--

CREATE INDEX ix_user_profiles_id ON public.user_profiles USING btree (id);


--
-- Name: ix_user_profiles_mac_address; Type: INDEX; Schema: public; Owner: wifi_user
--

CREATE UNIQUE INDEX ix_user_profiles_mac_address ON public.user_profiles USING btree (mac_address);


--
-- Name: ix_user_profiles_phone_number; Type: INDEX; Schema: public; Owner: wifi_user
--

CREATE INDEX ix_user_profiles_phone_number ON public.user_profiles USING btree (phone_number);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: wifi_user
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: wifi_user
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: ix_venue_crm_crm_provider_id; Type: INDEX; Schema: public; Owner: wifi_user
--

CREATE INDEX ix_venue_crm_crm_provider_id ON public.venue_crm USING btree (crm_provider_id);


--
-- Name: ix_venue_crm_venue_id; Type: INDEX; Schema: public; Owner: wifi_user
--

CREATE INDEX ix_venue_crm_venue_id ON public.venue_crm USING btree (venue_id);


--
-- Name: ix_venue_tariff_tariff_id; Type: INDEX; Schema: public; Owner: wifi_user
--

CREATE INDEX ix_venue_tariff_tariff_id ON public.venue_tariff USING btree (tariff_id);


--
-- Name: ix_venue_tariff_venue_id; Type: INDEX; Schema: public; Owner: wifi_user
--

CREATE INDEX ix_venue_tariff_venue_id ON public.venue_tariff USING btree (venue_id);


--
-- Name: ix_venues_id; Type: INDEX; Schema: public; Owner: wifi_user
--

CREATE INDEX ix_venues_id ON public.venues USING btree (id);


--
-- Name: ix_wireguard_peers_id; Type: INDEX; Schema: public; Owner: wifi_user
--

CREATE INDEX ix_wireguard_peers_id ON public.wireguard_peers USING btree (id);


--
-- Name: audit_logs audit_logs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT audit_logs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: banners banners_venue_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.banners
    ADD CONSTRAINT banners_venue_id_fkey FOREIGN KEY (venue_id) REFERENCES public.venues(id);


--
-- Name: events events_user_profile_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_user_profile_id_fkey FOREIGN KEY (user_profile_id) REFERENCES public.user_profiles(id);


--
-- Name: events events_venue_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_venue_id_fkey FOREIGN KEY (venue_id) REFERENCES public.venues(id);


--
-- Name: user_profiles fk_user_profiles_tariff_id; Type: FK CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.user_profiles
    ADD CONSTRAINT fk_user_profiles_tariff_id FOREIGN KEY (current_tariff_id) REFERENCES public.tariff_plans(id);


--
-- Name: local_users local_users_user_profile_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.local_users
    ADD CONSTRAINT local_users_user_profile_id_fkey FOREIGN KEY (user_profile_id) REFERENCES public.user_profiles(id);


--
-- Name: local_users local_users_venue_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.local_users
    ADD CONSTRAINT local_users_venue_id_fkey FOREIGN KEY (venue_id) REFERENCES public.venues(id);


--
-- Name: nas_devices nas_devices_venue_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.nas_devices
    ADD CONSTRAINT nas_devices_venue_id_fkey FOREIGN KEY (venue_id) REFERENCES public.venues(id);


--
-- Name: nas_status_history nas_status_history_nas_device_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.nas_status_history
    ADD CONSTRAINT nas_status_history_nas_device_id_fkey FOREIGN KEY (nas_device_id) REFERENCES public.nas_devices(id);


--
-- Name: netflow_records netflow_records_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.netflow_records
    ADD CONSTRAINT netflow_records_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.sessions(id);


--
-- Name: portal_templates portal_templates_venue_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.portal_templates
    ADD CONSTRAINT portal_templates_venue_id_fkey FOREIGN KEY (venue_id) REFERENCES public.venues(id);


--
-- Name: sessions sessions_nas_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_nas_id_fkey FOREIGN KEY (nas_id) REFERENCES public.nas_devices(id);


--
-- Name: sessions sessions_user_profile_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_user_profile_id_fkey FOREIGN KEY (user_profile_id) REFERENCES public.user_profiles(id);


--
-- Name: sessions sessions_venue_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_venue_id_fkey FOREIGN KEY (venue_id) REFERENCES public.venues(id);


--
-- Name: sms_codes sms_codes_provider_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.sms_codes
    ADD CONSTRAINT sms_codes_provider_id_fkey FOREIGN KEY (provider_id) REFERENCES public.sms_providers(id);


--
-- Name: sms_codes sms_codes_venue_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.sms_codes
    ADD CONSTRAINT sms_codes_venue_id_fkey FOREIGN KEY (venue_id) REFERENCES public.venues(id);


--
-- Name: user_profiles user_profiles_venue_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.user_profiles
    ADD CONSTRAINT user_profiles_venue_id_fkey FOREIGN KEY (venue_id) REFERENCES public.venues(id);


--
-- Name: users users_venue_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_venue_id_fkey FOREIGN KEY (venue_id) REFERENCES public.venues(id);


--
-- Name: venue_crm venue_crm_crm_provider_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.venue_crm
    ADD CONSTRAINT venue_crm_crm_provider_id_fkey FOREIGN KEY (crm_provider_id) REFERENCES public.crm_providers(id) ON DELETE CASCADE;


--
-- Name: venue_crm venue_crm_venue_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.venue_crm
    ADD CONSTRAINT venue_crm_venue_id_fkey FOREIGN KEY (venue_id) REFERENCES public.venues(id) ON DELETE CASCADE;


--
-- Name: venue_tariff venue_tariff_tariff_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.venue_tariff
    ADD CONSTRAINT venue_tariff_tariff_id_fkey FOREIGN KEY (tariff_id) REFERENCES public.tariff_plans(id) ON DELETE CASCADE;


--
-- Name: venue_tariff venue_tariff_venue_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.venue_tariff
    ADD CONSTRAINT venue_tariff_venue_id_fkey FOREIGN KEY (venue_id) REFERENCES public.venues(id) ON DELETE CASCADE;


--
-- Name: wireguard_peers wireguard_peers_nas_device_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wifi_user
--

ALTER TABLE ONLY public.wireguard_peers
    ADD CONSTRAINT wireguard_peers_nas_device_id_fkey FOREIGN KEY (nas_device_id) REFERENCES public.nas_devices(id);


--
-- PostgreSQL database dump complete
--

