# -*- coding: utf-8 -*-
"""Pages légales de Villa La Vanille (en français, langue juridique de référence)."""
import os

# ------------------------------------------------------------------
# À COMPLÉTER : informations sur le propriétaire (éditeur du site)
# Laisser None pour afficher « à compléter » en jaune.
# ------------------------------------------------------------------
LEGAL = {
    "editeur": "SCI MANDEL 4",
    "statut": "société civile immobilière au capital de 1 020 €, immatriculée au RCS de Paris sous le numéro 808 352 496, représentée par ses dirigeants, Fabien Radisic et Nadine Radisic (née Loret)",
    "adresse": "38 avenue Georges Mandel, 75016 Paris",
    "siret": "808 352 496 00018",
    "email": "radisic.thomas@gmail.com",
    "directeur": "Thomas Radisic",
    "mediateur": None,      # à compléter : nom et site du médiateur de la consommation
    "maj": "6 novembre 2026",
}

HEBERGEUR = "Netlify, Inc., 44 Montgomery Street, Suite 300, San Francisco, CA 94104, États-Unis – www.netlify.com"


def v(key):
    val = LEGAL[key]
    return val if val else '<span class="todo">à compléter</span>'


PAGES = {
"mentions-legales": ("Mentions légales", lambda: f"""
<h2>Éditeur du site</h2>
<p>Le site www.villalavanille.fr est édité par {v("editeur")}, {v("statut")}.<br>
Adresse : {v("adresse")}<br>
{("SIRET : " + LEGAL["siret"] + "<br>") if LEGAL["siret"] else ""}Contact : {LEGAL["email"]}</p>
<h2>Directeur de la publication</h2>
<p>{v("directeur")}</p>
<h2>Hébergeur</h2>
<p>{HEBERGEUR}</p>
<h2>Propriété intellectuelle</h2>
<p>Les textes, la mise en page et les photographies de la villa sont la propriété de l'éditeur. Les photographies de Marie-Galante appartiennent à leurs auteurs, crédités sur chaque image. Toute reproduction sans autorisation est interdite.</p>
<h2>Réservations</h2>
<p>Les réservations sont gérées par la conciergerie Kaza Marie Galante, via sa plateforme de réservation en ligne. Voir les <a href="cgv.html">conditions générales de vente</a>.</p>
"""),

"confidentialite": ("Politique de confidentialité", lambda: f"""
<h2>Responsable du traitement</h2>
<p>{v("editeur")}, {v("adresse")}. Contact : {LEGAL["email"]}</p>
<h2>Données collectées sur ce site</h2>
<p>Le site ne comporte aucun formulaire et ne collecte ni nom, ni adresse e-mail, ni numéro de téléphone. Les seules données traitées sont des données de mesure d'audience, et uniquement si vous les acceptez.</p>
<h2>Cookies de mesure d'audience</h2>
<p>Avec votre accord, nous utilisons Google Analytics et Google Ads (Google Ireland Ltd) pour savoir combien de personnes visitent le site, quelles pages sont consultées et combien de visiteurs cliquent sur le bouton de réservation. Ces outils déposent des cookies conservés 13 mois au maximum. Ils ne sont activés que si vous cliquez sur « Accepter » dans le bandeau. Vous pouvez changer d'avis à tout moment avec le lien « Gérer les cookies » en bas de chaque page.</p>
<p>Base légale : votre consentement. Les données peuvent être transférées aux États-Unis, dans le cadre du Data Privacy Framework UE–États-Unis.</p>
<h2>Carte Google Maps</h2>
<p>La carte affichée en bas de page est fournie par Google Maps, qui dépose ses propres cookies. Elle ne se charge que si vous avez accepté les cookies ou si vous cliquez sur « Afficher la carte ».</p>
<h2>Réservations</h2>
<p>Lorsque vous cliquez sur « Réserver », vous êtes dirigé vers la plateforme de réservation de la conciergerie Kaza Marie Galante. Les données saisies lors de la réservation sont traitées par cette conciergerie, selon sa propre politique de confidentialité.</p>
<h2>Vos droits</h2>
<p>Conformément au RGPD, vous disposez d'un droit d'accès, de rectification, d'effacement, d'opposition et de limitation sur vos données. Pour les exercer : {LEGAL["email"]}. Vous pouvez aussi adresser une réclamation à la CNIL (www.cnil.fr).</p>
"""),

"cgv": ("Conditions générales de vente", lambda: f"""
<h2>Objet</h2>
<p>Les présentes conditions encadrent la location saisonnière de la Villa La Vanille, à Grand-Bourg, Marie-Galante (Guadeloupe). La réservation est conclue en ligne sur la plateforme de la conciergerie Kaza Marie Galante. Les conditions affichées au moment de la réservation sur cette plateforme prévalent en cas de différence.</p>
<h2>Capacité</h2>
<p>La villa accueille jusqu'à 12 personnes dans 5 chambres. Le nombre d'occupants ne peut pas dépasser celui indiqué lors de la réservation.</p>
<h2>Prix</h2>
<p>Les prix sont indiqués par nuit et par semaine, selon le nombre de chambres ouvertes (voir la rubrique Tarifs du site). Ils s'entendent hors périodes de fêtes et du festival Terre de Blues, pour lesquelles un tarif spécifique s'applique. Des frais de service de 290 € s'ajoutent à chaque séjour.</p>
<h2>Taxe de séjour</h2>
<p>La taxe de séjour, de 2 € par personne et par nuit, est calculée selon les modalités fournies par les autorités locales. Elle est identique quelle que soit la provenance de la réservation.</p>
<h2>Durée</h2>
<p>Le séjour minimum est de 3 nuits. Arrivée à partir de 18 h, départ avant 10 h.</p>
<h2>Paiement</h2>
<p>Le règlement se fait par carte bancaire : 50 % à la réservation, le solde 30 jours avant l'arrivée.</p>
<h2>Caution</h2>
<p>Une caution de 1 500 € est demandée. Elle est restituée après l'état des lieux de sortie, déduction faite des éventuels dégâts constatés.</p>
<h2>Annulation</h2>
<p>Les conditions d'annulation sont celles indiquées lors de la réservation. Une assurance annulation de voyage est proposée, à partir de 3 % du montant du séjour. Conformément à l'article L221-28 du Code de la consommation, le droit de rétractation ne s'applique pas aux locations d'hébergement fournies à une date déterminée.</p>
<h2>Règlement intérieur</h2>
<p>Les animaux ne sont pas admis. Les fêtes et événements sont interdits ; les dîners entre amis sont les bienvenus, dans le respect du voisinage. La piscine n'est pas surveillée : la baignade se fait sous la responsabilité des voyageurs, et les enfants restent sous la surveillance de leurs parents. La villa n'est pas adaptée aux tout-petits.</p>
{("<h2>Médiation</h2><p>En cas de litige, vous pouvez recourir gratuitement à un médiateur de la consommation : " + LEGAL["mediateur"] + ".</p>") if LEGAL["mediateur"] else ""}
<h2>Droit applicable</h2>
<p>Les présentes conditions sont soumises au droit français.</p>
"""),

"conditions-utilisation": ("Conditions d'utilisation", lambda: f"""
<h2>Accès au site</h2>
<p>Le site www.villalavanille.fr présente la Villa La Vanille et permet d'accéder à sa plateforme de réservation. Il est accessible gratuitement. L'éditeur peut le modifier ou le suspendre à tout moment, sans préavis.</p>
<h2>Informations</h2>
<p>Les informations (descriptions, photos, tarifs) sont données à titre indicatif et peuvent évoluer. Seules les informations affichées lors de la réservation font foi.</p>
<h2>Propriété intellectuelle</h2>
<p>Les contenus du site sont protégés. Toute reproduction, totale ou partielle, sans autorisation écrite est interdite. Les photographies de Marie-Galante restent la propriété de leurs auteurs, crédités sur chaque image.</p>
<h2>Liens</h2>
<p>Le site contient des liens vers des sites tiers, notamment la plateforme de réservation. L'éditeur n'est pas responsable de leur contenu.</p>
<h2>Responsabilité</h2>
<p>L'éditeur s'efforce de fournir des informations exactes, mais ne peut garantir l'absence d'erreurs ou d'interruptions du site.</p>
<h2>Droit applicable</h2>
<p>Ces conditions sont soumises au droit français.</p>
"""),
}

