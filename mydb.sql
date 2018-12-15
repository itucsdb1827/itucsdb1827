--
-- PostgreSQL database dump
--

-- Dumped from database version 10.6 (Ubuntu 10.6-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.6 (Ubuntu 10.6-0ubuntu0.18.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: bets_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.bets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.bets_id_seq OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: bets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bets (
    id integer DEFAULT nextval('public.bets_id_seq'::regclass) NOT NULL,
    user_id integer,
    amount integer NOT NULL,
    typeof character varying(16) NOT NULL,
    answer double precision NOT NULL,
    clan_id integer,
    question_id integer
);


ALTER TABLE public.bets OWNER TO postgres;

--
-- Name: clans; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clans (
    id integer NOT NULL,
    headofclan integer,
    points integer DEFAULT 0,
    clanname character varying(16)
);


ALTER TABLE public.clans OWNER TO postgres;

--
-- Name: clans_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.clans_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.clans_id_seq OWNER TO postgres;

--
-- Name: clans_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.clans_id_seq OWNED BY public.clans.id;


--
-- Name: messages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.messages (
    user_id integer NOT NULL,
    message_id integer NOT NULL,
    sendtime timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    message text NOT NULL,
    replyof integer,
    problem_id integer NOT NULL,
    typeofmessage character varying(16) NOT NULL,
    clan_id integer,
    containanswer boolean DEFAULT false,
    imagepath character varying(200),
    reportnum integer DEFAULT 0
);


ALTER TABLE public.messages OWNER TO postgres;

--
-- Name: messages_message_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.messages_message_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.messages_message_id_seq OWNER TO postgres;

--
-- Name: messages_message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.messages_message_id_seq OWNED BY public.messages.message_id;


--
-- Name: problems; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.problems (
    user_id integer NOT NULL,
    id integer NOT NULL,
    senddate timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    title character varying(30) NOT NULL,
    question text NOT NULL,
    totalcollectedpoints integer NOT NULL,
    answer double precision,
    isanswered boolean DEFAULT false,
    topic character varying(15) NOT NULL,
    giventime character varying(15),
    typeof character varying NOT NULL,
    clan_id integer
);


ALTER TABLE public.problems OWNER TO postgres;

--
-- Name: problems_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.problems_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.problems_id_seq OWNER TO postgres;

--
-- Name: problems_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.problems_id_seq OWNED BY public.problems.id;


--
-- Name: request; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.request (
    id integer NOT NULL,
    user_id integer,
    clan_id integer
);


ALTER TABLE public.request OWNER TO postgres;

--
-- Name: request_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.request_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.request_id_seq OWNER TO postgres;

--
-- Name: request_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.request_id_seq OWNED BY public.request.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(16) NOT NULL,
    pass_word character varying(87) NOT NULL,
    avatarpath character varying(200) NOT NULL,
    email character varying(30) NOT NULL,
    points integer DEFAULT 100 NOT NULL,
    clannumber integer,
    dateofjoin timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    adminof character varying(16),
    isactive boolean NOT NULL,
    headofclan boolean DEFAULT false NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: clans id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clans ALTER COLUMN id SET DEFAULT nextval('public.clans_id_seq'::regclass);


--
-- Name: messages message_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages ALTER COLUMN message_id SET DEFAULT nextval('public.messages_message_id_seq'::regclass);


--
-- Name: problems id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.problems ALTER COLUMN id SET DEFAULT nextval('public.problems_id_seq'::regclass);


--
-- Name: request id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.request ALTER COLUMN id SET DEFAULT nextval('public.request_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: bets; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bets (id, user_id, amount, typeof, answer, clan_id, question_id) FROM stdin;
\.


--
-- Data for Name: clans; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.clans (id, headofclan, points, clanname) FROM stdin;
3	9	1000	clanx
\.


--
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.messages (user_id, message_id, sendtime, message, replyof, problem_id, typeofmessage, clan_id, containanswer, imagepath, reportnum) FROM stdin;
\.


--
-- Data for Name: problems; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.problems (user_id, id, senddate, title, question, totalcollectedpoints, answer, isanswered, topic, giventime, typeof, clan_id) FROM stdin;
\.


--
-- Data for Name: request; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.request (id, user_id, clan_id) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, pass_word, avatarpath, email, points, clannumber, dateofjoin, adminof, isactive, headofclan) FROM stdin;
5	123456	$pbkdf2-sha256$29000$MUaotZYyJuRcq/W.11rr/Q$nfaOhiCc6/PP68oav3yYMuU.iKS7QTN7poSDgLPbTlQ	z.jpg	mehmet.caglayan8@gmail.com	100	\N	2018-11-01 12:48:13.302696	\N	t	f
7	qazwsxedc	$pbkdf2-sha256$29000$KcX4v7eW0to7B0DIOeccAw$DjneA1wkWOrWjJgEN5a0z6J4I/mUK8IR5Ub.fsJjNtU	4.png	mehmet.caglayan@gmail.co	100	\N	2018-11-01 14:21:10.170942	\N	t	f
29	qazzaq	$pbkdf2-sha256$29000$Tcl5L8V4T2mNEUKIkZISog$YuakeJIh831YwJVqZ1W0ZWHZBAjPtuLdpDToJzPkY20	y.png2018-12-14 14:35:06.943973	123@gmail.com	100	3	2018-12-07 17:14:34.524163	ds	f	f
24	987654	$pbkdf2-sha256$29000$QYjxPgcgBMA4x9jbG.M8Zw$eOupD1xTpvHkewD2ulNHb24arYW9o5CyNW.KYjk4r4w	a.png	mehmet.caglayan8@gma	100	\N	2018-11-03 11:35:30.931272	\N	t	f
27	staticx	$pbkdf2-sha256$29000$zrl37r2XknKuVUqplfK.tw$YIh3rb2rpbFEYLyy/dCJb3cmG9yRWryMBx2YFYvbnyc	z.jpg2018-11-05 10:09:19.360291	sx@g.com	100	\N	2018-11-05 10:09:19.362114	\N	t	f
9	asdf12	$pbkdf2-sha256$29000$PCfEOMcYY0wpBQDAOIfw3g$g04YbnZYoZBTs2Yq3YDTHJoQ/CUnTI7U690NqZdGzG0	1.png	qaz@hotmail.com	1231676	3	2018-11-01 16:18:32.071093	general	t	t
3	hello	asdd	as	email	100	\N	2018-10-25 21:38:10.530554	\N	t	f
35	deneme	$pbkdf2-sha256$29000$AaB0rjXGuHeOsVbKOSdEqA$NayJEBc2CV3Ue5iWwcKQdirM6.X0WedKKG59ChiVyE0	2.PNG2018-12-14 15:24:15.775723	dene@gmail.com	100	\N	2018-12-14 15:24:15.775932	algo	f	f
30	paused	$pbkdf2-sha256$29000$bA0BoJSS0vq/V2oNYax1rg$sVEEE3G5V5YXK1uW/HwzhnsEN1.QpFdM6bmUGcdzhzo	y.png2018-12-11 13:03:12.911395	p@gmail.com	100	\N	2018-12-11 13:03:12.911677	\N	f	f
28	powerade	$pbkdf2-sha256$29000$QChlrLWWMoaQspaydg4hJA$8.pHQwxz37ZpvgwiP9nzDkyZqha1Dm9kguFVvpuLgc0	1.png2018-11-06 14:35:48.167844	123123@hot.com	100	\N	2018-11-06 14:18:24.60286	\N	f	f
31	123123	$pbkdf2-sha256$29000$3ltrTck5B6BUipHyPgfAuA$UyJNtLrYv1aoM9irSYBLKFpd8QWlvZrtoBbBc8tLiLs	1.png2018-12-11 15:44:43.772836	123123@aaa.com	100	\N	2018-12-11 15:44:43.773035	\N	f	f
\.


--
-- Name: bets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.bets_id_seq', 22, true);


--
-- Name: clans_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.clans_id_seq', 3, true);


--
-- Name: messages_message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.messages_message_id_seq', 78, true);


--
-- Name: problems_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.problems_id_seq', 32, true);


--
-- Name: request_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.request_id_seq', 3, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 35, true);


--
-- Name: bets bets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bets
    ADD CONSTRAINT bets_pkey PRIMARY KEY (id);


--
-- Name: clans clans_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clans
    ADD CONSTRAINT clans_pkey PRIMARY KEY (id);


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (message_id);


--
-- Name: problems problems_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.problems
    ADD CONSTRAINT problems_pkey PRIMARY KEY (id);


--
-- Name: request request_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.request
    ADD CONSTRAINT request_pkey PRIMARY KEY (id);


--
-- Name: users users_avatarpath_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_avatarpath_key UNIQUE (avatarpath);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_un; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_un UNIQUE (username);


--
-- Name: bets bets_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bets
    ADD CONSTRAINT bets_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: clans clans_headofclan_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clans
    ADD CONSTRAINT clans_headofclan_fkey FOREIGN KEY (headofclan) REFERENCES public.users(id);


--
-- Name: bets fk_somename; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bets
    ADD CONSTRAINT fk_somename FOREIGN KEY (question_id) REFERENCES public.problems(id);


--
-- Name: messages messages_clan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_clan_id_fkey FOREIGN KEY (clan_id) REFERENCES public.clans(id);


--
-- Name: messages messages_problem_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_problem_id_fkey FOREIGN KEY (problem_id) REFERENCES public.problems(id);


--
-- Name: messages messages_replyof_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_replyof_fkey FOREIGN KEY (replyof) REFERENCES public.messages(message_id) ON DELETE RESTRICT;


--
-- Name: messages messages_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: problems problems_clan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.problems
    ADD CONSTRAINT problems_clan_id_fkey FOREIGN KEY (clan_id) REFERENCES public.clans(id);


--
-- Name: problems problems_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.problems
    ADD CONSTRAINT problems_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: request request_clan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.request
    ADD CONSTRAINT request_clan_id_fkey FOREIGN KEY (clan_id) REFERENCES public.clans(id);


--
-- Name: request request_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.request
    ADD CONSTRAINT request_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: users users_clannumber_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_clannumber_fkey FOREIGN KEY (clannumber) REFERENCES public.clans(id);


--
-- PostgreSQL database dump complete
--

