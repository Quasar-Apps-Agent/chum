#!/usr/bin/env python3
"""Unit 4.0 verification: the Phase 4 mechanic register is complete and
consistent with the tracker and the live sources. Plan rule 4b: tracker
edits are code — this script is the assert. Prints VERIFY-OK or dies.

Checks (all hard asserts):
  1. PROGRESS.md: 4.0 ticked with its [CLOUD-OK] tag preserved; the seven
     pre-existing named boxes still present verbatim (never delete history).
  2. Every unchecked numeric 4.x box in PROGRESS.md has exactly one register
     entry in ue/PORT-NOTES-MECHANICS.md and vice versa.
  3. Every register entry carries SPEC / LAWS / ACCEPTS / TEST.
  4. Every scripts/*.gd file has exactly one primary home in §C, and every
     home token resolves (a 4.x box, a Phase 0 box present in PROGRESS.md,
     a later-phase tag, or DEV-TOOL).
  5. Laws 1–11, invariants I01–I31, QA-01–QA-61, achievements A01–A28,
     every non-ui input action in project.godot, and every constant in
     Data/Timings.csv resolve to valid boxes in §B.
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROGRESS = (ROOT / "PROGRESS.md").read_text(encoding="utf-8")
REGISTER = (ROOT / "ue" / "PORT-NOTES-MECHANICS.md").read_text(encoding="utf-8")
GODOT = (ROOT / "project.godot").read_text(encoding="utf-8")
TIMINGS = ROOT / "ue" / "Restoration" / "Data" / "Timings.csv"
SCRIPTS = sorted(p.name for p in (ROOT / "scripts").glob("*.gd"))


def die(msg: str) -> None:
    print("VERIFY-FAIL: " + msg)
    sys.exit(1)


def section(text: str, start: str, end: str) -> str:
    i = text.index(start)
    j = text.index(end, i)
    return text[i:j]


# ---- 1 · tracker state -------------------------------------------------
phase4 = section(PROGRESS, "## PHASE 4", "## PHASE 5")
if not re.search(r"^- \[x\] 4\.0 \[CLOUD-OK\] ENUMERATE", phase4, re.M):
    die("4.0 is not ticked with its [CLOUD-OK] tag preserved")
NAMED = ["4.WEB", "4.SAVE", "4.ENCOUNTERS", "4.FINALE", "4.QA51", "4.VERB", "4.FINAL"]
for n in NAMED:
    if not re.search(r"^- \[ \] " + re.escape(n) + r"\b", phase4, re.M):
        die(f"pre-existing box {n} missing or altered")
if "4.WEB reaction-matrix wiring audit (every action echoes in ≥2" not in phase4:
    die("4.WEB text altered")

# ---- 2 · boxes <-> register entries ------------------------------------
tracker_ids = re.findall(r"^- \[ \] 4\.(\d+[a-z]?) ", phase4, re.M)
register_ids = re.findall(r"^### 4\.(\d+[a-z]?) · ", REGISTER, re.M)
if len(register_ids) != len(set(register_ids)):
    die("duplicate register entry ids")
if set(tracker_ids) != set(register_ids):
    die(f"tracker/register mismatch: only in tracker {sorted(set(tracker_ids)-set(register_ids))}, "
        f"only in register {sorted(set(register_ids)-set(tracker_ids))}")
if tracker_ids != register_ids:
    die("tracker and register list the 4.x boxes in different orders")

# ---- 3 · entry shape ---------------------------------------------------
entries = re.split(r"^### 4\.", REGISTER, flags=re.M)[1:]
for e in entries:
    eid = e.split(" ")[0]
    body = e.split("\n", 1)[1].split("\n### ")[0]
    for field in ("SPEC", "LAWS", "ACCEPTS", "TEST"):
        if not re.search(r"\b" + field + r"\b", body):
            die(f"4.{eid} lacks {field}")

# ---- token validator ---------------------------------------------------
phase0_ids = set(re.findall(r"^- \[[ x]\] (0\.\d+[a-z]?(?:-\d+|-spec)?)\b",
                            section(PROGRESS, "## PHASE 0", "## PHASE 1"), re.M))
LATER = {"1.x", "2.x", "3.x", "5.1", "1.8", "1.9", "1.10", "1.12", "0.9", "DEV-TOOL"}
BOX4 = {"4." + i for i in register_ids} | set(NAMED)


def valid_token(tok: str) -> bool:
    tok = re.sub(r"\s*\(.*?\)", "", tok).strip()
    return tok in BOX4 or tok in phase0_ids or tok in LATER


def check_row(label: str, cell: str) -> None:
    toks = [t.strip() for t in cell.split(",") if t.strip()]
    if not toks:
        die(f"{label}: empty box cell")
    for t in toks:
        if not valid_token(t):
            die(f"{label}: unresolvable box token {t!r}")


# ---- 4 · script coverage -----------------------------------------------
c_sec = section(REGISTER, "## C · SCRIPT COVERAGE", "## D · WHAT")
rows = re.findall(r"^\| `([a-z_0-9]+\.gd)` \| ([^|]+) \|", c_sec, re.M)
covered = [r[0] for r in rows]
if len(covered) != len(set(covered)):
    die("a script has two primary homes")
missing = sorted(set(SCRIPTS) - set(covered))
extra = sorted(set(covered) - set(SCRIPTS))
if missing or extra:
    die(f"script coverage: unowned {missing}, phantom {extra}")
for name, home in rows:
    check_row(name, home)

# ---- 5 · laws / invariants / QA / achievements / inputs / timings -------
b_sec = section(REGISTER, "## B · LAWS", "## C · SCRIPT COVERAGE")


laws = re.findall(r"^\| (Law \d+)[^|]*\| ([^|]+) \|", b_sec, re.M)
law_map = {k: v for k, v in laws}
for n in range(1, 12):
    k = f"Law {n}"
    if k not in law_map:
        die(f"{k} unowned")
    check_row(k, law_map[k])

inv = {k: v for k, v in re.findall(r"^\| (I\d\d)[^|]*\| ([^|]+) \|", b_sec, re.M)}
for n in range(1, 32):
    k = f"I{n:02d}"
    if k not in inv:
        die(f"{k} unowned")
    check_row(k, inv[k])

qa = dict(re.findall(r"\| (QA-\d\d) \| ([^|]+?) (?=\|)", b_sec))
for n in range(1, 62):
    k = f"QA-{n:02d}"
    if k not in qa:
        die(f"{k} unowned")
    check_row(k, qa[k])

ach = dict(re.findall(r"\| (A\d\d) \| ([^|]+?) (?=\|)", b_sec))
for n in range(1, 29):
    k = f"A{n:02d}"
    if k not in ach:
        die(f"{k} unowned")
    check_row(k, ach[k])

actions = [a for a in re.findall(r"^([a-z_0-9]+)=\{", GODOT, re.M) if not a.startswith("ui_")]
acts = dict(re.findall(r"\| ([a-z_0-9]+) \| ([0-9][^|]*?) (?=\|)", b_sec))
for a in actions:
    if a not in acts:
        die(f"input action {a} unowned")
    check_row(a, acts[a])

with TIMINGS.open(encoding="utf-8") as fh:
    timing_rows = list(csv.DictReader(fh))
const_names = [r["constant"] for r in timing_rows]
b6 = b_sec[b_sec.index("### B.6"):]
for r in timing_rows:
    c = r["constant"]
    label = f"{c} ({r['file']})" if const_names.count(c) > 1 else c
    m = re.search(r"\| " + re.escape(label) + r" \| ([^|]+?) (?=\|)", b6)
    if not m:
        die(f"timing constant {label} unowned")
    check_row(label, m.group(1))

print(f"boxes {len(register_ids)} · scripts {len(SCRIPTS)} · laws 11 · invariants 31 · "
      f"QA 61 · achievements 28 · actions {len(actions)} · timings {len(timing_rows)}")
print("VERIFY-OK")
