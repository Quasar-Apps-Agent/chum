#!/usr/bin/env python3
"""Unit 4.0 (CLOUD-OK) — verify the Phase 4 mechanic enumeration.

Text units are verified by assert, not by eye (plan rule 4b, the 0.8b-spec
precedent). This script proves the enumeration is COMPLETE against its
sources and CONSISTENT between the tracker and the notes:

  1. PROGRESS.md Phase 4 boxes 4.1..4.N are contiguous, and 4.0 is ticked
     with its [CLOUD-OK] tag preserved.
  2. ue/PORT-NOTES-MECHANICS.md has exactly one "### 4.N" section per box,
     same ids, same order.
  3. Every QA line QA-01..QA-61 (restoration-qa-regression.md) is claimed
     by at least one section.
  4. Every invariant I01..I31 (restoration-invariant-suite.md) is claimed.
  5. Every achievement A01..A28 (restoration-achievements-design.md) is
     claimed.
  6. Every scripts/*.gd in the reference implementation is placed in the
     notes' script index (owned by a box, or explicitly excluded with a
     reason).
  7. Every constant the notes quote as NAME=VALUE matches Timings.csv
     (the arithmetic tripwire).
  8. Every docs/ path the notes cite exists.
  9. Every THE-LAWS law 1..11 is cited at least once.

Run from anywhere:  python3 tools/verify_mechanics.py
Exit 0 and print VERIFY-OK, or fail loudly on the first miss.
"""
import csv
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
PROGRESS = os.path.join(ROOT, "PROGRESS.md")
NOTES = os.path.join(ROOT, "ue", "PORT-NOTES-MECHANICS.md")
QA_DOC = os.path.join(ROOT, "docs", "production", "restoration-qa-regression.md")
INV_DOC = os.path.join(ROOT, "docs", "production", "restoration-invariant-suite.md")
ACH_DOC = os.path.join(ROOT, "docs", "production", "restoration-achievements-design.md")
TIMINGS = os.path.join(ROOT, "ue", "Restoration", "Data", "Timings.csv")
SCRIPTS = os.path.join(ROOT, "scripts")


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


progress = read(PROGRESS)
notes = read(NOTES)

# ---- 1. tracker boxes -------------------------------------------------------
m = re.search(r"## PHASE 4 — Puzzles & Functionality\n(.*?)\n## PHASE 5", progress, re.S)
assert m, "Phase 4 section anchor not found in PROGRESS.md"
phase4 = m.group(1)
assert re.search(r"^- \[x\] 4\.0 \[CLOUD-OK\] ", phase4, re.M), "4.0 must be ticked with its [CLOUD-OK] tag preserved"
box_ids = [int(x) for x in re.findall(r"^- \[[ x]\] 4\.(\d+) ", phase4, re.M)]
assert box_ids[0] == 0, "first box must be 4.0"
numbered = box_ids[1:]
assert numbered == list(range(1, len(numbered) + 1)), "Phase 4 boxes must be contiguous 4.1..4.N: %r" % numbered
N = len(numbered)
assert N >= 40, "expected a real enumeration, got %d boxes" % N
for legacy in ("4.WEB", "4.SAVE", "4.ENCOUNTERS", "4.FINALE", "4.QA51", "4.VERB", "4.FINAL"):
    assert ("- [ ] %s" % legacy) in phase4, "legacy audit box %s must survive (never delete history)" % legacy

# ---- 2. notes sections -----------------------------------------------------
sec_ids = [int(x) for x in re.findall(r"^### 4\.(\d+) ", notes, re.M)]
assert sec_ids == list(range(1, N + 1)), "notes sections %r != tracker boxes 1..%d" % (sec_ids, N)
# each tracker box title word-prefix must appear in its notes heading (same name)
for bid, title in re.findall(r"^- \[[ x]\] 4\.(\d+) ([^\n(:—]+)", phase4, re.M):
    if bid == "0":
        continue
    head = re.search(r"^### 4\.%s ([^\n]+)" % bid, notes, re.M).group(1)
    key = title.strip().split(" ")[0].strip(",.:")
    assert key.lower() in head.lower(), "box 4.%s title '%s' not echoed by notes heading '%s'" % (bid, title.strip(), head)

# ---- 3. QA coverage ---------------------------------------------------------
qa_defined = set(int(x) for x in re.findall(r"^QA-(\d\d) ", read(QA_DOC), re.M))
assert qa_defined == set(range(1, 62)), "QA doc defines %r" % sorted(qa_defined)
qa_cited = set()
for a, b in re.findall(r"QA-(\d\d)(?:\.\.(?:QA-)?(\d\d))?", notes):
    a = int(a)
    b = int(b) if b else a
    qa_cited.update(range(a, b + 1))
