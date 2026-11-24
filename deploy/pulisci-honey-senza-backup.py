#!/usr/bin/env python3
"""Rimuove definitivamente i vecchi file pubblici del sito Honey."""
import os
import re
import shutil
from html.parser import HTMLParser
from pathlib import Path

site=Path("/var/www/honeygarden-d092377")
if not site.is_dir() or site.is_symlink() or site.resolve()!=site:
    raise SystemExit("STOP: cartella Honey non riconosciuta.")
files=("index.html","favicon.png","beyou-contact-widget.js","media/public/honey-garden-gold.png")
for name in files:
    p=site/name
    if not p.is_file() or p.is_symlink():
        raise SystemExit("STOP: risorsa mancante o collegamento inatteso: "+name)
if (site/"media").is_symlink() or (site/"media/public").is_symlink():
    raise SystemExit("STOP: cartella media non riconosciuta.")
html=(site/"index.html").read_text(encoding="utf-8")
if "Honey Garden sta diventando" not in html or "https://thisisbeyou.com/" not in html:
    raise SystemExit("STOP: homepage diversa dal previsto.")

class Check(HTMLParser):
    def __init__(self): super().__init__(); self.paths=set(); self.video=False
    def handle_starttag(self,tag,attrs):
        if tag=="video": self.video=True
        for k,v in attrs:
            if k in ("src","href") and v and v.startswith("/") and not v.startswith("//"):
                self.paths.add(v.split("?",1)[0].split("#",1)[0])
check=Check(); check.feed(html)
allowed={"/","/favicon.png","/media/public/honey-garden-gold.png","/beyou-contact-widget.js"}
if check.video or check.paths-allowed:
    raise SystemExit("STOP: risorse della homepage diverse dal previsto: "+str(sorted(check.paths-allowed)))

private=Path("/opt/beyou-candidatura")
for name in ("index.php","originale.php","webhook"):
    if not (private/name).is_file() or (private/name).stat().st_size==0:
        raise SystemExit("STOP: candidatura BEYOU non trovata; nessuna modifica.")
if str(private/"originale.php") not in (private/"index.php").read_text(encoding="utf-8"):
    raise SystemExit("STOP: candidatura BEYOU non indipendente.")
if str(private/"webhook") not in (private/"originale.php").read_text(encoding="utf-8"):
    raise SystemExit("STOP: collegamento Discord BEYOU non riconosciuto.")

keep_files=set(files)|{"robots.txt","sitemap.xml"}
keep_dirs={"media","media/public"}
remove_files=[]
remove_dirs=[]
for root,dirs,names in os.walk(site,topdown=True,followlinks=False):
    base=Path(root)
    # I file nascosti possono includere configurazioni del server e .well-known.
    dirs[:]=[d for d in dirs if not d.startswith(".")]
    for d in dirs:
        p=base/d
        if p.is_symlink():
            remove_files.append(p)
        elif os.path.ismount(p):
            raise SystemExit("STOP: cartella montata rilevata: "+str(p))
    dirs[:]=[d for d in dirs if not (base/d).is_symlink()]
    for name in names:
        if name.startswith("."):
            continue
        p=base/name
        if str(p.relative_to(site)) not in keep_files:
            remove_files.append(p)
    if base!=site and str(base.relative_to(site)) not in keep_dirs:
        remove_dirs.append(base)

# Solo backup della homepage/site Honey creati con questa procedura, non quelli di Studio o BEYOU.
backup_pattern=re.compile(r"^backup-honey-(?:home|link|rimozione-barra|barra|barra-stile|alert|footer|riga|cookie|pagina)-[0-9]{8}-[0-9]{6}\\.html$")
backup_dir_pattern=re.compile(r"^backup-honey-(?:transizione|pagina-unica)-[0-9]{8}-[0-9]{6}$")
old_backups=[]
for p in Path("/root").iterdir():
    if backup_pattern.fullmatch(p.name) and (p.is_file() or p.is_symlink()):
        old_backups.append(p)
    elif backup_dir_pattern.fullmatch(p.name) and (p.is_dir() or p.is_symlink()):
        if p.is_dir() and not p.is_symlink():
            for root,dirs,names in os.walk(p,followlinks=False):
                for d in dirs:
                    q=Path(root)/d
                    if not q.is_symlink() and os.path.ismount(q):
                        raise SystemExit("STOP: backup contenente una cartella montata: "+str(q))
        old_backups.append(p)

for p in remove_files:
    p.unlink()
for p in sorted(remove_dirs,key=lambda p:len(p.parts),reverse=True):
    try: p.rmdir()
    except OSError:
        # Le directory contenenti file nascosti o di servizio restano intatte.
        pass
(site/"robots.txt").write_text("User-agent: *\\nAllow: /\\nSitemap: https://honeygarden.it/sitemap.xml\\n",encoding="utf-8")
(site/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://honeygarden.it/</loc></url></urlset>\\n',encoding="utf-8")
(site/"robots.txt").chmod(0o644)
(site/"sitemap.xml").chmod(0o644)
for p in old_backups:
    if p.is_symlink() or p.is_file(): p.unlink()
    else: shutil.rmtree(p)
print("File pubblici obsoleti rimossi senza creare backup:",len(remove_files))
print("Backup Honey di questa procedura rimossi:",len(old_backups))
print("Sitemap: solo homepage Honey.")
print("File nascosti e configurazioni del server conservati.")
