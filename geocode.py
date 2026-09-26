#!/usr/bin/env python3
"""Fill in missing coordinates in places.js.

Usage:  python3 geocode.py            (updates places.js)
        python3 geocode.py --dry-run  (shows what it would do, changes nothing)

Only city lines without coordinates are looked up. Lines that already have
coordinates are never touched, so anything you typed by hand always wins.
Uses OpenStreetMap's Nominatim service (max 1 request per second).
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

PLACES_FILE = Path(__file__).with_name("places.js")
NOMINATIM = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "personal-travel-map-geocoder/1.0 (python urllib)"

# Must match the rules in index.html.
COORD_RE = re.compile(r"^(-?\d{1,2}(?:\.\d+)?)\s*,\s*(-?\d{1,3}(?:\.\d+)?)$")
BLOCK_RE = re.compile(r"(window\.PLACES\s*=\s*`)(.*)(`\s*;?\s*)$", re.S)


def has_coords(fields):
    return any("." in f and COORD_RE.match(f) for f in fields)


def lookup(query):
    url = NOMINATIM + "?" + urllib.parse.urlencode(
        {"q": query, "format": "jsonv2", "limit": 1, "accept-language": "en"})
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as resp:
        results = json.load(resp)
    return results[0] if results else None


def main():
    dry_run = "--dry-run" in sys.argv
    text = PLACES_FILE.read_text(encoding="utf-8")

    match = BLOCK_RE.search(text)
    if not match or text.count("`") != 2:
        sys.exit("places.js looks damaged: it needs exactly one opening and one closing "
                 "backtick (`), on the first and last lines. Remove any backticks from your notes.")
    if "${" in match.group(2):
        sys.exit("places.js contains '${', which breaks the file. Please remove it from your notes.")

    lines = match.group(2).split("\n")
    changed = 0
    looked_up = 0
    for i, raw in enumerate(lines):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        fields = [f.strip() for f in line.split("|")]
        name = fields[0]
        if "," not in name or has_coords(fields[1:]):
            continue  # country-only entry, or already has coordinates

        if looked_up:
            time.sleep(1.1)  # Nominatim usage policy: max 1 request per second
        looked_up += 1
        try:
            hit = lookup(name)
        except Exception as err:  # network problems, rate limiting, etc.
            print(f"  ✗ {name}: lookup failed ({err})")
            continue
        if not hit:
            print(f"  ✗ {name}: not found. Check the spelling, or add coordinates by hand.")
            continue

        coords = f"{float(hit['lat']):.4f}, {float(hit['lon']):.4f}"
        print(f"  ✓ {name}  →  {coords}\n      ({hit['display_name']})")
        lines[i] = raw.rstrip().rstrip("|").rstrip() + " | " + coords
        changed += 1

    if not looked_up:
        print("Nothing to do: every city already has coordinates.")
        return
    if changed and not dry_run:
        new_text = text[:match.start(2)] + "\n".join(lines) + text[match.end(2):]
        PLACES_FILE.write_text(new_text, encoding="utf-8")
        print(f"\nSaved {changed} new coordinate(s) to {PLACES_FILE.name}.")
    elif dry_run:
        print(f"\nDry run: {changed} place(s) would be updated. Nothing was changed.")
    print("If a place landed in the wrong spot, replace its coordinates in places.js by hand.")


if __name__ == "__main__":
    main()
