# -*- coding: utf-8 -*-
"""
Générateur du site Villa La Vanille.
1. Modifiez CONFIG, TARIFS, CONDITIONS et les textes ci-dessous.
2. Lancez :  python3 build.py   (depuis le dossier src)
3. Les pages sont régénérées dans le dossier parent.
"""
import json, os, shutil, html
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, ".."))

# ------------------------------------------------------------------
# CONFIG — à compléter avant la mise en ligne
# ------------------------------------------------------------------
CONFIG = {
    "domain": "https://www.villalavanille.fr",
    "registration": "À COMPLÉTER",       # n° d'enregistrement meublé de tourisme (obligatoire)
    "instagram": "",
    "airbnb": "https://www.airbnb.fr/rooms/41926993",
    "phone": "+590 690 547 547",
    "email": "info@kazamariegalante.com",
    # Calendrier et réservation de la conciergerie (tous les boutons « Réserver » y mènent)
    # Carte du pied de page : adresse ou coordonnées « latitude,longitude » de la villa
    "map_q": "Villa La Vanille, Section Lalane, 97112 Grand-Bourg, Marie-Galante, Guadeloupe",
    "map_zoom": 15,
    "google_tag": "G-8RVVVXJ4HN",
    "booking": "https://book.octorate.com/octobook/site/ota/result.xhtml?id=357&property=768373&room=226938",
}

# ------------------------------------------------------------------
# TARIFS — selon le nombre de chambres : (chambres, prix par nuit, prix par semaine)
# ------------------------------------------------------------------
TARIFS = [(1, 250, 1750), (2, 300, 2100), (3, 350, 2450), (4, 400, 2800), (5, 475, 3325)]

# Conditions affichées sous les tarifs. None = ligne masquée.
# Arrivée, départ et annulation : repris du site de réservation de la conciergerie.
CONDITIONS = {
    "fr": [("Séjour minimum", "3 nuits"), ("Arrivée", "À partir de 18 h"), ("Départ", "Avant 10 h"),
           ("Frais de service", "290 €"),
           ("Taxe de séjour", "2 € par personne et par nuit<small>Le montant de la taxe de séjour est calculé selon les modalités fournies par les autorités locales. Cette somme est une taxe, elle est donc identique quelle que soit la provenance de la réservation.</small>"),
           ("Règlement", "Par carte bancaire : 50 % à la réservation, le solde 30 jours avant l'arrivée"),
           ("Caution", "1 500 €"), ("Assurance annulation", "À partir de 3 %")],
    "en": [("Minimum stay", "3 nights"), ("Check-in", "From 6 pm"), ("Check-out", "Before 10 am"),
           ("Service fee", "€290"),
           ("Tourist tax", "€2 per person per night<small>The tourist tax is calculated according to the rules set by the local authorities. As it is a tax, the amount is the same wherever the booking is made.</small>"),
           ("Payment", "By card: 50% at booking, the balance 30 days before arrival"),
           ("Security deposit", "€1,500"), ("Cancellation insurance", "From 3%")],
    "es": [("Estancia mínima", "3 noches"), ("Llegada", "A partir de las 18 h"), ("Salida", "Antes de las 10 h"),
           ("Gastos de servicio", "290 €"),
           ("Tasa turística", "2 € por persona y noche<small>El importe de la tasa turística se calcula según las modalidades establecidas por las autoridades locales. Al tratarse de un impuesto, es idéntico sea cual sea el origen de la reserva.</small>"),
           ("Pago", "Con tarjeta: 50 % al reservar y el resto 30 días antes de la llegada"),
           ("Fianza", "1.500 €"), ("Seguro de cancelación", "Desde el 3 %")],
}

# Avis réels (copiez 2 ou 3 commentaires Airbnb). Ex. {"text": "…", "who": "Marie, juillet 2026"}
QUOTES = []

LANGS = ["fr", "en", "es"]
PATHS = {"fr": "", "en": "en/", "es": "es/"}

