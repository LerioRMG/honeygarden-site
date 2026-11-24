#!/usr/bin/env python3
"""Archivia il vecchio sito Honey e conserva la homepage attuale."""
import os
import re
import shutil
import sys
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path

site=Path("/var/www/honeygarden-d092377")
backup=Path("/root") / ("backup-honey-pagina-unica-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
keep={"index.html","favicon.png","beyou-contact-widget.js"}
needed=[site/"index.html",site/"favicon.png",site/"beyou-contact-widget.js",site/"media/public/honey-garden-gold.png"]
if any(not p.is_file() or p.is_symlink() for p in needed):
    raise SystemExit("STOP: manca una risorsa della pagina; nessuna modifica effettuata.")
if (site/"media").is_symlink() or (site/"media/public").is_symlink():
    raise SystemExit("STOP: cartella media inattesa; nessuna modifica effettuata.")
html=(site/"index.html").read_text(encoding="utf-8")
if "Honey Garden sta diventando" not in html or "https://thisisbeyou.com/" not in html:
    raise SystemExit("STOP: homepage diversa dal previsto; nessuna modifica effettuata.")

class Refs(HTMLParser):
    def __init__(self): super().__init__(); self.urls=[]; self.video=False
    def handle_starttag(self,tag,attrs):
        if tag=="video": self.video=True
        for k,v in attrs:
            if k in ("href","src") and v and v.startswith("/") and not v.startswith("//"):
                self.urls.append(v.split("?",1)[0].split("#",1)[0])
parser=Refs();parser.feed(html)
allowed={"/","/favicon.png","/beyou-contact-widget.js","/media/public/honey-garden-gold.png"}
unknown=set(parser.urls)-allowed
if parser.video or unknown:
    raise SystemExit("STOP: la homepage richiede risorse aggiuntive; nessuna modifica effettuata: "+", ".join(sorted(unknown)))

# Il sito BEYOU usa una copia privata; non archiviare se manca.
for p in (Path("/opt/beyou-candidatura/index.php"),Path("/opt/beyou-candidatura/originale.php"),Path("/opt/beyou-candidatura/webhook")):
    if not p.is_file() or p.stat().st_size==0:
        raise SystemExit("STOP: copia indipendente della candidatura BEYOU non trovata; nessuna modifica.")
wrapper=Path("/opt/beyou-candidatura/index.php").read_text(encoding="utf-8")
backend=Path("/opt/beyou-candidatura/originale.php").read_text(encoding="utf-8")
if "/opt/beyou-candidatura/originale.php" not in wrapper or "/opt/beyou-candidatura/webhook" not in backend:
    raise SystemExit("STOP: candidatura BEYOU non indipendente; nessuna modifica.")
if os.stat(site).st_dev!=os.stat("/root").st_dev:
    raise SystemExit("STOP: /root e il sito sono su dischi diversi; nessuna modifica.")
if backup.exists():
    raise SystemExit("STOP: cartella backup già presente; nessuna modifica.")

backup.mkdir(mode=0o700)
moved=[]
new_media=False
try:
    # Gli elementi nascosti includono .well-known, necessario al certificato.
    for entry in list(site.iterdir()):
        if entry.name.startswith(".") or entry.name in keep:
            continue
        os.replace(entry,backup/entry.name)
        moved.append(entry.name)
    logo=site/"media/public/honey-garden-gold.png"
    logo.parent.mkdir(parents=True,exist_ok=False)
    new_media=True
    shutil.copy2(backup/"media/public/honey-garden-gold.png",logo)
    (site/"robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://honeygarden.it/sitemap.xml\n",encoding="utf-8")
    (site/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://honeygarden.it/</loc></url></urlset>\n',encoding="utf-8")
    for p in (site/"robots.txt",site/"sitemap.xml"):
        p.chmod(0o644)
except BaseException:
    for name in ("robots.txt","sitemap.xml"):
        p=site/name
        if p.exists(): p.unlink()
    if new_media:
        shutil.rmtree(site/"media")
    for name in reversed(moved):
        os.replace(backup/name,site/name)
    raise

print("Homepage Honey mantenuta; vecchi file pubblici spostati nel backup.")
print("Sitemap aggiornata con la sola homepage.")
print("Backup:",backup)
print("Nota: le vecchie pagine Honey non sono più disponibili ai loro indirizzi.")
