#!/usr/bin/env python3
"""
Récupère les derniers articles de presse sénégalaise, garde ceux qui
mentionnent probablement un accident de la circulation (filtre par
mots-clés), et écrit le résultat dans news-alerts.json à la racine du
dépôt. Ce fichier est ensuite lu par l'application (voir index.html,
fonction loadPressAlerts) pour alimenter le module "Alertes accidents"
avec des alertes venant de la presse, en plus de celles générées par les
signalements créés dans l'application elle-même.

Conçu pour tourner gratuitement via GitHub Actions (voir
.github/workflows/news-alerts.yml), sur un simple cron — pas de serveur ni
de service payant nécessaire.

Inclut aussi les vidéos de quelques chaînes YouTube d'actualité
sénégalaises, via leurs flux Atom publics (https://www.youtube.com/feeds/
videos.xml?channel_id=...) — un flux gratuit et sans clé API, contrairement
à l'API de recherche YouTube qui nécessite une clé Google Cloud. C'est plus
limité qu'une vraie recherche (on ne voit que les nouvelles vidéos des
chaînes suivies, pas toutes les vidéos YouTube mentionnant un accident),
mais ça reste gratuit et ne demande aucune configuration côté utilisateur.

Volontairement sans dépendance tierce autre que `requests` (déjà
disponible dans l'environnement GitHub Actions standard) : le parsing
RSS/Atom est fait à la main avec xml.etree, pour éviter de dépendre d'un
paquet comme feedparser qui peut ne pas être disponible partout.

Limite assumée : c'est un filtre par mots-clés simple, pas une analyse
sémantique. Il peut laisser passer quelques faux positifs (ex. un article
qui parle d'un "accident de parcours" au sens figuré) et en rater
d'autres (formulations inhabituelles). À ajuster au besoin en modifiant
KEYWORDS ci-dessous.

Note sur les identifiants de chaîne YouTube (YOUTUBE_CHANNELS) : ils n'ont
pas pu être vérifiés en direct au moment de l'écriture de ce script (accès
réseau restreint dans l'environnement de développement utilisé). Si une
chaîne ne remonte jamais rien, vérifiez son channel_id en ouvrant
`https://www.youtube.com/@nom-de-la-chaine`, affichage du code source de
la page (Ctrl+U), et recherche de "channelId" ou "externalId".
"""

import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import unescape

import requests

# Sources RSS de presse sénégalaise. Ajouter/retirer une source ici suffit —
# le reste du script s'adapte automatiquement.
FEEDS = [
    {"name": "SeneNews", "url": "https://www.senenews.com/feed"},
    {"name": "Sénégal7", "url": "https://senegal7.com/feed/"},
    {"name": "PresseAfrik (via presseAdakar)", "url": "http://news.adakar.com/xml/all.xml"},
    {"name": "AllAfrica — Sénégal", "url": "https://fr.allafrica.com/tools/headlines/rdf/senegal/headlines.rdf"},
]

# Chaînes YouTube d'actualité sénégalaises suivies (flux Atom publics, sans
# clé API). Le nom affiché précise "YouTube" pour que ce soit clair côté
# application que la source est une vidéo, pas un article.
YOUTUBE_CHANNELS = [
    {"name": "RTS — Radio Télévision Sénégalaise (YouTube)", "channel_id": "UC3Pwur55-OPFYDN_xg6JR_w"},
    {"name": "TFM — Télé Futurs Médias (YouTube)", "channel_id": "UC5NQ49FVRIAuWE1el6L2gkg"},
]

# Mots-clés (recherchés en minuscules) : un article est retenu si son titre
# OU son résumé contient au moins un de ces mots/expressions.
KEYWORDS = [
    "accident de la circulation", "accident de la route", "accident mortel",
    "accident de moto", "accident de bus", "accident de car",
    "carambolage", "collision", "renversé", "renversée", "percuté",
    "percutée", "accrochage mortel", "tué sur la route", "tués sur la route",
    "chavir", "car rapide",
]