T = {
"fr": dict(
    title="Villa La Vanille | Villa de luxe avec piscine et vue mer à Marie-Galante",
    desc="Villa créole de 5 chambres pour 12 personnes à Grand-Bourg, Marie-Galante : piscine d'eau salée chauffée, vue sur le canal de la Dominique, jardin tropical. Réservation en direct.",
    m_villa="La villa", m_rooms="Les chambres", m_tarifs="Tarifs", book="Réserver", t_h="Modalités et tarifs", t_p="Le prix dépend du nombre de chambres ouvertes. Tarifs hors périodes de fêtes et Terre de Blues.", col_opt="Option", col_n="Prix / nuit", col_w="Prix / semaine", ch1="chambre", chn="chambres", cond_h="Conditions",
    place="Grand-Bourg, Marie-Galante",
    tag="Villa créole   Marie-Galante   Guadeloupe", cue="Défilez", cap1="La grande table", cap2="Les chambres", cap4="La galerie", cap5="La cuisine d'été", coin_d1="5 chambres, 12 personnes", coin_d2="Piscine d'eau salée",
    hero_p="Villa créole, piscine et vue sur le canal de la Dominique.",
    dispo="Voir les disponibilités",
    intro_k="Bienvenue",
    lede="Deux maisons créoles, un jardin tropical et la mer pour seul horizon. Ici, les journées se comptent en baignades et en couchers de soleil.",
    c1="voyageurs", c2="chambres", c3="salles de bain", c4="m² de jardin",
    v_h="La villa",
    v1h="La galerie", v1="Plus de 80 m² de terrasse en bois, ouverts sur le jardin et la mer. On y prend le petit-déjeuner, on y lit à l'ombre, on y fait la sieste.",
    v2h="Le salon", v2="Bois blanc, hauts plafonds et fibres naturelles. Un intérieur lumineux, frais et sans artifice, qui s'ouvre largement sur la galerie.",
    v3h="La grande table", v3="Douze couverts sous la galerie, face au jardin. La cuisine d'été, avec barbecue au gaz et plancha, est juste à côté.",
    r_h="Les chambres", r_p="Cinq chambres climatisées, réparties entre deux maisons. Chacun trouve son espace et son calme.",
    house1="La maison principale", house2="La maison de la piscine",
    r1="Chambre 1", r2="Chambre 2", r3="Chambre 3", r4="Chambre 4", r5="Chambre 5",
    king="Lit king size, moustiquaire, vue mer", bunks="Deux lits superposés, pour quatre enfants ou adolescents",
    king_bath="Lit king size, salle de bain privative",
    r_note="Une chambre de quatre lits pour enfants est disponible sur demande, avec supplément.",
    p_h="Prestations", cz_h="Une conciergerie à votre service", cz_1="Que vous souhaitiez réserver vos <strong>billets de bateau, une voiture de location, un taxi, un chef à domicile, des activités, un massage, une sortie en mer ou simplement être conseillé</strong> pour organiser votre séjour, Fabie est là pour vous accompagner.", cz_2="En plus de ses précieux conseils, elle vous fera bénéficier de <strong>tarifs préférentiels et de codes promo exclusifs MGVIP</strong> auprès de nombreux partenaires locaux.",
    p_p="La piscine d'eau salée est chauffée et regarde la mer. Le reste a été pensé pour que vous n'ayez à vous occuper de rien.",
    pr=["Piscine d'eau salée chauffée, vue mer", "Cuisine intérieure équipée et cuisine d'été",
        "Barbecue au gaz et plancha", "Climatisation dans toutes les chambres",
        "Wi-Fi et espace de travail", "Jardinier et pisciniste chaque semaine"],
    g_h="Galerie",
    alt_piscine="La piscine et le jardin", alt_patio="La galerie ouverte sur la mer", alt_salon="Le salon",
    alt_cuisine="La cuisine", alt_sam="La grande table sous la galerie",
    close="Fermer", prev="Précédente", next="Suivante",
    i_h="Marie-Galante",
    i_p="Une île ronde et paisible, à une heure de bateau de la Guadeloupe. On y circule entre champs de canne, plages désertes et anciens moulins.",
    l1h="Les plages", l1="Petite-Anse, la Feuillère, Anse Canot. Sable blanc et eau calme.",
    l2h="Les distilleries", l2="Bielle, Bellevue et Père Labat. Le rhum de l'île est réputé dans toute la Caraïbe.",
    l3h="Habitation Murat", l3="Ancienne sucrerie devenue écomusée, tout près de Grand-Bourg.",
    l4h="Gueule Grand Gouffre", l4="Une falaise spectaculaire au nord, où l'Atlantique passe sous une arche.",
    l5h="Moulin de Bézard", l5="Le seul moulin à vent restauré de l'île.",
    l6h="La mer", l6="Plongée, sorties en bateau et pêche autour de l'île.",
    a_h="Venir à la villa",
    a_p="Bateau depuis Pointe-à-Pitre jusqu'au port de Grand-Bourg, en une heure environ, ou petit avion jusqu'à l'aérodrome de l'île. La villa est à 3 km du bourg et du port, dans un quartier calme. Une voiture est conseillée.",
    av_h="Ils ont séjourné ici", av_s="sur 5, d'après 17 avis Airbnb. Coup de cœur voyageurs.",
    s=["Propreté", "Précision", "Arrivée", "Communication", "Emplacement", "Qualité-prix"],
    inf_h="Infos pratiques", rules_h="Bon à savoir",
    rules=["Les animaux ne sont pas admis.", "Pas de fêtes. Les dîners entre amis sont les bienvenus.",
           "La piscine n'est pas surveillée.", "La villa n'est pas adaptée aux tout-petits."],
    b_h="Réserver", b_p="Les réservations sont gérées par notre conciergerie. Consultez les disponibilités et réservez votre séjour en ligne.",
    b_cal="Voir le calendrier et réserver",
    l_arrive="Arrivée", l_depart="Départ", l_guests="Voyageurs", l_name="Nom", l_email="E-mail", l_msg="Message",
    send="Envoyer ma demande", ready="Votre demande est prête. Choisissez comment l'envoyer :",
    via_wa="WhatsApp", via_mail="E-mail",
    js_hello="Bonjour, je souhaite réserver la Villa La Vanille.", js_subject="Demande de réservation — Villa La Vanille",
    f_contact="Nous contacter", ck_t="Nous utilisons des cookies de mesure d'audience (Google Analytics) pour comprendre comment le site est utilisé et l'améliorer. Vous pouvez les accepter ou les refuser.", ck_ok="Accepter", ck_non="Refuser", ck_g="Gérer les cookies", map_btn="Afficher la carte", map_note="Google Maps dépose des cookies.", map_open="Ouvrir dans Google Maps", f_follow="Suivre", reg="N° d'enregistrement", legal="Mentions légales", lg2="Politique de confidentialité", lg3="Conditions générales de vente", lg4="Conditions d'utilisation", blog="Le journal", blog_t="Idées et conseils pour votre séjour",
),
"en": dict(
    title="Villa La Vanille | Luxury villa with pool and sea view in Marie-Galante",
    desc="Five-bedroom Creole villa sleeping 12 in Grand-Bourg, Marie-Galante, Guadeloupe: heated saltwater pool, view over the Dominica channel, tropical garden. Book direct.",
    m_villa="The villa", m_rooms="Bedrooms", m_tarifs="Rates", book="Book", t_h="Terms and rates", t_p="The price depends on the number of bedrooms opened. Rates exclude holiday periods and the Terre de Blues festival.", col_opt="Option", col_n="Price / night", col_w="Price / week", ch1="bedroom", chn="bedrooms", cond_h="Conditions",
    place="Grand-Bourg, Marie-Galante",
    tag="Creole villa   Marie-Galante   Guadeloupe", cue="Scroll", cap1="The long table", cap2="The bedrooms", cap4="The gallery", cap5="The summer kitchen", coin_d1="5 bedrooms, 12 guests", coin_d2="Saltwater pool",
    hero_p="A Creole villa, a pool and a view over the Dominica channel.",
    dispo="Check availability",
    intro_k="Welcome",
    lede="Two Creole houses, a tropical garden and nothing but the sea on the horizon. Here, days are counted in swims and sunsets.",
    c1="guests", c2="bedrooms", c3="bathrooms", c4="m² of garden",
    v_h="The villa",
    v1h="The gallery", v1="Over 80 m² of wooden veranda, open to the garden and the sea. Breakfast, reading in the shade, an afternoon nap.",
    v2h="The living room", v2="White wood, high ceilings and natural fibres. A bright, cool interior that opens wide onto the gallery.",
    v3h="The long table", v3="Seats twelve under the gallery, facing the garden. The summer kitchen, with gas barbecue and plancha, is right next to it.",
    r_h="The bedrooms", r_p="Five air-conditioned bedrooms across two houses. Everyone finds their own space and quiet.",
    house1="The main house", house2="The pool house",
    r1="Bedroom 1", r2="Bedroom 2", r3="Bedroom 3", r4="Bedroom 4", r5="Bedroom 5",
    king="King bed, mosquito net, sea view", bunks="Two bunk beds, for four children or teens",
    king_bath="King bed, private bathroom",
    r_note="A four-bed children's room is available on request, for an extra fee.",
    p_h="Amenities", cz_h="A concierge at your service", cz_1="Whether you want to book <strong>ferry tickets, a rental car, a taxi, a private chef, activities, a massage, a boat trip, or simply get advice</strong> to plan your stay, Fabie is there to help.", cz_2="On top of her valuable advice, she will give you <strong>preferential rates and exclusive MGVIP promo codes</strong> with many local partners.",
    p_p="The saltwater pool is heated and faces the sea. Everything else is designed so you have nothing to worry about.",
    pr=["Heated saltwater pool with sea view", "Equipped indoor kitchen and summer kitchen",
        "Gas barbecue and plancha", "Air conditioning in every bedroom",
        "Wi-Fi and workspace", "Gardener and pool technician every week"],
    g_h="Gallery",
    alt_piscine="The pool and garden", alt_patio="The gallery opening onto the sea", alt_salon="The living room",
    alt_cuisine="The kitchen", alt_sam="The long table under the gallery",
    close="Close", prev="Previous", next="Next",
    i_h="Marie-Galante",
    i_p="A round, peaceful island one hour by boat from Guadeloupe. Life moves between sugar cane fields, empty beaches and old windmills.",
    l1h="Beaches", l1="Petite-Anse, La Feuillère, Anse Canot. White sand and calm water.",
    l2h="Rum distilleries", l2="Bielle, Bellevue and Père Labat. The island's rum is famous across the Caribbean.",
    l3h="Habitation Murat", l3="A former sugar estate turned eco-museum, close to Grand-Bourg.",
    l4h="Gueule Grand Gouffre", l4="A dramatic northern cliff where the Atlantic rushes under a rock arch.",
    l5h="Bézard windmill", l5="The island's only restored windmill.",
    l6h="The sea", l6="Diving, boat trips and fishing around the island.",
    a_h="Getting here",
    a_p="Ferry from Pointe-à-Pitre to Grand-Bourg harbour in about one hour, or a short flight to the island's airfield. The villa is 3 km from town and the harbour, in a quiet area. A car is recommended.",
    av_h="Our guests", av_s="out of 5, from 17 Airbnb reviews. Guest favorite.",
    s=["Cleanliness", "Accuracy", "Check-in", "Communication", "Location", "Value"],
    inf_h="Practical information", rules_h="Good to know",
    rules=["No pets.", "No parties. Dinners with friends are welcome.",
           "The pool is not supervised.", "The villa is not suited to toddlers."],
    b_h="Book", b_p="Bookings are handled by our concierge service. Check availability and book your stay online.",
    b_cal="See the calendar and book",
    l_arrive="Arrival", l_depart="Departure", l_guests="Guests", l_name="Name", l_email="Email", l_msg="Message",
    send="Send my request", ready="Your request is ready. Choose how to send it:",
    via_wa="WhatsApp", via_mail="Email",
    js_hello="Hello, I would like to book Villa La Vanille.", js_subject="Booking request — Villa La Vanille",
    f_contact="Contact us", ck_t="We use audience measurement cookies (Google Analytics) to understand how the site is used and improve it. You can accept or decline them.", ck_ok="Accept", ck_non="Decline", ck_g="Manage cookies", map_btn="Show the map", map_note="Google Maps sets cookies.", map_open="Open in Google Maps", f_follow="Follow", reg="Registration no.", legal="Legal notice", lg2="Privacy policy", lg3="Terms of sale", lg4="Terms of use", blog="The journal", blog_t="Ideas and tips for your stay",
),
"es": dict(
    title="Villa La Vanille | Villa de lujo con piscina y vista al mar en Marie-Galante",
    desc="Villa criolla de 5 habitaciones para 12 personas en Grand-Bourg, Marie-Galante, Guadalupe: piscina de agua salada climatizada, vista al canal de Dominica, jardín tropical. Reserva directa.",
    m_villa="La villa", m_rooms="Habitaciones", m_tarifs="Tarifas", book="Reservar", t_h="Condiciones y tarifas", t_p="El precio depende del número de habitaciones abiertas. Tarifas fuera de los periodos festivos y del festival Terre de Blues.", col_opt="Opción", col_n="Precio / noche", col_w="Precio / semana", ch1="habitación", chn="habitaciones", cond_h="Condiciones",
    place="Grand-Bourg, Marie-Galante",
    tag="Villa criolla   Marie-Galante   Guadalupe", cue="Deslice", cap1="La gran mesa", cap2="Las habitaciones", cap4="La galería", cap5="La cocina de verano", coin_d1="5 habitaciones, 12 personas", coin_d2="Piscina de agua salada",
    hero_p="Villa criolla, piscina y vista al canal de Dominica.",
    dispo="Ver disponibilidad",
    intro_k="Bienvenidos",
    lede="Dos casas criollas, un jardín tropical y el mar como único horizonte. Aquí los días se cuentan en baños y atardeceres.",
    c1="huéspedes", c2="habitaciones", c3="baños", c4="m² de jardín",
    v_h="La villa",
    v1h="La galería", v1="Más de 80 m² de terraza de madera, abiertos al jardín y al mar. Desayuno, lectura a la sombra y siesta.",
    v2h="El salón", v2="Madera blanca, techos altos y fibras naturales. Un interior luminoso y fresco que se abre a la galería.",
    v3h="La gran mesa", v3="Doce comensales bajo la galería, frente al jardín. La cocina de verano, con barbacoa de gas y plancha, está al lado.",
    r_h="Las habitaciones", r_p="Cinco habitaciones con aire acondicionado, repartidas en dos casas. Cada uno encuentra su espacio y su calma.",
    house1="La casa principal", house2="La casa de la piscina",
    r1="Habitación 1", r2="Habitación 2", r3="Habitación 3", r4="Habitación 4", r5="Habitación 5",
    king="Cama king, mosquitera, vista al mar", bunks="Dos literas, para cuatro niños o adolescentes",
    king_bath="Cama king, baño privado",
    r_note="Bajo petición, hay una habitación infantil de cuatro camas, con suplemento.",
    p_h="Servicios", cz_h="Una conserjería a su servicio", cz_1="Tanto si desea reservar <strong>billetes de barco, un coche de alquiler, un taxi, un chef a domicilio, actividades, un masaje, una salida en barco o simplemente recibir consejos</strong> para organizar su estancia, Fabie está ahí para acompañarle.", cz_2="Además de sus valiosos consejos, le ofrecerá <strong>tarifas preferentes y códigos promocionales exclusivos MGVIP</strong> con numerosos socios locales.",
    p_p="La piscina de agua salada está climatizada y mira al mar. Todo lo demás está pensado para que no tenga que ocuparse de nada.",
    pr=["Piscina de agua salada climatizada con vista al mar", "Cocina interior equipada y cocina de verano",
        "Barbacoa de gas y plancha", "Aire acondicionado en todas las habitaciones",
        "Wi-Fi y espacio de trabajo", "Jardinero y técnico de piscina cada semana"],
    g_h="Galería",
    alt_piscine="La piscina y el jardín", alt_patio="La galería abierta al mar", alt_salon="El salón",
    alt_cuisine="La cocina", alt_sam="La gran mesa bajo la galería",
    close="Cerrar", prev="Anterior", next="Siguiente",
    i_h="Marie-Galante",
    i_p="Una isla redonda y tranquila, a una hora en barco de Guadalupe. La vida pasa entre campos de caña, playas desiertas y antiguos molinos.",
    l1h="Las playas", l1="Petite-Anse, La Feuillère, Anse Canot. Arena blanca y agua tranquila.",
    l2h="Las destilerías", l2="Bielle, Bellevue y Père Labat. El ron de la isla es famoso en todo el Caribe.",
    l3h="Habitation Murat", l3="Antigua hacienda azucarera convertida en ecomuseo, cerca de Grand-Bourg.",
    l4h="Gueule Grand Gouffre", l4="Un acantilado espectacular al norte, donde el Atlántico pasa bajo un arco.",
    l5h="Molino de Bézard", l5="El único molino de viento restaurado de la isla.",
    l6h="El mar", l6="Buceo, paseos en barco y pesca alrededor de la isla.",
    a_h="Cómo llegar",
    a_p="Barco desde Pointe-à-Pitre hasta el puerto de Grand-Bourg en una hora aproximadamente, o avioneta hasta el aeródromo de la isla. La villa está a 3 km del pueblo y del puerto, en una zona tranquila. Se recomienda coche.",
    av_h="Nuestros huéspedes", av_s="sobre 5, según 17 opiniones en Airbnb. Favorito entre huéspedes.",
    s=["Limpieza", "Veracidad", "Llegada", "Comunicación", "Ubicación", "Calidad-precio"],
    inf_h="Información práctica", rules_h="Bueno saber",
    rules=["No se admiten mascotas.", "No se permiten fiestas. Las cenas con amigos son bienvenidas.",
           "La piscina no está vigilada.", "La villa no está adaptada a niños muy pequeños."],
    b_h="Reservar", b_p="Las reservas las gestiona nuestro servicio de conserjería. Consulte la disponibilidad y reserve su estancia en línea.",
    b_cal="Ver el calendario y reservar",
    l_arrive="Llegada", l_depart="Salida", l_guests="Huéspedes", l_name="Nombre", l_email="Correo", l_msg="Mensaje",
    send="Enviar mi solicitud", ready="Su solicitud está lista. Elija cómo enviarla:",
    via_wa="WhatsApp", via_mail="Correo",
    js_hello="Hola, me gustaría reservar Villa La Vanille.", js_subject="Solicitud de reserva — Villa La Vanille",
    f_contact="Contáctenos", ck_t="Utilizamos cookies de medición de audiencia (Google Analytics) para entender cómo se usa el sitio y mejorarlo. Puede aceptarlas o rechazarlas.", ck_ok="Aceptar", ck_non="Rechazar", ck_g="Gestionar cookies", map_btn="Mostrar el mapa", map_note="Google Maps instala cookies.", map_open="Abrir en Google Maps", f_follow="Seguir", reg="N.º de registro", legal="Aviso legal", lg2="Política de privacidad", lg3="Condiciones de venta", lg4="Condiciones de uso", blog="El diario", blog_t="Ideas y consejos para su estancia",
),
}


