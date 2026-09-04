#!/usr/bin/env python3
"""Unit 4.0 — assert-verify ue/PORT-NOTES-MECHANICS.md against the source.

Text units verify by assertion, not by eye (rule 4b: tracker edits are
code). This script fails loudly if the enumeration and the repo disagree:

  1. every `x.gd` named in a §2 row exists in scripts/
  2. the set of scripts claimed (§2 rows ∪ §5 census) == every scripts/*.gd
  3. every QA-nn in docs/production/restoration-qa-regression.md has a home
     in §3 (and §3 names no QA line that does not exist)
  4. every Inn in docs/production/restoration-invariant-suite.md has a home
     in §4 (and vice versa)
  5. every Phase 4 box in PROGRESS.md (4.N / 4.NAME) is a §2 row or one of
     the pre-existing named boxes, and every §2 row is a PROGRESS box
  6. every box a §3/§4 home names exists in PROGRESS.md

Prints VERIFY-OK with counts. Run from anywhere: python3 tools/verify_mechanics.py
"""
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


notes = read("ue/PORT-NOTES-MECHANICS.md")
progress = read("PROGRESS.md")
qa_doc = read("docs/production/restoration-qa-regression.md")
inv_doc = read("docs/production/restoration-invariant-suite.md")

fails = []


def check(cond, msg):
    if not cond:
        fails.append(msg)


def section(title_prefix):
    """Return the text of the '## N · TITLE' section starting with title_prefix."""
    m = re.search(r"^## %s.*?$" % re.escape(title_prefix), notes, re.M)
    check(m is not None, "section missing: %s" % title_prefix)
    if m is None:
        return ""
    rest = notes[m.end():]
    n = re.search(r"^## ", rest, re.M)
    return rest[: n.start()] if n else rest


def table_rows(text):
    """Yield lists of cells for every markdown table body row in text."""
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells or set(cells[0]) <= set("-: ") or cells[0] in ("Box", "QA", "Inv", "Script"):
            continue
        yield cells


# ---------------------------------------------------------------- §2 rows
enum = section("2 · THE ENUMERATION")
rows = {}
for cells in table_rows(enum):
    box = cells[0]
    check(re.fullmatch(r"4\.\d+", box) is not None, "§2 row id malformed: %r" % box)
    check(box not in rows, "§2 duplicate box %s" % box)
    rows[box] = cells
check(len(rows) >= 30, "§2 has only %d rows" % len(rows))

scripts_dir = os.path.join(ROOT, "scripts")
all_scripts = sorted(f for f in os.listdir(scripts_dir) if f.endswith(".gd"))
check(len(all_scripts) == 73, "expected 73 reference scripts, found %d" % len(all_scripts))

claimed = {}
for box, cells in rows.items():
    for s in re.findall(r"`([a-z_0-9]+\.gd)`", cells[2] if len(cells) > 2 else ""):
        check(s in all_scripts, "%s names a script that does not exist: %s" % (box, s))
        claimed.setdefault(s, set()).add(box)
    # QA and Inv columns must be well formed
    qa_cell = cells[3] if len(cells) > 3 else ""
    inv_cell = cells[4] if len(cells) > 4 else ""
    check(qa_cell == "—" or re.fullmatch(r"(QA-\d\d)(,\s*QA-\d\d)*", qa_cell) is not None,
          "%s QA cell malformed: %r" % (box, qa_cell))
    check(inv_cell == "—" or re.fullmatch(r"(I\d\d)(,\s*I\d\d)*", inv_cell) is not None,
          "%s Inv cell malformed: %r" % (box, inv_cell))
    canon_only = "CANON-ONLY" in cells[1]
    has_scripts = cells[2].strip() != "—"
    check(canon_only != has_scripts,
          "%s: CANON-ONLY rows have no scripts and code rows have scripts (canon_only=%s, scripts=%s)"
          % (box, canon_only, has_scripts))

# ---------------------------------------------------------------- §5 census
census = section("5 · SCRIPT CENSUS")
census_scripts = {}
for cells in table_rows(census):
    m = re.fullmatch(r"`([a-z_0-9]+\.gd)`", cells[0])
    check(m is not None, "§5 row malformed: %r" % cells[0])
    if m:
        check(m.group(1) in all_scripts, "§5 names a script that does not exist: %s" % m.group(1))
        census_scripts[m.group(1)] = cells[1]

union = set(claimed) | set(census_scripts)
missing = sorted(set(all_scripts) - union)
check(not missing, "reference scripts nobody claims: %s" % ", ".join(missing))
extra = sorted(union - set(all_scripts))
check(not extra, "claimed scripts that do not exist: %s" % ", ".join(extra))

