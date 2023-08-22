# Insitorium
**Walk outside in a sound environment**

# Programme de Localisation Sonore avec Python
![photo_2022-08-26_19-35-18](https://user-images.githubusercontent.com/6421175/186960845-934650ba-a1f2-423f-b170-583672409168.jpg)

Ce programme utilise la localisation GPS pour jouer des sons en fonction de la proximité de l'utilisateur à des points spécifiques. Il a été pensé pour fonctionner en utilisant des données de localisation de haute précision à partir d'un réseau GNSS RTK (Real-Time Kinematic) tel que CentipedeRTK.

## Installation de Pydroid3 sur Android

1. Téléchargez et installez l'application Pydroid3 à partir du [Google Play Store](https://play.google.com/store/apps/details?id=ru.iiec.pydroid3).

2. Ouvrez l'application Pydroid3 et assurez-vous que votre environnement Python est configuré correctement.

3. Pour installer des bibliothèques supplémentaires, ouvrez le module PIP dans Pydroid3 et utilisez le gestionnaire INSTALL paquets pip. Installer les bibliothèques nécessaires : **geopy, pg8000, plyer**

## Utilisation des Imports en Python avec Pydroid3

Le code ci-dessous est conçu pour être exécuté dans l'environnement Pydroid3. Vous pouvez éditer et exécuter des scripts Python directement depuis l'application Pydroid3. Assurez-vous d'installer toutes les bibliothèques requises à l'aide du gestionnaire de paquets pip avant d'exécuter le script.
Fonctionnement avec CentipedeRTK et Récepteur GNSS RTK

Ce programme a été conçu pour fonctionner avec un réseau GNSS RTK tel que CentipedeRTK, qui fournit des données de localisation de haute précision en temps réel.
Pour utiliser ce programme de manière optimale:

1. Assurez-vous que vous avez un récepteur GNSS RTK compatible et d'un casque de bonne qualité. Les plans pour fabriquer un récepteur GNSS RTK compatible sont disponibles [ici](https://docs.centipede.fr/docs/make_rover/rover_v5_1).

![IMG_20220828_202032~2](https://user-images.githubusercontent.com/6421175/187089002-54ecafa0-9c47-4997-8a35-2a56b925c2ba.jpg)
    
2. Paramétrez l'application mobile NTRIP Client Lefebure avec CentipedeRTK pour obtenir des données de correction GNSS en temps réel.
    
3. Activez le paramétrage "Mock Location" (Localisation fictive) dans les options de développement d'Android. Cela permettra à votre application de simulation de localisation d'utiliser les données de localisation GNSS.
    
4. Exécutez le script dans l'environnement Pydroid3 avec toutes les bibliothèques requises installées.
    
5. Le programme jouera des sons en fonction de votre position par rapport aux points de la base de données.


    