# ---- Textes ajoutés : rangées « La villa » et légendes des photos ----
EXTRA = {
"fr": dict(
    v0h="La piscine", v0="Une piscine d'eau salée chauffée, face à la mer. Son solarium en bois, ses bains de soleil et le jardin tropical tout autour en font le cœur de la villa, du matin jusqu'au coucher du soleil.",
    v1h="La galerie", v1="Une galerie de plus de 80 m² ouverte sur le jardin tropical, avec vue sur l'océan et l'île de la Dominique. On y prend le petit-déjeuner, on y lit à l'ombre, on y fait la sieste dans le hamac.",
    vsh="Le salon cathédrale", vs="Sous une haute charpente en bois blanc, le salon s'ouvre par de grandes portes à persiennes sur la galerie et la mer. Canapé en lin, suspensions en rotin, tomettes et objets chinés : un intérieur créole lumineux, frais et apaisant.",
    v2h="La grande table", v2="Sous la galerie, une salle à manger pour douze personnes. Le soir, les suspensions en rotin et les photophores s'allument pour de longs dîners face au jardin.",
    v3h="Les cuisines", v3="Une cuisine intérieure équipée, ouverte sur la galerie, et une cuisine extérieure avec barbecue au gaz et plancha.",
    rooms_gal="Les chambres en images",
    alt={"piscine-maison":"La piscine devant la maison de la piscine","galerie":"La galerie ouverte sur la mer",
         "cuisine":"La cuisine intérieure","vue-mer":"La vue sur la mer depuis le jardin","maison-principale":"La maison principale et sa galerie","salon-vue-mer":"Le salon cathédrale ouvert sur la mer","salon":"Le salon cathédrale le soir","cuisine-ete":"La cuisine d'été, barbecue et plancha","cuisine-ete-2":"La cuisine d'été le long de la maison",
         "grande-table":"La grande table sous la galerie, le soir","table-dressee":"La table dressée face à la mer",
         "chambre-baldaquin":"Chambre avec lit à baldaquin","chambre-soir":"Chambre le soir, ouverte sur la terrasse",
         "chambre-enfants":"La chambre des enfants et ses lits superposés","chambre-enfants-2":"La chambre des enfants et sa douche",
         "chambre-blanche":"Chambre aux volets blancs","chambre-cartes":"Chambre aux cartes anciennes",
         "chambre-vue-piscine":"Vue sur la piscine depuis le lit","chambre5":"Chambre 5, lit king size","chambre5-sdb":"La salle de bain de la chambre 5","piscine":"La piscine d'eau salée chauffée"},
),
"en": dict(
    v0h="The pool", v0="A heated saltwater pool facing the sea. With its wooden sun deck, loungers and the tropical garden all around, it is the heart of the villa, from morning to sunset.",
    v1h="The gallery", v1="A gallery of over 80 m² open to the tropical garden, with views of the ocean and the island of Dominica. Breakfast, reading in the shade, a nap in the hammock.",
    vsh="The cathedral living room", vs="Beneath a soaring white wooden roof, the living room opens through tall louvred doors onto the gallery and the sea. Linen sofa, rattan pendants, terracotta tiles and found objects: a bright, cool and calming Creole interior.",
    v2h="The long table", v2="Under the gallery, a dining area for twelve. In the evening, the rattan lamps and candles light up long dinners facing the garden.",
    v3h="The kitchens", v3="An equipped indoor kitchen opening onto the gallery, and an outdoor kitchen with gas barbecue and plancha.",
    rooms_gal="The bedrooms in pictures",
    alt={"piscine-maison":"The pool in front of the pool house","galerie":"The gallery opening onto the sea",
         "cuisine":"The indoor kitchen","vue-mer":"The sea view from the garden","maison-principale":"The main house and its gallery","salon-vue-mer":"The cathedral living room opening onto the sea","salon":"The cathedral living room at night","cuisine-ete":"The summer kitchen, barbecue and plancha","cuisine-ete-2":"The summer kitchen along the house",
         "grande-table":"The long table under the gallery at night","table-dressee":"The table set facing the sea",
         "chambre-baldaquin":"Bedroom with canopy bed","chambre-soir":"Bedroom at night, opening onto the terrace",
         "chambre-enfants":"The children's room with bunk beds","chambre-enfants-2":"The children's room and its shower",
         "chambre-blanche":"Bedroom with white shutters","chambre-cartes":"Bedroom with antique maps",
         "chambre-vue-piscine":"View of the pool from the bed","chambre5":"Bedroom 5, king bed","chambre5-sdb":"Bedroom 5 bathroom","piscine":"The heated saltwater pool"},
),
"es": dict(
    v0h="La piscina", v0="Una piscina de agua salada climatizada frente al mar. Con su solárium de madera, sus tumbonas y el jardín tropical alrededor, es el corazón de la villa, de la mañana al atardecer.",
    v1h="La galería", v1="Una galería de más de 80 m² abierta al jardín tropical, con vista al océano y a la isla de Dominica. Desayuno, lectura a la sombra y siesta en la hamaca.",
    vsh="El salón catedral", vs="Bajo una alta estructura de madera blanca, el salón se abre con grandes puertas de persianas a la galería y al mar. Sofá de lino, lámparas de ratán, baldosas de barro y objetos antiguos: un interior criollo luminoso, fresco y sereno.",
    v2h="La gran mesa", v2="Bajo la galería, un comedor para doce personas. Por la noche, las lámparas de ratán y las velas acompañan largas cenas frente al jardín.",
    v3h="Las cocinas", v3="Una cocina interior equipada, abierta a la galería, y una cocina exterior con barbacoa de gas y plancha.",
    rooms_gal="Las habitaciones en imágenes",
    alt={"piscine-maison":"La piscina frente a la casa de la piscina","galerie":"La galería abierta al mar",
         "cuisine":"La cocina interior","vue-mer":"La vista al mar desde el jardín","maison-principale":"La casa principal y su galería","salon-vue-mer":"El salón catedral abierto al mar","salon":"El salón catedral de noche","cuisine-ete":"La cocina de verano, barbacoa y plancha","cuisine-ete-2":"La cocina de verano junto a la casa",
         "grande-table":"La gran mesa bajo la galería, de noche","table-dressee":"La mesa puesta frente al mar",
         "chambre-baldaquin":"Habitación con cama con dosel","chambre-soir":"Habitación de noche, abierta a la terraza",
         "chambre-enfants":"La habitación infantil con literas","chambre-enfants-2":"La habitación infantil y su ducha",
         "chambre-blanche":"Habitación de contraventanas blancas","chambre-cartes":"Habitación con mapas antiguos",
         "chambre-vue-piscine":"Vista de la piscina desde la cama","chambre5":"Habitación 5, cama king","chambre5-sdb":"El baño de la habitación 5","piscine":"La piscina de agua salada climatizada"},
),
}
for _l in EXTRA:
    T[_l].update(EXTRA[_l])

