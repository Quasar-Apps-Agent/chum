#!/usr/bin/env python3
"""RESTORATION string extractor. Scans scripts/ for player-facing literals,
writes translations/strings.csv in Godot's source-as-key format (column one
is the English source; per-locale columns start empty). Re-run any time;
existing translations in the CSV are preserved by key."""
import re, glob, csv, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'translations', 'strings.csv')
LOCALES = ['fr', 'de', 'es', 'it', 'pt_BR']

def harvest():
    keys, fmt_sites = [], 0
    seen = set()
    for f in sorted(glob.glob(os.path.join(ROOT, 'scripts', '*.gd'))):
        src = open(f, encoding='utf-8').read()
        for m in re.finditer(r'"((?:[^"\\]|\\.)*)"', src):
            lit = m.group(1)
            if len(lit) < 4 or lit.startswith(('res://', 'user://', 'uid://')):
                continue
            if not re.search(r"[A-Za-z]{3,}", lit) or (' ' not in lit and '·' not in lit):
                continue
            tail = src[m.end():m.end() + 3]
            if tail.strip().startswith('%'):
                fmt_sites += 1  # template used with %: translate the template
            if lit not in seen:
                seen.add(lit)
                keys.append(lit)
    return keys, fmt_sites

def main():
    old = {}
    if os.path.exists(OUT):
        with open(OUT, newline='', encoding='utf-8') as f:
            for row in csv.reader(f):
                if row and row[0] != 'keys':
                    old[row[0]] = row[1:]
    keys, fmt_sites = harvest()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['keys'] + LOCALES)
        for k in keys:
            w.writerow([k] + (old.get(k, [''] * len(LOCALES)) + [''] * len(LOCALES))[:len(LOCALES)])
    print(f"extracted {len(keys)} source strings; {fmt_sites} are % templates (translate the template, keep the placeholders)")

if __name__ == '__main__':
    main()