NAV = [("mentions-legales", "Mentions légales"), ("confidentialite", "Politique de confidentialité"),
       ("cgv", "Conditions générales de vente"), ("conditions-utilisation", "Conditions d'utilisation")]


def build(out):
    d = os.path.join(out, "legal")
    os.makedirs(d, exist_ok=True)
    for slug, (titre, corps) in PAGES.items():
        nav = " · ".join(f'<a href="{s}.html"{" aria-current=\"page\"" if s == slug else ""}>{t}</a>' for s, t in NAV)
        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titre} | Villa La Vanille</title>
<meta name="robots" content="noindex, follow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400&family=Jost:wght@300;400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../style.css">
</head>
<body class="legal-page">
<header class="legal-top"><div class="wrap"><a class="legal-logo" href="../index.html">Villa La Vanille</a><a class="legal-back" href="../index.html">← Retour au site</a></div></header>
<main class="wrap legal-body">
<h1>{titre}</h1>
<p class="legal-maj">Dernière mise à jour : {LEGAL["maj"]}</p>
{corps()}
<nav class="legal-nav">{nav}</nav>
</main>
<div id="cookies" class="cookies" hidden role="dialog" aria-label="Cookies">
  <p>Nous utilisons des cookies de mesure d'audience (Google Analytics) pour comprendre comment le site est utilisé et l'améliorer. Vous pouvez les accepter ou les refuser.</p>
  <div><button type="button" class="c-non">Refuser</button><button type="button" class="c-ok">Accepter</button></div>
</div>
<script src="../consent.js"></script>
</body>
</html>
"""
        with open(os.path.join(d, slug + ".html"), "w", encoding="utf-8") as f:
            f.write(html)
