# Location of music on your computer

import pygame
import os
from pygame.locals import *
import pg8000.native
import time

MUSIC_PATH = "./son/all/"

HOST = "localhost"
PORT = 5432
USER = "geobeat"
PASSWORD = "password"
DATABASE = "insitorium"

list_sound = []
list_volume =[]
list_play = []
list_stop = []
old_sound = []

def database():
    global res
    global res_pos
    # Connect to an existing database
    conn = pg8000.native.Connection(USER,host=HOST, port=8090, database=DATABASE, password=PASSWORD)
    QUERY = """--Requête de calcul de la distance 3D entre l'antenne et tout les points de son
    --exclusion des positions hors du buffer de son (rayon)
    --Calcul du %de volume du son
    SELECT
    *,
    ROUND(100-((a.dist_m * 100)/a.rayon)) prcent_vol --Calcul du %de volume du son
    FROM
    (SELECT
    	p.id,
    	p.texte || '.wav' song_file,
    	ROUND(
    		ST_3DDistance(
    			ST_Transform(p.geom,2154),
    			ST_Transform(
    				ST_SetSRID(
                        ST_MakePoint(pos.longi,pos.lati,pos.height)
    				, 4171)
    				,2154)
    	)::NUMERIC,2) as dist_m,
     	rayon
		FROM public.point p,
        --(SELECT longi ,lati, height FROM public.user_position ORDER BY id DESC LIMIT 1) pos
		(SELECT longi ,lati, height FROM public.user_position  ORDER BY id DESC LIMIT 1) pos
	) a
    WHERE a.dist_m < a.rayon
    ORDER BY prcent_vol DESC"""

    res =  conn.run(QUERY)
    print(res)
    conn.close()

def query():
    global list_play
    global list_volume
    global list_sound
    list_sound = []
    list_volume =[]
    list_play = []
    database()
    pygame.mixer.pre_init(44100, -16, 6, 1024*4)
    pygame.mixer.init()
    pygame.init()
    #get song2play from database()
    for row in res:
        cmd1 = "sound"
        cmd2 = " = pygame.mixer.Sound('"
        cmd3 = "')"
        cmd4 = ".set_volume("
        cmd5 = ")"
        cmd_sound = cmd1+str(row[0])+cmd2+MUSIC_PATH+row[1]+cmd3
        cmd_volume = cmd1+str(row[0]) +cmd4+str(row[4]/100)+cmd5
        cmd_play = cmd1+str(row[0])+".play(-1)"
        cmd_stop = cmd1+str(row[0])+".stop()"
        #make list
        list_sound.append(cmd_sound)
        list_volume.append(cmd_volume)
        list_play.append(cmd_play)
        list_stop.append(cmd_stop)
    print(list_sound)
    # print(list_volume)
    # print(list_play)

def run():
    old_sound = []
    old_play = []
    while True:
        try:
            query()
            if list_sound: #don't start if no new data
                #LISTEN!: Load > play > volume
                for l_s in list_sound:
                    if l_s in old_sound:
                        print('same sound')
                    else:
                        print(l_s)
                        exec(l_s)
                for l_p in list_play:
                    if l_p in old_play:
                        print('sound already playing')
                    else:
                        print(l_p)
                        exec(l_p)
                if old_play:
                    for o_p in old_play:
                            if o_p in list_play:
                                print('tjs dans la zone')
                            else:
                                exec(o_p[:-9]+".stop()")
                                print('Sortie de zone', o_p[:-9])
                for l_v in list_volume:
                    print(l_v)
                    exec(l_v)
                    old_sound = list_sound
                    old_play = list_play
                # for l_s in list_stop:
                #     print(l_s)
                #     exec(l_s)
            else:
                print('no data')
        except Exception:
            continue

if __name__ == "__main__":
    run()
