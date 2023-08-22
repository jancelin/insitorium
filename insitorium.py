import pygame
import threading
import time
from geopy.distance import geodesic
import pg8000
from plyer import gps

# Connexion à la base de données PostgreSQL, modifier avec votre paramétrage
conn = pg8000.connect(
    user='user',
    password='hackme',
    host='IP_postgres_database',
    port=5432,
    database='insitorium'
)

# Initialisation de pygame
pygame.mixer.pre_init(44100, -16, 6, 1024*4)
pygame.mixer.init()
pygame.init()

# Rayon de 100 mètres
radius = 100

# Coordonnées cibles (initialisées avec des valeurs par défaut)
target_coor = (0, 0)  # Les coordonnées cibles seront mises à jour par le GPS

# Fonction pour jouer le son "bug.wav"
def play_waiting_sound():
    waiting_sound = pygame.mixer.Sound("./son/wait.wav")
    waiting_sound.set_volume(0.1)  # Volume à 60%
    waiting_sound.play(-1)  # Joue en boucle en continu
    return waiting_sound

# Jouer le son d'attente
waiting_sound = play_waiting_sound()

# Callback pour mettre à jour les coordonnées cibles
def on_location(**kwargs):
    global target_coor
    target_coor = (kwargs['lon'], kwargs['lat'])
    #print("Received GPS Data:", target_coor)

    # Arrêter le son d'attente une fois la position GPS reçue
    if waiting_sound:
        waiting_sound.stop()

# Configuration et initialisation de Plyer GPS
gps.configure(on_location=on_location)
gps.start(minTime=50, minDistance=0.01)

# Attendre la réception d'une position GPS de bonne qualité avant de continuer
while target_coor == (0, 0):
    print("Waiting for GPS Data...")
    time.sleep(0.5)

# Requête SQL pour récupérer les données avec les coordonnées en (longitude,latitude)
query = f"""
    SELECT p.id, p.texte, ST_Y(p.geom) as lat, ST_X(p.geom) as lon, p.rayon
    FROM public.point2 p
    WHERE ST_DWithin(ST_SetSRID(ST_MakePoint({target_coor[0]}, {target_coor[1]}), 4171)::geography, p.geom::geography, {radius});
"""

# Exécution de la requête et stockage dans une liste
cursor = conn.cursor()
cursor.execute(query)
data = cursor.fetchall()
cursor.close()

# Création d'une liste de dictionnaires pour stocker les données
local_data = [{'id': row[0], 'texte': row[1], 'geom': (row[3], row[2]), 'rayon': float(row[4]), 'playing': False} for row in data]

print("Local Data:", local_data)  # Affichage en mode débogage

def play_sound(file_path, volume):
    sound = pygame.mixer.Sound(file_path)
    sound.set_volume(volume)
    sound.play(-1)  # Joue en boucle
    return sound

def update_distances_and_volumes():
    point_sounds = {}

    while True:
        # Récupération des coordonnées du GPS
        gps_coordinates = target_coor

        # Calcul de la distance pour chaque point
        for point in local_data:
            point_coords = point['geom']
            point_distance = geodesic(gps_coordinates, point_coords).meters
            point['distance'] = point_distance

            # Calcul du volume sonore
            point['prcent_vol'] = 100 - ((point_distance * 100) / point['rayon'])

            if point['id'] in point_sounds:
                if point['prcent_vol'] <= 0:
                    point_sounds[point['id']].fadeout(800)
                    #point_sounds[point['id']].stop()
                    del point_sounds[point['id']]
                else:
                    point_sounds[point['id']].set_volume(point['prcent_vol'] / 100)
            else:
                if point['prcent_vol'] > 0:
                    point_sound = play_sound(f"./son/{point['texte']}.wav", point['prcent_vol'] / 100)
                    point_sounds[point['id']] = point_sound

        # Pause très courte pour la mise à jour
        time.sleep(0.05)  # Vous pouvez ajuster cette valeur en fonction de vos besoins

# Démarrage du thread de mise à jour
update_thread = threading.Thread(target=update_distances_and_volumes)
update_thread.start()