# ---------------------------------------------------------------- §3 QA coverage
qa_in_doc = sorted(set(re.findall(r"^(QA-\d\d)\b", qa_doc, re.M)))
qa_sec = section("3 · QA COVERAGE")
qa_home = {}
for cells in table_rows(qa_sec):
    # the table is three (QA, Home) pairs wide
    for i in range(0, len(cells) - 1, 2):
        q, h = cells[i], cells[i + 1]
        if not q:
            continue
        check(re.fullmatch(r"QA-\d\d", q) is not None, "§3 malformed QA id %r" % q)
        check(q not in qa_home, "§3 duplicate %s" % q)
        qa_home[q] = h
check(sorted(qa_home) == qa_in_doc,
      "§3 QA set != regression script: missing %s, extra %s"
      % (sorted(set(qa_in_doc) - set(qa_home)), sorted(set(qa_home) - set(qa_in_doc))))

# every QA line a §2 row cites must be routed to that row in §3
for box, cells in rows.items():
    for q in re.findall(r"QA-\d\d", cells[3]):
        check(q in qa_home and box in qa_home[q].split(" / "),
              "%s cites %s but §3 routes %s to %r" % (box, q, q, qa_home.get(q)))

# ---------------------------------------------------------------- §4 invariants
inv_in_doc = sorted(set(re.findall(r"^(I\d\d)\b", inv_doc, re.M)))
inv_sec = section("4 · INVARIANT HOMES")
inv_home = {}
for cells in table_rows(inv_sec):
    for i in range(0, len(cells) - 1, 2):
        k, h = cells[i], cells[i + 1]
        if not k:
            continue
        check(re.fullmatch(r"I\d\d", k) is not None, "§4 malformed invariant id %r" % k)
        check(k not in inv_home, "§4 duplicate %s" % k)
        inv_home[k] = h
check(sorted(inv_home) == inv_in_doc,
      "§4 invariant set != suite: missing %s, extra %s"
      % (sorted(set(inv_in_doc) - set(inv_home)), sorted(set(inv_home) - set(inv_in_doc))))
for box, cells in rows.items():
    for k in re.findall(r"I\d\d", cells[4]):
        check(k in inv_home and box in inv_home[k].split(" / "),
              "%s cites %s but §4 routes %s to %r" % (box, k, k, inv_home.get(k)))

# ---------------------------------------------------------------- PROGRESS boxes
m = re.search(r"^## PHASE 4 .*?$(.*?)^## PHASE 5", progress, re.M | re.S)
check(m is not None, "PROGRESS.md Phase 4 section not found")
phase4 = m.group(1) if m else ""
boxes = re.findall(r"^- \[[ x]\] (4\.[A-Za-z0-9]+)\b", phase4, re.M)
check(len(boxes) == len(set(boxes)), "PROGRESS Phase 4 has duplicate box ids")
named = {"4.0", "4.WEB", "4.SAVE", "4.ENCOUNTERS", "4.FINALE", "4.QA51", "4.VERB", "4.FINAL"}
for b in boxes:
    check(b in rows or b in named, "PROGRESS box %s has no §2 row" % b)
for b in rows:
    check(b in boxes, "§2 row %s is not a PROGRESS box" % b)
check(re.search(r"^- \[x\] 4\.0 \[CLOUD-OK\]", phase4, re.M) is not None,
      "4.0 must be ticked and keep its [CLOUD-OK] tag")
# numeric rows appear in PROGRESS in the §2 order
num_boxes = [b for b in boxes if re.fullmatch(r"4\.\d+", b) and b != "4.0"]
check(num_boxes == list(rows), "PROGRESS 4.N order differs from §2 order")

# every home named in §3/§4 resolves to a real PROGRESS box (any phase)
all_boxes = set(re.findall(r"^- \[[ x]\] ([0-9]+\.[A-Za-z0-9b-]+)\b", progress, re.M))
for table_name, table in (("§3", qa_home), ("§4", inv_home)):
    for k, h in table.items():
        for part in h.split(" / "):
            part = part.strip()
            if re.fullmatch(r"3\.1–3\.20", part):
                continue
            check(part in all_boxes, "%s routes %s to %r which is not a PROGRESS box" % (table_name, k, part))

if fails:
    print("VERIFY-FAIL")
    for f in fails:
        print("  - " + f)
    sys.exit(1)

canon_only = sum(1 for c in rows.values() if "CANON-ONLY" in c[1])
print("VERIFY-OK · %d Phase 4 rows (%d canon-only) · %d/%d scripts claimed (%d in §2, %d census) · "
      "QA %d/%d homed · invariants %d/%d homed · PROGRESS boxes %d"
      % (len(rows), canon_only, len(union), len(all_scripts), len(claimed), len(census_scripts),
         len(qa_home), len(qa_in_doc), len(inv_home), len(inv_in_doc), len(boxes)))
