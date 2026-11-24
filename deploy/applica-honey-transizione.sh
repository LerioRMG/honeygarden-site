#!/usr/bin/env bash
set -euo pipefail
repo=/opt/hg-studio-live
page=/var/www/honeygarden-d092377/index.html
expected=f1aae568d68e0350b172dd0b32a668ac13df0abf
target=08c4460e3c5ec780605e3a1c30ac5e276867c6d8
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

test -f "$page" || { echo "STOP: homepage Honey non trovata."; exit 1; }
actual=$(git -C "$repo" hash-object "$page")
if [ "$actual" != "$expected" ]; then
  echo "STOP: la homepage Honey è diversa dalla versione verificata."
  echo "Nessuna modifica effettuata. Invia il risultato mostrato."
  echo "Hash attuale: $actual"
  exit 1
fi
git -C "$repo" show "$target:index.html" > "$tmp/index.html"
test -s "$tmp/index.html"
python3 - "$tmp/index.html" <<'PY'
from html.parser import HTMLParser
from pathlib import Path
import sys
class Check(HTMLParser):
    def __init__(self):
        super().__init__(); self.body = False; self.video = False
    def handle_starttag(self, tag, attrs):
        if tag == "body": self.body = True
        if tag == "video": self.video = True
p = Path(sys.argv[1])
s = p.read_text(encoding="utf-8")
c = Check(); c.feed(s)
if not c.body or c.video or 'https://thisisbeyou.com/' not in s:
    raise SystemExit("STOP: pagina non valida.")
PY
backup="/root/backup-honey-transizione-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$backup"
cp -a "$page" "$backup/index.html"
cp -p "$page" "$tmp/original-metadata"
cat "$tmp/index.html" > "$tmp/original-metadata"
mv -f "$tmp/original-metadata" "$page"
echo "Honey Garden aggiornato. Backup: $backup"
