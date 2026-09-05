#!/usr/bin/env python3
"""Fetch CC0 scans into tools/texsrc/<Id>/ and append CREDITS lines.
Poly Haven: api.polyhaven.com/files/<id> (2k jpg: Diffuse, nor_gl, Rough, Displacement).
AmbientCG: ambientcg.com/get?file=<Id>_2K-JPG.zip (needs a User-Agent).
Idempotent: skips ids whose folder already has files. Asset policy: PLAN §2.
Usage: python3 tools/fetch_scans.py ph:wool_boucle acg:Fabric080 ...
"""
import io, json, os, sys, urllib.request, zipfile
ROOT = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(ROOT, "texsrc")
UA = {"User-Agent": "restoration-build/1.0 (CC0 asset fetch)"}

def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()

def credit(line):
    with open(os.path.join(TEX, "CREDITS.md"), "a") as f:
        f.write(line + "\n")

def polyhaven(aid):
    d = os.path.join(TEX, aid)
    have = os.listdir(d) if os.path.isdir(d) else []
    if sum(1 for n in have if any(k in n for k in ("Diffuse", "diff", "nor_gl", "Rough"))) >= 3:
        return "skip (have)"
    files = json.loads(get("https://api.polyhaven.com/files/" + aid))
    os.makedirs(d, exist_ok=True)
    got = []
    for key in ("Diffuse", "diff", "nor_gl", "Rough", "rough", "Displacement", "disp", "AO"):
        m = files.get(key)
        if not m or "2k" not in m or "jpg" not in m["2k"]:
            continue
        url = m["2k"]["jpg"]["url"]
        out = os.path.join(d, "%s_%s_2k.jpg" % (aid, key))
        open(out, "wb").write(get(url))
        got.append(key)
    credit("- %s — Poly Haven, CC0 — https://polyhaven.com/a/%s (2k jpg: %s)" % (aid, aid, ", ".join(got)))
    return "ok " + ",".join(got)

def ambientcg(aid):
    d = os.path.join(TEX, aid)
    have = os.listdir(d) if os.path.isdir(d) else []
    if sum(1 for n in have if any(k in n for k in ("_Color", "_NormalGL", "_Roughness"))) >= 3:
        return "skip (have)"
    z = zipfile.ZipFile(io.BytesIO(get("https://ambientcg.com/get?file=%s_2K-JPG.zip" % aid)))
    os.makedirs(d, exist_ok=True)
    names = [n for n in z.namelist() if n.lower().endswith(".jpg")]
    for n in names:
        open(os.path.join(d, os.path.basename(n)), "wb").write(z.read(n))
    credit("- %s — AmbientCG, CC0 — https://ambientcg.com/view?id=%s (2K JPG)" % (aid, aid))
    return "ok %d files" % len(names)

if __name__ == "__main__":
    for spec in sys.argv[1:]:
        src, aid = spec.split(":", 1)
        try:
            r = polyhaven(aid) if src == "ph" else ambientcg(aid)
        except Exception as ex:
            r = "FAILED: %s" % ex
        print("%-28s %s" % (spec, r))
