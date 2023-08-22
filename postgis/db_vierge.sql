
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

-- DROP TABLE public.point2;

CREATE TABLE IF NOT EXISTS public.point2
(
    id integer NOT NULL DEFAULT nextval('point2_id_seq'::regclass),
    geom geometry(Point,4171),
    rayon numeric,
    texte character varying(25) COLLATE pg_catalog."default",
    CONSTRAINT pk_point2 PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.point2
    OWNER to admin;

-- Index: idx_geom

-- DROP INDEX public.idx_geom;

CREATE INDEX idx_geom
    ON public.point2 USING gist
    (geom gist_geometry_ops)
    TABLESPACE pg_default;

CREATE OR REPLACE VIEW public.bufferpoint2
 AS
 SELECT p.id,
    p.texte,
    st_buffer(p.geom::geography, p.rayon::double precision, 35) AS buffer
   FROM point2 p;

ALTER TABLE public.bufferpoint2
    OWNER TO admin;

GRANT ALL ON TABLE public.bufferpoint2 TO admin;