# Ordre de la galerie et légendes : (photo, titre, sous-titre) dans chaque langue
GALLERY = ["vue-mer", "piscine-maison", "piscine", "galerie", "salon-vue-mer", "salon", "grande-table", "table-dressee", "cuisine", "cuisine-ete",
           "cuisine-ete-2", "chambre-baldaquin", "chambre-soir", "chambre-enfants", "chambre-enfants-2",
           "chambre-vue-piscine", "chambre-cartes", "chambre-blanche", "chambre5", "chambre5-sdb"]
CAPTIONS = {
"fr": {"vue-mer": ("La vue", "L'océan et la Dominique depuis le jardin"),
       "maison-principale": ("La maison principale", "Galerie et jardin tropical"),
       "piscine-maison": ("La maison de la piscine", "Trois chambres avec salle de bain, face au bassin"),
       "piscine": ("La piscine", "Eau salée chauffée et terrasse en bois"),
       "galerie": ("La galerie", "Plus de 80 m² ouverts sur le jardin et la mer"),
       "salon-vue-mer": ("Le salon cathédrale", "Grandes portes ouvertes sur la mer"),
       "salon": ("Le salon cathédrale", "Lin, rotin et bois blanc, le soir"),
       "grande-table": ("La grande table", "Douze couverts sous la galerie, le soir"),
       "table-dressee": ("Le dîner", "La table dressée face au jardin"),
       "cuisine": ("La cuisine", "Équipée et ouverte sur la galerie"),
       "cuisine-ete": ("La cuisine d'été", "Barbecue au gaz et plancha"),
       "cuisine-ete-2": ("La cuisine d'été", "Le long de la maison, à l'ombre"),
       "chambre-baldaquin": ("Chambre 1", "Lit king size et moustiquaire"),
       "chambre-soir": ("Chambre 1", "La même chambre, le soir"),
       "chambre-enfants": ("Chambre 2", "Lits superposés pour quatre enfants"),
       "chambre-enfants-2": ("Chambre 2", "Avec sa douche"),
       "chambre-vue-piscine": ("Chambre 3", "Le réveil, face à la piscine"),
       "chambre-cartes": ("Chambre 3", "Lit king size et cartes anciennes"),
       "chambre-blanche": ("Chambre 4", "Volets blancs et lit à baldaquin"),
       "chambre5": ("Chambre 5", "Lit king size"),
       "chambre5-sdb": ("Chambre 5", "La salle de bain")},
"en": {"vue-mer": ("The view", "The ocean and Dominica from the garden"),
       "maison-principale": ("The main house", "Gallery and tropical garden"),
       "piscine-maison": ("The pool house", "Three bedrooms with bathrooms, facing the pool"),
       "piscine": ("The pool", "Heated saltwater and a wooden deck"),
       "galerie": ("The gallery", "Over 80 m² open to the garden and the sea"),
       "salon-vue-mer": ("The cathedral living room", "Tall doors open to the sea"),
       "salon": ("The cathedral living room", "Linen, rattan and white wood, at night"),
       "grande-table": ("The long table", "Twelve seats under the gallery, at night"),
       "table-dressee": ("Dinner", "The table set facing the garden"),
       "cuisine": ("The kitchen", "Fully equipped, open onto the gallery"),
       "cuisine-ete": ("The summer kitchen", "Gas barbecue and plancha"),
       "cuisine-ete-2": ("The summer kitchen", "Along the house, in the shade"),
       "chambre-baldaquin": ("Bedroom 1", "King bed and mosquito net"),
       "chambre-soir": ("Bedroom 1", "The same room, at night"),
       "chambre-enfants": ("Bedroom 2", "Bunk beds for four children"),
       "chambre-enfants-2": ("Bedroom 2", "With its own shower"),
       "chambre-vue-piscine": ("Bedroom 3", "Waking up facing the pool"),
       "chambre-cartes": ("Bedroom 3", "King bed and antique maps"),
       "chambre-blanche": ("Bedroom 4", "White shutters and canopy bed"),
       "chambre5": ("Bedroom 5", "King bed"),
       "chambre5-sdb": ("Bedroom 5", "The bathroom")},
"es": {"vue-mer": ("La vista", "El océano y Dominica desde el jardín"),
       "maison-principale": ("La casa principal", "Galería y jardín tropical"),
       "piscine-maison": ("La casa de la piscina", "Tres habitaciones con baño, frente a la piscina"),
       "piscine": ("La piscina", "Agua salada climatizada y terraza de madera"),
       "galerie": ("La galería", "Más de 80 m² abiertos al jardín y al mar"),
       "salon-vue-mer": ("El salón catedral", "Grandes puertas abiertas al mar"),
       "salon": ("El salón catedral", "Lino, ratán y madera blanca, de noche"),
       "grande-table": ("La gran mesa", "Doce comensales bajo la galería, de noche"),
       "table-dressee": ("La cena", "La mesa puesta frente al jardín"),
       "cuisine": ("La cocina", "Equipada y abierta a la galería"),
       "cuisine-ete": ("La cocina de verano", "Barbacoa de gas y plancha"),
       "cuisine-ete-2": ("La cocina de verano", "Junto a la casa, a la sombra"),
       "chambre-baldaquin": ("Habitación 1", "Cama king y mosquitera"),
       "chambre-soir": ("Habitación 1", "La misma habitación, de noche"),
       "chambre-enfants": ("Habitación 2", "Literas para cuatro niños"),
       "chambre-enfants-2": ("Habitación 2", "Con su ducha"),
       "chambre-vue-piscine": ("Habitación 3", "Despertar frente a la piscina"),
       "chambre-cartes": ("Habitación 3", "Cama king y mapas antiguos"),
       "chambre-blanche": ("Habitación 4", "Contraventanas blancas y cama con dosel"),
       "chambre5": ("Habitación 5", "Cama king"),
       "chambre5-sdb": ("Habitación 5", "El baño")},
}
# Photos de chaque chambre (la première est la photo principale)
ROOMS = {
    "house1": [("r1", "king", ["chambre-baldaquin", "chambre-soir"]),
               ("r2", "bunks", ["chambre-enfants", "chambre-enfants-2"])],
    "house2": [("r3", "king_bath", ["chambre-vue-piscine", "chambre-cartes"]),
               ("r4", "king_bath", ["chambre-blanche"]),
               ("r5", "king_bath", ["chambre5", "chambre5-sdb"])],
}

