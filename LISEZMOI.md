# Site Villa La Vanille — mode d'emploi

## Le dossier
- `index.html` (français), `en/index.html`, `es/index.html`
- `style.css` : couleurs et polices (variables en haut du fichier)
- `script.js` : barre de navigation, carrousels (chambres, galerie) et plein écran
- `img/` : les photos
- `src/build.py` : tous les textes, coordonnées et infos pratiques, dans les 3 langues
- `sitemap.xml`, `robots.txt` : pour Google

## Modifier un texte, un tarif, une coordonnée
1. Ouvrez `src/build.py` et modifiez CONFIG, INFOS ou les textes.
2. Dans le dossier `src`, lancez : `python3 build.py`
Les trois pages sont régénérées. Une ligne d'infos pratiques à `None` est masquée.

## Changer une photo
Remplacez le fichier dans `img/` en gardant le même nom :
Les noms des photos et leur ordre dans la galerie sont dans `src/build.py` (listes GALLERY, CAPTIONS pour les légendes, et ROOMS, qui associe chaque chambre à ses photos).
Format conseillé : JPG, 2 400 px de large, moins de 500 Ko.

## À compléter avant la mise en ligne
1. Numéro d'enregistrement du meublé de tourisme
2. Le lien de réservation de la conciergerie se change dans CONFIG (`booking`)
3. Nom de domaine définitif
4. Tarifs basse et haute saison, dates, séjour minimum, caution, ménage, taxe de séjour (TARIFS et CONDITIONS dans build.py)
5. 2 ou 3 avis réels (liste QUOTES)
6. Mentions légales

## Mesure d'audience et réservations
- `consent.js` : bandeau cookies + balise Google G-8RVVVXJ4HN (Analytics et Google Ads), chargée seulement après « Accepter ».
- `reservation/` : page intermédiaire. Tous les boutons « Réserver » y mènent ; elle compte la visite (événement `clic_reservation`) puis redirige vers Octorate. Google Ads mesure les conversions sur l'adresse villalavanille.fr/reservation.
- Le lien de réservation Octorate se change dans CONFIG (`booking`), puis `python3 build.py`.

## Blog (« Le journal »)
- Chaque article est un fichier JSON dans `src/articles/` (texte en français, anglais et espagnol).
- `python3 build.py` (dans `src`) génère /blog/, /en/blog/, /es/blog/ et met à jour le sitemap.
