# -*- coding: utf-8 -*-
"""
Blog de Villa La Vanille.
Chaque article est un fichier JSON dans src/articles/ :
{
  "slug": "que-faire-a-marie-galante",          # adresse de l'article (sans accents ni espaces)
  "date": "2026-11-12",                          # date de publication AAAA-MM-JJ
  "image": "ile-plages.jpg",                     # photo de couverture, dans img/
  "credit": "© Guillaume Aricique",              # crédit photo (ou "")
  "fr": {"title": "...", "desc": "...", "body": "<p>...</p><h2>...</h2>..."},
  "en": {...}, "es": {...}
}
Le générateur crée /blog/ (FR), /en/blog/ (EN), /es/blog/ (ES), une page par article,
et renvoie la liste des adresses pour le sitemap.
"""
import glob, html, json, os

LANGS = ["fr", "en", "es"]
PREFIX = {"fr": "", "en": "en/", "es": "es/"}

T = {
    "fr": dict(blog="Le journal", intro="Idées de visites, conseils pratiques et bonnes adresses pour préparer votre séjour à Marie-Galante.",
               back="← Retour au journal", home="Retour au site", read="Lire l'article", cta_h="Séjourner à la Villa La Vanille",
               cta_p="Villa créole avec piscine et vue sur la mer, 5 chambres pour 12 personnes, à Grand-Bourg.",
               cta="Voir les disponibilités", villa="La villa", months=["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]),
    "en": dict(blog="The journal", intro="Places to visit, practical tips and good addresses to plan your stay in Marie-Galante.",
               back="← Back to the journal", home="Back to the site", read="Read the article", cta_h="Stay at Villa La Vanille",
               cta_p="Creole villa with pool and sea view, 5 bedrooms for 12 guests, in Grand-Bourg.",
               cta="Check availability", villa="The villa", months=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]),
    "es": dict(blog="El diario", intro="Lugares que visitar, consejos prácticos y buenas direcciones para preparar su estancia en Marie-Galante.",
               back="← Volver al diario", home="Volver al sitio", read="Leer el artículo", cta_h="Alojarse en Villa La Vanille",
               cta_p="Villa criolla con piscina y vista al mar, 5 habitaciones para 12 personas, en Grand-Bourg.",
               cta="Ver disponibilidad", villa="La villa", months=["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]),
}


def date_txt(d, lang):
    y, m, j = d.split("-")
    m = T[lang]["months"][int(m) - 1]
    return f"{int(j)} {m} {y}" if lang != "en" else f"{m} {int(j)}, {y}"


def charger(src):
    arts = []
    for f in glob.glob(os.path.join(src, "articles", "*.json")):
        with open(f, encoding="utf-8") as fh:
            arts.append(json.load(fh))
    arts.sort(key=lambda a: a["date"], reverse=True)
    return arts


def head(title, desc, lang, depth, canonical, alts, domain, extra=""):
    p = "../" * depth
    alt = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{domain}/{u}">' for l, u in alts)
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{domain}/{canonical}">
{alt}
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300&family=Jost:wght@300;400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}style.css">
{extra}
</head>
"""


def pied(lang, depth, ck):
    p = "../" * depth
    return f"""
<div id="cookies" class="cookies" hidden role="dialog" aria-label="Cookies">
  <p>{ck["ck_t"]}</p>
  <div><button type="button" class="c-non">{ck["ck_non"]}</button><button type="button" class="c-ok">{ck["ck_ok"]}</button></div>
</div>
<script src="{p}consent.js"></script>
</body>
</html>
"""


def entete(lang, depth, t):
    p = "../" * depth
    home = p + PREFIX[lang] + "index.html"
    return f"""<body class="blog-page">
<header class="legal-top"><div class="wrap"><a class="legal-logo" href="{home}">Villa La Vanille</a>
<nav class="blog-nav"><a href="{home}#villa">{t["villa"]}</a><a href="{p}{PREFIX[lang]}blog/index.html">{t["blog"]}</a><a class="btn-dispo" href="{p}reservation/">{t["cta"]}</a></nav></div></header>
"""


def build(out, src, domain, cookie_texts):
    """Génère le blog. Renvoie la liste des chemins à ajouter au sitemap."""
    arts = charger(src)
    urls = []
    for lang in LANGS:
        t = T[lang]
        ck = cookie_texts[lang]
        base = os.path.join(out, PREFIX[lang], "blog")
        os.makedirs(base, exist_ok=True)
        depth = 1 if lang == "fr" else 2
        p = "../" * depth
        # --- liste des articles
        cartes = ""
        for a in arts:
            c = a[lang]
            cartes += (f'<a class="b-carte" href="{a["slug"]}.html"><div class="b-img"><img src="{p}img/{a["image"]}" alt="{html.escape(c["title"])}" loading="lazy"></div>'
                       f'<p class="b-date">{date_txt(a["date"], lang)}</p><h2>{html.escape(c["title"])}</h2><p>{html.escape(c["desc"])}</p><span class="b-lire">{t["read"]}</span></a>')
        idx_alts = [(l, PREFIX[l] + "blog/") for l in LANGS]
        page = head(f'{t["blog"]} | Villa La Vanille, Marie-Galante', t["intro"], lang, depth, PREFIX[lang] + "blog/", idx_alts, domain)
        page += entete(lang, depth, t)
        page += f'<main class="wrap blog-body"><h1>{t["blog"]}</h1><p class="b-intro">{t["intro"]}</p><div class="b-grille">{cartes}</div></main>'
        page += pied(lang, depth, ck)
        with open(os.path.join(base, "index.html"), "w", encoding="utf-8") as f:
            f.write(page)
        urls.append(PREFIX[lang] + "blog/")
        # --- articles
        for a in arts:
            c = a[lang]
            alts = [(l, PREFIX[l] + "blog/" + a["slug"] + ".html") for l in LANGS]
            ld = json.dumps({"@context": "https://schema.org", "@type": "BlogPosting", "headline": c["title"],
                             "description": c["desc"], "datePublished": a["date"], "inLanguage": lang,
                             "image": f'{domain}/img/{a["image"]}',
                             "author": {"@type": "Organization", "name": "Villa La Vanille"},
                             "mainEntityOfPage": f'{domain}/{PREFIX[lang]}blog/{a["slug"]}.html'}, ensure_ascii=False)
            page = head(f'{c["title"]} | Villa La Vanille', c["desc"], lang, depth,
                        PREFIX[lang] + "blog/" + a["slug"] + ".html", alts, domain,
                        f'<script type="application/ld+json">{ld}</script>')
            page += entete(lang, depth, t)
            credit = f'<small class="credit">{html.escape(a.get("credit", ""))}</small>' if a.get("credit") else ""
            page += f"""<main class="article">
<div class="a-cover"><img src="{p}img/{a["image"]}" alt="{html.escape(c["title"])}">{credit}</div>
<div class="wrap a-body">
<p class="b-date">{date_txt(a["date"], lang)}</p>
<h1>{html.escape(c["title"])}</h1>
<p class="a-chapo">{html.escape(c["desc"])}</p>
{c["body"]}
<aside class="a-cta"><h2>{t["cta_h"]}</h2><p>{t["cta_p"]}</p><a class="btn plein" href="{p}reservation/">{t["cta"]}</a></aside>
<p><a class="a-back" href="index.html">{t["back"]}</a></p>
</div></main>"""
            page += pied(lang, depth, ck)
            with open(os.path.join(base, a["slug"] + ".html"), "w", encoding="utf-8") as f:
                f.write(page)
            urls.append(PREFIX[lang] + "blog/" + a["slug"] + ".html")
    return urls