# ------------------------------------------------------------------
# MARIE-GALANTE — expériences (photo, catégorie, titre, texte) et infos pratiques
# Déposez les photos dans img/ avec le nom indiqué : elles remplacent le fond coloré.
# ------------------------------------------------------------------
ILE = {
"fr": dict(
    titre="Marie-Galante, l'île aux cent moulins",
    intro="Ronde comme une galette, posée sur une mer turquoise, Marie-Galante a gardé ce que les Antilles ont parfois perdu : des plages sans foule, des champs de canne à perte de vue et une douceur de vivre authentique. Voici ce qui vous attend, à quelques minutes de la villa.",
    exp=[("ile-plages", "Se baigner", "Les plages", "Anse Canot, Petite-Anse, la Feuillère : sable blanc, lagons turquoise, et souvent personne d'autre que vous."),
         ("ile-rhum", "Goûter", "Le rhum agricole", "Bielle, Bellevue et Père Labat ouvrent leurs chais. Le rhum de l'île est réputé dans toute la Caraïbe."),
         ("ile-moulins", "Flâner", "Les cent moulins", "Anciens moulins à vent de pierre au milieu des cannes. Celui de Bézard a retrouvé ses ailes."),
         ("ile-gouffre", "S'émerveiller", "Gueule Grand Gouffre", "Au nord de l'île, l'Atlantique s'engouffre sous une arche de falaise. Un spectacle saisissant."),
         ("ile-charrettes", "Rencontrer", "Les charrettes à bœufs", "Pendant la récolte, les charrettes tirées par des bœufs transportent encore la canne vers les distilleries."),
         ("ile-murat", "Comprendre", "L'Habitation Murat", "Ancienne sucrerie devenue écomusée, tout près de Grand-Bourg, au cœur de l'histoire de l'île."),
         ("ile-mer", "Explorer", "Les fonds marins", "Snorkeling, plongée, sorties en bateau ou pêche : la mer se découvre à quelques minutes de la villa."),
         ("ile-terre-de-blues", "Vibrer", "Terre de Blues", "Chaque année au printemps, le festival fait vibrer l'île au son du blues et des musiques caribéennes."),
         ("ile-table", "Savourer", "La table créole", "Langouste grillée les pieds dans le sable, bébélé, sorbet coco : la cuisine marie-galantaise se savoure face à la mer.")],
    acc_h="Préparer votre séjour",
    acc=[("Venir à Marie-Galante", "En bateau depuis Pointe-à-Pitre jusqu'au port de Grand-Bourg, en une heure environ. Ou en petit avion jusqu'à l'aérodrome de l'île. La villa est à 3 km du bourg et du port."),
         ("Se déplacer sur l'île", "Une voiture de location est conseillée pour profiter des plages et des sites. L'île est petite : tout est à moins de 30 minutes en voiture."),
         ("Quand venir", "Toute l'année. La saison sèche, de décembre à mai, est la plus prisée. Le festival Terre de Blues a lieu chaque année au printemps."),
         ("Notre conciergerie vous aide", "Billets de bateau, voiture de location, chef à domicile, sorties en mer : Fabie organise tout et vous fait bénéficier des codes promo MGVIP auprès de ses partenaires.")],
),
"en": dict(
    titre="Marie-Galante, the island of a hundred windmills",
    intro="Round as a galette and set in a turquoise sea, Marie-Galante has kept what the Caribbean has sometimes lost: uncrowded beaches, endless sugar cane fields and an authentic, gentle way of life. Here is what awaits you, a few minutes from the villa.",
    exp=[("ile-plages", "Swim", "The beaches", "Anse Canot, Petite-Anse, La Feuillère: white sand, turquoise lagoons, and often no one else but you."),
         ("ile-rhum", "Taste", "Agricultural rum", "Bielle, Bellevue and Père Labat open their cellars. The island's rum is famous across the Caribbean."),
         ("ile-moulins", "Wander", "The hundred windmills", "Old stone windmills among the cane fields. The one at Bézard has its sails back."),
         ("ile-gouffre", "Marvel", "Gueule Grand Gouffre", "In the north of the island, the Atlantic rushes under a cliff arch. A striking sight."),
         ("ile-charrettes", "Meet", "Ox carts", "During the harvest, ox-drawn carts still carry the cane to the distilleries."),
         ("ile-murat", "Discover", "Habitation Murat", "A former sugar estate turned eco-museum, close to Grand-Bourg, at the heart of the island's history."),
         ("ile-mer", "Explore", "Under the sea", "Snorkelling, diving, boat trips or fishing: the sea is a few minutes from the villa."),
         ("ile-terre-de-blues", "Feel the beat", "Terre de Blues", "Every spring, the festival fills the island with blues and Caribbean music."),
         ("ile-table", "Savour", "Creole cuisine", "Grilled lobster with your feet in the sand, bébélé, coconut sorbet: the island's cooking is best enjoyed facing the sea.")],
    acc_h="Plan your stay",
    acc=[("Getting to Marie-Galante", "By ferry from Pointe-à-Pitre to Grand-Bourg harbour, in about one hour. Or by small plane to the island's airfield. The villa is 3 km from town and the harbour."),
         ("Getting around", "A rental car is recommended to enjoy the beaches and sights. The island is small: everything is less than 30 minutes away by car."),
         ("When to come", "All year round. The dry season, from December to May, is the most popular. The Terre de Blues festival takes place every spring."),
         ("Our concierge helps you", "Ferry tickets, rental car, private chef, boat trips: Fabie arranges everything and gives you MGVIP promo codes with her partners.")],
),
"es": dict(
    titre="Marie-Galante, la isla de los cien molinos",
    intro="Redonda como una galleta y rodeada de un mar turquesa, Marie-Galante conserva lo que el Caribe a veces ha perdido: playas sin multitudes, campos de caña hasta el horizonte y una forma de vida auténtica y serena. Esto es lo que le espera, a pocos minutos de la villa.",
    exp=[("ile-plages", "Bañarse", "Las playas", "Anse Canot, Petite-Anse, La Feuillère: arena blanca, lagunas turquesa y, a menudo, nadie más que usted."),
         ("ile-rhum", "Degustar", "El ron agrícola", "Bielle, Bellevue y Père Labat abren sus bodegas. El ron de la isla es famoso en todo el Caribe."),
         ("ile-moulins", "Pasear", "Los cien molinos", "Antiguos molinos de viento de piedra entre los campos de caña. El de Bézard ha recuperado sus aspas."),
         ("ile-gouffre", "Maravillarse", "Gueule Grand Gouffre", "Al norte de la isla, el Atlántico entra bajo un arco de acantilado. Un espectáculo impresionante."),
         ("ile-charrettes", "Conocer", "Las carretas de bueyes", "Durante la zafra, las carretas tiradas por bueyes aún llevan la caña a las destilerías."),
         ("ile-murat", "Descubrir", "La Habitation Murat", "Antigua hacienda azucarera convertida en ecomuseo, cerca de Grand-Bourg, en el corazón de la historia de la isla."),
         ("ile-mer", "Explorar", "Los fondos marinos", "Esnórquel, buceo, salidas en barco o pesca: el mar está a pocos minutos de la villa."),
         ("ile-terre-de-blues", "Vibrar", "Terre de Blues", "Cada primavera, el festival llena la isla de blues y músicas caribeñas."),
         ("ile-table", "Saborear", "La cocina criolla", "Langosta a la parrilla con los pies en la arena, bébélé, sorbete de coco: la cocina de la isla se saborea frente al mar.")],
    acc_h="Prepare su estancia",
    acc=[("Llegar a Marie-Galante", "En barco desde Pointe-à-Pitre hasta el puerto de Grand-Bourg, en una hora aproximadamente. O en avioneta hasta el aeródromo de la isla. La villa está a 3 km del pueblo y del puerto."),
         ("Moverse por la isla", "Se recomienda alquilar un coche para disfrutar de las playas y los lugares de interés. La isla es pequeña: todo está a menos de 30 minutos en coche."),
         ("Cuándo venir", "Todo el año. La temporada seca, de diciembre a mayo, es la más solicitada. El festival Terre de Blues se celebra cada primavera."),
         ("Nuestra conserjería le ayuda", "Billetes de barco, coche de alquiler, chef a domicilio, salidas en barco: Fabie lo organiza todo y le ofrece códigos promocionales MGVIP con sus socios.")],
),
}