missing = qa_defined - qa_cited
assert not missing, "QA lines never claimed by any box: %s" % sorted(missing)

# ---- 4. invariant coverage --------------------------------------------------
inv_defined = set(int(x) for x in re.findall(r"^I(\d\d) ", read(INV_DOC), re.M))
assert inv_defined == set(range(1, 32)), "invariant doc defines %r" % sorted(inv_defined)
inv_cited = set()
for a, b in re.findall(r"\bI(\d\d)(?:\.\.I?(\d\d))?\b", notes):
    a = int(a)
    b = int(b) if b else a
    inv_cited.update(range(a, b + 1))
missing = inv_defined - inv_cited
assert not missing, "invariants never claimed by any box: %s" % sorted(missing)

# ---- 5. achievement coverage ------------------------------------------------
# A27 and A28 share one addendum line, so match anywhere, not just at line start
ach_defined = set(int(x) for x in re.findall(r"\bA(\d\d) [A-Z']", read(ACH_DOC)))
assert ach_defined == set(range(1, 29)), "achievement doc defines %r" % sorted(ach_defined)
ach_cited = set()
for a, b in re.findall(r"\bA(\d\d)(?:\.\.A?(\d\d))?\b", notes):
    a = int(a)
    b = int(b) if b else a
    ach_cited.update(range(a, b + 1))
missing = ach_defined - ach_cited
assert not missing, "achievements never claimed by any box: %s" % sorted(missing)

# ---- 6. script index --------------------------------------------------------
scripts = sorted(f for f in os.listdir(SCRIPTS) if f.endswith(".gd"))
idx = re.search(r"## SCRIPT INDEX\n(.*?)\n## ", notes, re.S)
assert idx, "SCRIPT INDEX section missing from notes"
indexed = {}
for name, owner in re.findall(r"^\| `([a-z0-9_]+\.gd)` \| ([^|]+) \|", idx.group(1), re.M):
    assert name not in indexed, "script indexed twice: %s" % name
    indexed[name] = owner.strip()
missing = [s for s in scripts if s not in indexed]
assert not missing, "reference scripts not placed in the index: %s" % missing
ghost = [s for s in indexed if s not in scripts]
assert not ghost, "index names scripts that do not exist: %s" % ghost
for name, owner in indexed.items():
    assert re.match(r"^(4\.\d+|EXCLUDED)", owner), "index owner for %s must be a box id or EXCLUDED: %r" % (name, owner)
    for bid in re.findall(r"4\.(\d+)", owner):
        assert 1 <= int(bid) <= N, "index for %s points at unknown box 4.%s" % (name, bid)

# ---- 7. constants tripwire --------------------------------------------------
timings = {}
with open(TIMINGS, newline="") as f:
    for row in csv.DictReader(f):
        timings[row["constant"]] = float(row["value"])
quoted = re.findall(r"\b([A-Z][A-Z0-9_]{3,})=(-?\d+(?:\.\d+)?)\b", notes)
assert quoted, "notes quote no NAME=VALUE constants; the tripwire has nothing to bite"
checked = 0
for name, val in quoted:
    if name in timings:
        assert float(val) == timings[name], "notes quote %s=%s but Timings.csv says %s" % (name, val, timings[name])
        checked += 1
assert checked >= 15, "only %d Timings constants quoted; expected the mechanics to lean on them" % checked

# ---- 8. cited paths exist ---------------------------------------------------
paths = set(re.findall(r"`((?:docs|ue|scripts|scenes|tools)/[A-Za-z0-9_./-]+)`", notes))
for p in sorted(paths):
    assert os.path.exists(os.path.join(ROOT, p)), "notes cite a path that does not exist: %s" % p

# ---- 9. the laws ------------------------------------------------------------
laws_cited = set(int(x) for x in re.findall(r"\bLaw (\d+)\b", notes))
assert laws_cited == set(range(1, 12)), "THE-LAWS cited: %s (need 1..11)" % sorted(laws_cited)

print("boxes 4.1..4.%d == notes sections %d" % (N, len(sec_ids)))
print("QA lines claimed %d/61 · invariants %d/31 · achievements %d/28" % (len(qa_cited & qa_defined), len(inv_cited & inv_defined), len(ach_cited & ach_defined)))
owned = sum(1 for o in indexed.values() if o.startswith("4."))
print("scripts indexed %d/%d (%d owned by boxes, %d excluded with reason)" % (len(indexed), len(scripts), owned, len(indexed) - owned))
print("Timings constants cross-checked %d · cited paths %d · laws 11/11" % (checked, len(paths)))
print("VERIFY-OK")
