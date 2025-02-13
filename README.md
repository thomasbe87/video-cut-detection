## Description (FR)

Ce projet permet de détecter automatiquement les changements de scène ("cut") dans une vidéo en capturant l'écran en direct et en analysant les différences d'image, à base d'un histogramme.
D'autres scripts python existent, mais ne permettent pas la capture dun contenu en streaming à ma connaissance, d'où cette solution.

Ce projet a servi de base pour la rédaction d'un article sur le média belge Le Vif et d'un graphique comparatif entre 13 émissions pour enfants (https://www.levif.be/societe/famille/patpatrouille-gabby-ou-les-schtroumpfs-pourquoi-vous-devriez-surveiller-la-vitesse-des-dessins-animes-de-vos-enfants/)
La solution a de véritable limite pour capturer l'exactitude de la totalité des changements de plan, la sensibilité permettant de corriger certains "faux positifs", mais sans pouvoir garantir une détection parfaite.
Libre à vous d'améliorer cette base :)

## Fonctionnalités

- Détection automatique des cuts
- Export des résultats en CSV
- Paramètres configurables (seuil de détection, temps minimum entre cuts)

## Dépendances

- opencv-python
- numpy
- mss

pip install opencv-python numpy mss

## Utilisation
 
Placez la vidéo en plein écran sur le moniteur principal et déclenchez le script python (cut.py) dans le terminal. Vous verrez apparaître en temps réel dans le terminal les différents cuts détectés. Ajustez éventuellement le seuil de détection après quelques secondes si les détections semblent trop nombreuses ou trop peu nombreuses.


-----

## Description (EN)

This project allows for the automatic detection of scene changes ("cuts") in a video by capturing the screen live and analyzing image differences using a histogram-based approach.
While other Python scripts exist for this purpose, they do not, to my knowledge, support capturing streaming content directly from the screen, which makes this solution useful.

This project was used as the foundation for an article published in the Belgian media outlet Le Vif and for a comparative analysis graphic between 13 children's TV shows (https://www.levif.be/societe/famille/patpatrouille-gabby-ou-les-schtroumpfs-pourquoi-vous-devriez-surveiller-la-vitesse-des-dessins-animes-de-vos-enfants/).
The solution has inherent limitations in capturing all scene changes with perfect accuracy. Sensitivity settings can help reduce some false positives, but perfect detection cannot be guaranteed.
Feel free to improve this base project! :)

## Features

- Automatic cut detection
- Export results to CSV
- Configurable parameters (detection threshold, minimum time between cuts)

## Dependencies

- opencv-python
- numpy
- mss

pip install opencv-python numpy mss

## Usage

Place the video in full screen on the primary monitor and run the Python script (cut.py) in the terminal. You will see detected cuts appear in real-time in the terminal.
If the detections seem too frequent or too sparse, adjust the detection threshold after observing the results for a few seconds.