# Crédits photo affichés en petit sur chaque photo de Marie-Galante (laisser "" si inconnu)
CREDITS = {
    "ile-plages": "© Guillaume Aricique", "ile-rhum": "© CIRT DOM", "ile-moulins": "© Fédération française des moulins",
    "ile-gouffre": "© Les îles de la Guadeloupe", "ile-charrettes": "© Marie-Galante VIP",
    "ile-murat": "© Office de tourisme de Marie-Galante", "ile-mer": "© Ultramarina",
    "ile-terre-de-blues": "© Festival Terre de Blues", "ile-table": "© Les îles de la Guadeloupe",
}

RESA_PAGE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Réservation | Villa La Vanille</title>
<meta http-equiv="refresh" content="2;url={URL}">
<style>
  html,body{height:100%;margin:0}
  body{display:grid;place-items:center;background:#F3EFE8;color:#23292B;font:300 1rem/1.6 "Jost",system-ui,sans-serif;text-align:center}
  h1{font:300 2.4rem/1.1 "Cormorant Garamond",Georgia,serif;margin:0 0 1rem;letter-spacing:.04em}
  p{margin:.2rem 0;color:#6E7674}
  .barre{width:160px;height:1px;background:#d6cfc3;margin:1.6rem auto;overflow:hidden}
  .barre span{display:block;height:100%;width:0;background:#8C6A48;animation:p 1.8s ease forwards}
  @keyframes p{to{width:100%}}
  a{color:#23292B}
</style>
</head>
<body data-event="clic_reservation">
  <main>
    <h1>Villa La Vanille</h1>
    <p>Redirection vers le calendrier de réservation…</p>
    <p>Redirecting to the booking calendar…</p>
    <p>Redirigiendo al calendario de reservas…</p>
    <div class="barre"><span></span></div>
    <p><a href="{URL}">Continuer / Continue / Continuar</a></p>
  </main>
  <script src="/consent.js"></script>
  <script>setTimeout(function(){ location.replace("{URL}"); }, 1800);</script>
</body>
</html>
"""

SCORES = ["4,8", "5,0", "5,0", "4,9", "5,0", "4,9"]
CUR = ' aria-current="true"'


def num(s, lang):
    return s.replace(",", ".") if lang == "en" else s


def jsonld(lang, t):
    return json.dumps({
        "@context": "https://schema.org", "@type": "VacationRental",
        "name": "Villa La Vanille", "description": t["desc"],
        "url": CONFIG["domain"] + "/" + PATHS[lang],
        "image": [CONFIG["domain"] + "/img/" + f for f in ["piscine-maison.jpg", "galerie.jpg", "grande-table.jpg", "chambre-vue-piscine.jpg"]],
        "address": {"@type": "PostalAddress", "streetAddress": "Section Lalane", "addressLocality": "Grand-Bourg", "postalCode": "97112",
                    "addressRegion": "Guadeloupe", "addressCountry": "GP"},
        "containsPlace": {"@type": "Accommodation", "occupancy": {"@type": "QuantitativeValue", "value": 12},
                          "numberOfBedrooms": 5, "numberOfBathroomsTotal": 5},
        "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": n, "value": True}
                           for n in ["Pool", "Sea view", "Air conditioning", "Wifi", "Barbecue"]],
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": 4.94, "reviewCount": 17, "bestRating": 5},
        "telephone": CONFIG["phone"], "email": CONFIG["email"],
        "sameAs": [u for u in [CONFIG["airbnb"], CONFIG["instagram"]] if u],
    }, ensure_ascii=False, indent=2)


def page(lang):
    t = T[lang]
    p = "" if lang == "fr" else "../"
    def lang_links():
        return "".join(f'<a href="{p}{PATHS[l]}index.html" hreflang="{l}" lang="{l}"{CUR if l == lang else ""}>{l.upper()}</a>' for l in LANGS)
    alt = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{CONFIG["domain"]}/{PATHS[l]}">' for l in LANGS)
    scores = "".join(f'<li><strong>{num(v, lang)}</strong><span>{k}</span></li>' for k, v in zip(t["s"], SCORES))
    quotes = ""
    if QUOTES:
        quotes = '<div class="quotes">' + "".join(
            f'<blockquote>« {html.escape(q["text"])} »<cite>{html.escape(q["who"])}</cite></blockquote>' for q in QUOTES) + "</div>"
    presta = "".join(f"<li>{x}</li>" for x in t["pr"])
    rules = "".join(f"<li>{x}</li>" for x in t["rules"])
    TODO = '<span class="todo">' + ("À compléter" if lang == "fr" else "To complete" if lang == "en" else "Por completar") + '</span>'
    def eur(v):
        n = f"{v:,}"
        return ("€" + n) if lang == "en" else n.replace(",", "\u202f" if lang == "fr" else ".") + "\u00a0€"
    rows = "".join(f'<tr><td>{n} {t["ch1"] if n == 1 else t["chn"]}</td><td>{eur(pn)}</td><td>{eur(pw)}</td></tr>' for n, pn, pw in TARIFS)
    saisons = (f'<div class="grille"><table><thead><tr><th>{t["col_opt"]}</th><th>{t["col_n"]}</th><th>{t["col_w"]}</th></tr></thead>'
               f'<tbody>{rows}</tbody></table></div>')
    conds = "".join(f"<div><dt>{k}</dt><dd>{v or TODO}</dd></div>" for k, v in CONDITIONS[lang])
    reg = CONFIG["registration"]
    reg_html = f'<span class="todo">{reg}</span>' if "COMPL" in reg else reg
    insta = f'<a href="{CONFIG["instagram"]}">Instagram</a><br>' if CONFIG["instagram"] else ""
    AL = t["alt"]
    CP = CAPTIONS[lang]
    def carrousel(head, slides, n, cls=""):
        return (f'<div class="carrousel {cls}"><div class="wrap g-head">{head}'
                f'<div class="g-nav"><span class="compteur small">01 / {n:02d}</span>'
                f'<button type="button" class="c-prev" aria-label="{t["prev"]}"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg></button>'
                f'<button type="button" class="c-next" aria-label="{t["next"]}"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg></button></div></div>'
                f'<div class="piste" data-group tabindex="0">{slides}</div></div>')
    def slide(pics, title, sub, centre=False):
        imgs = "".join(f'<button type="button" class="zoomg" aria-label="{AL[n]}"><img src="{p}img/{n}.jpg" alt="{AL[n]}" loading="lazy"></button>' for n in pics)
        cls = "slide centre" if centre or len(pics) > 1 else "slide"
        return (f'<figure class="{cls}"><div class="pics n{len(pics)}">{imgs}</div>'
                f'<figcaption><strong>{title}</strong><span>{sub}</span></figcaption></figure>')
    def house(k):
        slides = "".join(slide(pics, t[r], t[d], True) for r, d, pics in ROOMS[k])
        return carrousel(f'<h3 class="house-t">{t[k]}</h3>', slides, len(ROOMS[k]), "rooms-c")
    # Galerie : les photos consécutives qui portent le même titre sont regroupées sur une seule vignette
    groupes = []
    for n in GALLERY:
        if groupes and CP[groupes[-1][0]][0] == CP[n][0]:
            groupes[-1].append(n)
        else:
            groupes.append([n])
    gallery = "".join(slide(g, CP[g[0]][0], CP[g[0]][1]) for g in groupes)
    I = ILE[lang]
    def exp_slide(img, tag, title, txt):
        if os.path.exists(os.path.join(OUT, "img", img + ".jpg")):
            pic = f'<button type="button" class="zoomg" aria-label="{title}"><img src="{p}img/{img}.jpg" alt="{title}" loading="lazy"></button>'
        else:
            pic = f'<div class="ph-ile" aria-hidden="true"><span>{img}.jpg</span></div>'
        cr = CREDITS.get(img, "")
        if cr:
            pic = f'<div class="cr-wrap">{pic}<small class="credit">{cr}</small></div>'
        return (f'<figure class="slide exp">{pic}<figcaption><em>{tag}</em><strong>{title}</strong><span>{txt}</span></figcaption></figure>')
    ile_slides = "".join(exp_slide(*e) for e in I["exp"])
    PLUS = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>'
    accs = "".join(f'<details class="acc"><summary><span>{q}</span>{PLUS}</summary><p>{r}</p></details>' for q, r in I["acc"])
    nb = len(groupes)
    B = ("" if lang == "fr" else "../") + "reservation/"
    EXT = ' target="_blank" rel="noopener"'

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t["title"]}</title>
<meta name="description" content="{t["desc"]}">
<link rel="canonical" href="{CONFIG["domain"]}/{PATHS[lang]}">
{alt}
<link rel="alternate" hreflang="x-default" href="{CONFIG["domain"]}/">
<meta property="og:type" content="website">
<meta property="og:title" content="{t["title"]}">
<meta property="og:description" content="{t["desc"]}">
<meta property="og:image" content="{CONFIG["domain"]}/img/piscine-maison.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300&family=Jost:wght@300;400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}style.css">
<script type="application/ld+json">
{jsonld(lang, t)}
</script>
</head>
<body>

<header class="top">
  <div class="bar">
    <nav class="pill" aria-label="Menu">
      <a href="#villa">{t["m_villa"]}</a>
      <a href="#chambres">{t["m_rooms"]}</a>
      <a href="#tarifs">{t["m_tarifs"]}</a>
    </nav>
    <div class="side">
      <div class="langs pill-s">{lang_links()}</div>
      <a class="btn-dispo" href="{B}"{EXT}><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg><span>{t["dispo"]}</span></a>
    </div>
  </div>
</header>

<main>
<div class="hero" id="accueil">
  <img src="{p}img/piscine-maison.jpg" alt="{AL["piscine-maison"]}" fetchpriority="high">
  <div class="hero-text wrap">
    <span class="small">{t["place"]}</span>
    <h1>Villa La Vanille</h1>
    <p>{t["hero_p"]}</p>
    <a class="btn" href="{B}"{EXT}>{t["dispo"]}</a>
  </div>
  <span class="scroll" aria-hidden="true"></span>
</div>

<section class="intro">
  <div class="wrap">
    <span class="small" style="color:var(--teck)">{t["intro_k"]}</span>
    <p class="lede">{t["lede"]}</p>
    <ul class="chiffres">
      <li><strong>12</strong><span>{t["c1"]}</span></li>
      <li><strong>5</strong><span>{t["c2"]}</span></li>
      <li><strong>5</strong><span>{t["c3"]}</span></li>
      <li><strong>2 000</strong><span>{t["c4"]}</span></li>
    </ul>
  </div>
</section>

<section id="villa" style="padding-top:0">
  <div class="wrap">
    <h2>{t["v_h"]}</h2>
    <div class="row">
      <figure><img src="{p}img/piscine.jpg" alt="{AL["piscine"]}" loading="lazy"></figure>
      <div class="txt"><span class="num">I</span><h3>{t["v0h"]}</h3><p>{t["v0"]}</p></div>
    </div>
    <div class="row inv">
      <figure><img src="{p}img/galerie.jpg" alt="{AL["galerie"]}" loading="lazy"></figure>
      <div class="txt"><span class="num">II</span><h3>{t["v1h"]}</h3><p>{t["v1"]}</p></div>
    </div>
    <div class="row">
      <figure class="duo"><img src="{p}img/salon-vue-mer.jpg" alt="{AL["salon-vue-mer"]}" loading="lazy"><img src="{p}img/salon.jpg" alt="{AL["salon"]}" loading="lazy"></figure>
      <div class="txt"><span class="num">III</span><h3>{t["vsh"]}</h3><p>{t["vs"]}</p></div>
    </div>
    <div class="row inv">
      <figure><img src="{p}img/grande-table.jpg" alt="{AL["grande-table"]}" loading="lazy"></figure>
      <div class="txt"><span class="num">IV</span><h3>{t["v2h"]}</h3><p>{t["v2"]}</p></div>
    </div>
    <div class="row">
      <div class="carrousel mini">
        <div class="piste" data-group tabindex="0">{"".join(f'<figure class="slide"><button type="button" class="zoomg" aria-label="{AL[n]}"><img src="{p}img/{n}.jpg" alt="{AL[n]}" loading="lazy"></button></figure>' for n in ["cuisine", "cuisine-ete", "cuisine-ete-2"])}</div>
        <div class="g-nav"><span class="compteur small">01 / 03</span>
          <button type="button" class="c-prev" aria-label="{t["prev"]}"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg></button>
          <button type="button" class="c-next" aria-label="{t["next"]}"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg></button></div>
      </div>
      <div class="txt"><span class="num">V</span><h3>{t["v3h"]}</h3><p>{t["v3"]}</p></div>
    </div>
  </div>
</section>

<section id="chambres" class="sable">
  <div class="wrap">
    <div class="head"><h2 style="margin:0">{t["r_h"]}</h2><p>{t["r_p"]}</p></div>
  </div>
  {house("house1")}
  {house("house2")}
  <div class="wrap"><p class="note">{t["r_note"]}</p></div>
</section>

<section id="prestations">
  <div class="wrap row presta-row">
    <figure class="tall" data-group><button type="button" class="zoomg" aria-label="{AL["vue-mer"]}"><img src="{p}img/vue-mer.jpg" alt="{AL["vue-mer"]}" loading="lazy"></button></figure>
    <div class="txt">
      <h2>{t["p_h"]}</h2>
      <p>{t["p_p"]}</p>
      <ul class="presta">{presta}</ul>
      <div class="concierge">
        <h3>{t["cz_h"]}</h3>
        <p>{t["cz_1"]}</p>
        <p>{t["cz_2"]}</p>
      </div>
    </div>
  </div>
</section>

<section id="galerie" style="padding-top:0">
  {carrousel('<h2 style="margin:0">' + t["g_h"] + '</h2>', gallery, nb)}
</section>

<dialog class="lb" id="lb" aria-label="{t["g_h"]}">
  <img src="" alt="">
  <div class="lb-bar">
    <button class="prev" type="button">{t["prev"]}</button>
    <span class="count small"></span>
    <button class="next" type="button">{t["next"]}</button>
    <button class="close" type="button">{t["close"]}</button>
  </div>
</dialog>

<section id="ile" class="sable ile">
  <div class="wrap ile-head">
    <h2>{I["titre"]}</h2>
    <p>{I["intro"]}</p>
  </div>
  {carrousel("", ile_slides, len(I["exp"]), "ile-c")}
  <div class="wrap ile-acc">
    <h3>{I["acc_h"]}</h3>
    <div>{accs}</div>
  </div>
</section>

<section class="avis" id="avis">
  <div class="wrap">
    <h2>{t["av_h"]}</h2>
    <p class="note-globale">{num("4,94", lang)}</p>
    <p class="sous">{t["av_s"]}</p>
    <ul class="scores">{scores}</ul>
    {quotes}
  </div>
</section>

<section id="tarifs" class="sable">
  <div class="wrap">
    <div class="head"><h2 style="margin:0">{t["t_h"]}</h2><p>{t["t_p"]}</p></div>
    {saisons}
    <div class="infos" style="margin-top:4.5rem">
      <div><h3 class="sub">{t["cond_h"]}</h3><dl>{conds}</dl></div>
      <div><h3 class="sub">{t["rules_h"]}</h3><ul class="presta">{rules}</ul></div>
    </div>
    <div style="margin-top:3.5rem"><a class="btn plein" href="{B}"{EXT}>{t["b_cal"]}</a></div>
  </div>
</section>

<section id="reserver" class="resa-v">
  <div class="wrap">
    <h2>{t["b_h"]}</h2>
    <p>{t["b_p"]}</p>
    <a class="btn plein" href="{B}"{EXT}>{t["b_cal"]}</a>
  </div>
</section>
</main>

<footer>
  <div class="wrap">
    <div class="cols">
      <div><a class="logo" href="#accueil">Villa La Vanille</a><p>Section Lalane<br>97112 Grand-Bourg, Marie-Galante<br>Guadeloupe</p>
        <div class="carte-f" data-src="https://maps.google.com/maps?q={quote(CONFIG["map_q"])}&z={CONFIG["map_zoom"]}&output=embed">
          <div class="carte-ph"><button type="button" class="carte-btn">{t["map_btn"]}</button><small>{t["map_note"]}</small></div>
        </div>
        <p class="carte-lien"><a href="https://www.google.com/maps/search/?api=1&query={quote(CONFIG["map_q"])}" target="_blank" rel="noopener">{t["map_open"]} ↗</a></p></div>
      <div><h4>{t["book"]}</h4><p><a href="{B}"{EXT}>{t["b_cal"]}</a></p><h4 style="margin-top:2rem">{t["blog"]}</h4><p><a href="{p}{PATHS[lang]}blog/index.html">{t["blog_t"]}</a></p></div>
      <div class="contact-f"><h4>{t["f_contact"]}</h4><p><a href="tel:{CONFIG["phone"].replace(" ", "")}">{CONFIG["phone"]}</a><br><a href="mailto:{CONFIG["email"]}">{CONFIG["email"]}</a></p></div>
    </div>
    <div class="legal"><span class="langs foot-langs">{lang_links()}</span><span><a href="{p}legal/mentions-legales.html">{t["legal"]}</a> · <a href="{p}legal/confidentialite.html">{t["lg2"]}</a> · <a href="{p}legal/cgv.html">{t["lg3"]}</a> · <a href="{p}legal/conditions-utilisation.html">{t["lg4"]}</a> · <a href="#" id="gerer-cookies">{t["ck_g"]}</a>&nbsp;&nbsp; © Villa La Vanille</span></div>
  </div>
</footer>

<div id="cookies" class="cookies" hidden role="dialog" aria-label="Cookies">
  <p>{t["ck_t"]}</p>
  <div><button type="button" class="c-non">{t["ck_non"]}</button><button type="button" class="c-ok">{t["ck_ok"]}</button></div>
</div>
<script src="{p}consent.js"></script>
<script src="{p}script.js"></script>
</body>
</html>
"""


def build():
    import legal
    legal.build(OUT)
    for lang in LANGS:
        d = os.path.join(OUT, PATHS[lang])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(page(lang))
    for name in ["style.css", "script.js", "consent.js"]:
        if os.path.abspath(HERE) != OUT:
            shutil.copy(os.path.join(HERE, name), os.path.join(OUT, name))
    # Page intermédiaire /reservation/ : mesure les clics de réservation, puis redirige vers Octorate
    os.makedirs(os.path.join(OUT, "reservation"), exist_ok=True)
    with open(os.path.join(OUT, "reservation", "index.html"), "w", encoding="utf-8") as f:
        f.write(RESA_PAGE.replace("{URL}", CONFIG["booking"]))
    import blog
    ck = {l: {k: T[l][k] for k in ("ck_t", "ck_ok", "ck_non")} for l in LANGS}
    blog_urls = blog.build(OUT, HERE, CONFIG["domain"], ck)
    urls = "".join(f"  <url><loc>{CONFIG['domain']}/{u}</loc></url>\n" for u in [PATHS[l] for l in LANGS] + blog_urls)
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {CONFIG['domain']}/sitemap.xml\n")
    print("Site généré dans", OUT)


if __name__ == "__main__":
    build()