OUTPUT_PATH = "news-alerts.json"
MAX_ITEMS = 25
MAX_AGE_DAYS = 14
REQUEST_TIMEOUT = 20
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; CaarangueYoonBot/1.0; +https://github.com)"}


def matches_keywords(text):
    text_low = text.lower()
    return any(kw in text_low for kw in KEYWORDS)


def clean_text(raw):
    if not raw:
        return ""
    no_tags = re.sub(r"<[^>]+>", " ", raw)
    return unescape(re.sub(r"\s+", " ", no_tags)).strip()


def local_tag(elem):
    """Nom de balise sans le préfixe de namespace XML (ex: '{...}item' -> 'item')."""
    return elem.tag.rsplit('}', 1)[-1].lower()


def child_text(item_elem, names):
    for child in item_elem:
        if local_tag(child) in names:
            return (child.text or "").strip()
    return ""


def child_link(item_elem):
    """Récupère l'URL d'un item, en gérant les deux formats rencontrés :
    RSS classique (<link>texte de l'URL</link>) et Atom/YouTube
    (<link rel="alternate" href="..."/>, élément vide avec un attribut)."""
    for child in item_elem:
        if local_tag(child) != "link":
            continue
        if child.text and child.text.strip():
            return child.text.strip()
        href = child.get("href")
        if href:
            return href.strip()
    return ""


def parse_date(raw):
    if not raw:
        return None
    raw = raw.strip()
    try:
        return parsedate_to_datetime(raw)
    except Exception:
        pass
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except Exception:
        return None


def fetch_source(source):
    items = []
    try:
        resp = requests.get(source["url"], headers=HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
    except Exception as exc:  # noqa: BLE001 — une source en panne ne doit pas interrompre les autres
        print(f"[avertissement] échec de récupération de {source['name']} : {exc}", file=sys.stderr)
        return items

    # RSS/RDF utilisent <item>, Atom (dont les flux YouTube) utilise <entry>.
    for item_elem in root.iter():
        tag = local_tag(item_elem)
        if tag not in ("item", "entry"):
            continue
        title = clean_text(child_text(item_elem, {"title"}))
        summary = clean_text(child_text(item_elem, {"description", "summary"}))
        link = child_link(item_elem)
        if not title or not link:
            continue
        if not matches_keywords(title + " " + summary):
            continue
        raw_date = child_text(item_elem, {"pubdate", "date", "published"})
        dt = parse_date(raw_date)
        if dt and dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        items.append({
            "title": title,
            "link": link,
            "source": source["name"],
            "publishedAt": dt.isoformat() if dt else None,
            "_sort_key": dt or datetime.min.replace(tzinfo=timezone.utc),
        })
    return items


def main():
    now = datetime.now(timezone.utc)
    all_sources = list(FEEDS) + [
        {"name": yt["name"], "url": f"https://www.youtube.com/feeds/videos.xml?channel_id={yt['channel_id']}"}
        for yt in YOUTUBE_CHANNELS
    ]
    all_items = []
    for source in all_sources:
        all_items.extend(fetch_source(source))

    seen_links = set()
    deduped = []
    for item in sorted(all_items, key=lambda it: it["_sort_key"], reverse=True):
        if item["link"] in seen_links:
            continue
        seen_links.add(item["link"])
        age_days = (now - item["_sort_key"]).days
        if age_days > MAX_AGE_DAYS:
            continue
        item.pop("_sort_key")
        deduped.append(item)
        if len(deduped) >= MAX_ITEMS:
            break

    output = {
        "updatedAt": now.isoformat(),
        "sources": [s["name"] for s in all_sources],
        "items": deduped,
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"{len(deduped)} article(s) retenu(s) sur {len(all_items)} candidat(s) toutes sources confondues.")


if __name__ == "__main__":
    main()
