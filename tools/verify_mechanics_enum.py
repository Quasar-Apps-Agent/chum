#!/usr/bin/env python3
"""Unit 4.0 verifier — the mechanics census is text, so its verification is
an assert script, not an eye (the 0.8b-spec precedent).

Asserts, against the live repo:
  * every QA-01..QA-61 line of docs/production/restoration-qa-regression.md
    is owned in the enumeration
  * every invariant I01..I31 of restoration-invariant-suite.md is owned
  * every achievement A01..A28 of restoration-achievements-design.md is owned
  * every key of game_state.gd's _save_dict() is owned (parsed from source)
  * every (file, constant) row of ue/Restoration/Data/Timings.csv is owned
  * every scripts/*.gd file is accounted for by basename
  * every 4.x box id the enumeration declares exists in PROGRESS.md, and
    every 4.x box in PROGRESS.md is declared by the enumeration
  * PROGRESS.md's 4.0 box is ticked and still carries its [CLOUD-OK] tag
Prints VERIFY-OK on success; any failure is an AssertionError naming it.
"""
import csv
import glob
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


enum = read("docs", "production", "restoration-mechanics-enumeration.md")
progress = read("PROGRESS.md")
qa_doc = read("docs", "production", "restoration-qa-regression.md")
inv_doc = read("docs", "production", "restoration-invariant-suite.md")
ach_doc = read("docs", "production", "restoration-achievements-design.md")
gs = read("scripts", "game_state.gd")

failures = []


def check(cond, msg):
    if not cond:
        failures.append(msg)


## 1 · QA lines: every id the regression doc defines must appear in the census
qa_ids = sorted(set(re.findall(r"^(QA-\d\d)\b", qa_doc, re.M)))
check(len(qa_ids) == 61, "expected 61 QA ids in the regression doc, found %d" % len(qa_ids))
for q in qa_ids:
    check(q in enum, "QA line unowned: %s" % q)

## 2 · Invariants: every I-id defined at line start in the suite
inv_ids = sorted(set(re.findall(r"^(I\d\d)\b", inv_doc, re.M)))
check(len(inv_ids) == 31, "expected 31 invariants, found %d" % len(inv_ids))
for i in inv_ids:
    check(re.search(r"\b%s\b" % i, enum) is not None, "invariant unowned: %s" % i)

## 3 · Achievements A01..A28
ach_ids = sorted(set(re.findall(r"\b(A\d\d)\b", ach_doc)))
ach_ids = [a for a in ach_ids if 1 <= int(a[1:]) <= 28]
check(len(ach_ids) == 28, "expected 28 achievement ids, found %d" % len(ach_ids))
for a in ach_ids:
    check(re.search(r"\b%s\b" % a, enum) is not None, "achievement unowned: %s" % a)

## 4 · Save keys, parsed from _save_dict() in the source
m = re.search(r"func _save_dict\(\) -> Dictionary:\n(.*?)\n\n\nfunc ", gs, re.S)
check(m is not None, "_save_dict not found in game_state.gd")
save_keys = re.findall(r'^\s*"([a-z_0-9]+)":', m.group(1), re.M) if m else []
check(len(save_keys) == 55, "expected 55 save keys, found %d" % len(save_keys))
for k in save_keys:
    check(re.search(r"\b%s\b" % re.escape(k), enum) is not None, "save key unowned: %s" % k)

## 5 · Timings rows
with open(os.path.join(ROOT, "ue", "Restoration", "Data", "Timings.csv"), newline="") as f:
    rows = list(csv.DictReader(f))
check(len(rows) == 32, "expected 32 Timings rows, found %d" % len(rows))
for r in rows:
    check(r["file"] in enum, "Timings file unowned: %s" % r["file"])
    check(re.search(r"\b%s\b" % re.escape(r["constant"]), enum) is not None,
          "Timings constant unowned: %s.%s" % (r["file"], r["constant"]))

## 6 · Every reference script accounted for
scripts = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "scripts", "*.gd")))
check(len(scripts) >= 70, "expected the reference script set, found %d" % len(scripts))
for s in scripts:
    check(s in enum, "script unaccounted: %s" % s)

## 7 · Box ids: enumeration §8 versus PROGRESS.md Phase 4
sec8 = enum.split("## 8 · THE BOXES")[1]
declared = set(re.findall(r"\b(4\.\d+)\b", sec8))
check(len(declared) == 34, "expected 34 declared boxes, found %d" % len(declared))
ph4 = progress.split("## PHASE 4")[1].split("## PHASE 5")[0]
present = set(re.findall(r"^- \[[ x]\] (4\.\d+)\b", ph4, re.M))
present.discard("4.0")
check(declared == present, "box id mismatch: declared-not-present=%s present-not-declared=%s"
      % (sorted(declared - present), sorted(present - declared)))
for kept in ("4.WEB", "4.SAVE", "4.ENCOUNTERS", "4.FINALE", "4.QA51", "4.VERB", "4.FINAL"):
    check(("- [ ] %s" % kept) in ph4, "kept box missing from PROGRESS: %s" % kept)
    check(kept in enum, "kept box not keyed in the enumeration: %s" % kept)

## 8 · The 4.0 box itself: ticked, tag preserved
check(re.search(r"^- \[x\] 4\.0 \[CLOUD-OK\]", ph4, re.M) is not None,
      "4.0 is not ticked with its [CLOUD-OK] tag preserved")
check(ph4.count("[CLOUD-OK]") >= 2, "the CLOUD-OK lane must survive (4.0 + 4.1)")

## 9 · The findings the census promised to surface
for needle in ("M2 THE HOME SINGER is prose-only", "ENDING A · AUDIENCE ONLY is prose-only"):
    check(needle in enum, "finding missing: %s" % needle)

if failures:
    for f_ in failures:
        print("FAIL ·", f_)
    sys.exit("VERIFY-FAILED (%d)" % len(failures))
print("VERIFY-OK · QA %d · invariants %d · achievements %d · save keys %d · timings %d · scripts %d · boxes %d"
      % (len(qa_ids), len(inv_ids), len(ach_ids), len(save_keys), len(rows), len(scripts), len(declared)))
