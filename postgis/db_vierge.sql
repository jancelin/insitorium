
CREATE DATABASE insitorium
    WITH
    OWNER = admin
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

ALTER DATABASE insitorium
    SET search_path TO '"$user", public, topology';
-- Table: public.point

-- DROP TABLE public.point;

CREATE TABLE public.point
(
    id serial,
    geom geometry(PointZ,4171),
    hauteur numeric,
    ordre integer,
    rayon numeric,
    texte character varying(25) COLLATE pg_catalog."default",
    central boolean,
    ausol boolean,
    CONSTRAINT pk_point PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.point
    OWNER to admin;

-- Index: idx_geom

-- DROP INDEX public.idx_geom;

CREATE INDEX idx_geom
    ON public.point USING gist
    (geom gist_geometry_ops)
    TABLESPACE pg_default;

    -- Table: public.user_position

    -- DROP TABLE public.user_position;

    CREATE TABLE public.user_position
    (
        id serial,
        user_ins character varying COLLATE pg_catalog."default",
        dat numeric,
        lati numeric,
        longi numeric,
        height numeric,
        direct numeric,
        CONSTRAINT id_user_insitorium PRIMARY KEY (id)
    )
    WITH (
        OIDS = FALSE
    )
    TABLESPACE pg_default;

    ALTER TABLE public.user_position
        OWNER to admin;

    GRANT ALL ON TABLE public.user_position TO admin;

    GRANT SELECT ON TABLE public.user_position TO replicator;

    -- Index: inx_user_pos

    -- DROP INDEX public.inx_user_pos;

    CREATE INDEX inx_user_pos
        ON public.user_position USING btree
        (id DESC)
        TABLESPACE pg_default;
        
    -- Table: public.sound

-- DROP TABLE public.sound;

CREATE TABLE public.sound
(
    id serial,
    name_sound character varying(50) COLLATE pg_catalog."default" NOT NULL,
    name_ext character varying(60) COLLATE pg_catalog."default",
    where_file character varying(70) COLLATE pg_catalog."default" NOT NULL,
    description character varying(100) COLLATE pg_catalog."default",
    CONSTRAINT sound_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.sound
    OWNER to admin;

GRANT ALL ON TABLE public.sound TO admin;
