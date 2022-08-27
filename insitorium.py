
##------------------------------------------------------------------------------
##------------------------------------------------------------------------------
## Play Insitorium land sound on your smartphone with rtk location
##------------------------------------------------------------------------------
##------------------------------------------------------------------------------
## Use pydroid3 on your smartphone for runnig:
## * Pydroid 3 - IDE for Python 3:
##      https://play.google.com/store/apps/details?id=ru.iiec.pydroid3&hl=fr&gl=US
## * ACtivate location : Setting > system > additionnal permissions:
##      https://play.google.com/store/apps/details?id=ru.iiec.pydroidpermissionsplugin
## * Pydroid repository plugin:
##      https://play.google.com/store/apps/details?id=ru.iiec.pydroid3.quickinstallrepo
## * PIP INSTALL :
##      * pg8000
##      * plyer
## Use rtk connexion for location with Lefebure and CentipedeRTK:
##  * https://play.google.com/store/search?q=lefebure+ntrip&c=apps&hl=fr&gl=FR
##  * https://docs.centipede.fr/docs/Rover_rtklib_android/#application-lefebure-propri%C3%A9taire
##------------------------------------------------------------------------------

import pygame
import os
from pygame.locals import *
import pg8000.native
import time
from plyer import gps
from kivy.lang import Builder

## Where sounds ?
MUSIC_PATH = "./son/all/"

## Online Database connexion
HOST = "localhost"
PORT = 5432
USER = "geobeat"
PASSWORD = "password"
DATABASE = "insitorium"

## Blank variables
list_sound = []
list_volume =[]
list_play = []
list_stop = []
old_sound = []

## Get location
def gnss_llh(**kwargs):
    global lat
    global lon
    global elv
    global coor
    lat = 0.00
    lon = 0.00
    elv = 123
    coor = '0,0,0'

    lat = kwargs.get('lat')
    lon = kwargs.get('lon')
    elv = kwargs.get('altitude')
    coor = str(kwargs.get('lon'))+','+str(kwargs.get('lat'))+','+str(kwargs.get('altitude'))

    print(coor)

## Get nearest geolacated sounds from online database
def database():
    global res
    global res_pos
    print('Position',coor)
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
                        ST_MakePoint("""+coor+""")
    				, 4171)
    				,2154)
    	)::NUMERIC,2) as dist_m,
     	rayon
		FROM public.point p
		--(SELECT longi ,lati, height FROM public.user_position  ORDER BY id DESC LIMIT 1) pos
	) a
    WHERE a.dist_m < a.rayon
    ORDER BY prcent_vol DESC"""
    # print(QUERY)
    res =  conn.run(QUERY)
    print(res)
    conn.close()

## Transform database values to python pygame Sound command (load, play, volume, fadeout,...)
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

## Running insitorium
def run():
    old_sound = []
    old_play = []
    while True:
        try:
            ## Start GPS & get positions
            gps.configure(on_location=gnss_llh)
            gps.start()
            ## Get nerest sounds with
            query()
            if list_sound: ## don't start if no new data
                ## LISTEN!: Load > play > volume or fadeout sound
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
                                exec(o_p[:-9]+".fadeout(900)")
                                print('Sortie de zone', o_p[:-9])
                for l_v in list_volume:
                    print(l_v)
                    exec(l_v)
                    old_sound = list_sound
                    old_play = list_play
                    gps.stop()
            else:
                print('no data')
        except Exception:
            continue

if __name__ == "__main__":
    run()
