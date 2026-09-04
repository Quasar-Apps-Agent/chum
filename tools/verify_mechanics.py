#!/usr/bin/env python3
"""Unit 4.0 — assert the mechanics enumeration is complete and consistent.

Verification for a text unit is an assert script, not an eye (the 0.8b-spec
precedent). This proves, against the repo as it stands:

  * every scripts/*.gd is claimed by exactly one row of the script table in
    ue/PORT-NOTES-MECHANICS.md, and every box it names exists;
  * every QA-nn in docs/production/restoration-qa-regression.md and every
    Inn in docs/production/restoration-invariant-suite.md is assigned;
  * every (file, constant) row of ue/Restoration/Data/Timings.csv is homed;
  * every QA / invariant / achievement id the notes mention exists in its
    source document, and every *.gd the notes mention exists on disk;
  * every 4.x / 4.Rx box heading in the notes has a 4.x / 4.Rx box in
    PROGRESS.md, and vice versa; the legacy Phase 4 boxes survive;
  * PROGRESS.md's 4.0 line is ticked and still carries its [CLOUD-OK] tag
    (plan rule 4b: tracker edits are code).

Deterministic, read-only, no Godot needed. Exit 0 and print VERIFY-OK, or
raise the first AssertionError with the offending ids.
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "ue" / "PORT-NOTES-MECHANICS.md"
PROGRESS = ROOT / "PROGRESS.md"
QA_DOC = ROOT / "docs" / "production" / "restoration-qa-regression.md"
INV_DOC = ROOT / "docs" / "production" / "restoration-invariant-suite.md"
ACH_DOC = ROOT / "docs" / "production" / "restoration-achievements-design.md"
TIMINGS = ROOT / "ue" / "Restoration" / "Data" / "Timings.csv"
SCRIPTS = ROOT / "scripts"

# owners that are not Phase 4 boxes: Phase 0/1/5 boxes checked against
# PROGRESS.md, plus three placeholders that name a lane rather than a box
PLACEHOLDER_OWNERS = {"3.x", "DEV", "ART"}
LEGACY_BOXES = {"4.WEB", "4.SAVE", "4.ENCOUNTERS", "4.FINALE", "4.QA51",
                "4.VERB", "4.FINAL"}

BOX_HEADING = re.compile(r"^#### (4\.R?\d+) ", re.M)
BOX_LINE = re.compile(r"^- \[([ x])\] (\S+) ", re.M)
TABLE_ROW = re.compile(r"^\| `?([^|`]+?)`? \| ([^|]+) \|$", re.M)


def section(text: str, heading: str) -> str:
    """Return the body of a '### heading' up to the next '### ' or '## '."""
    start = text.index(heading)
    rest = text[start + len(heading):]
    m = re.search(r"^##+ ", rest, re.M)
    return rest[: m.start()] if m else rest


def split_boxes(cell: str) -> list[str]:
    return [b.strip() for b in cell.split(",") if b.strip()]


def main() -> int:
    notes = NOTES.read_text(encoding="utf-8")
    progress = PROGRESS.read_text(encoding="utf-8")

    # --- the boxes the notes define -------------------------------------
    note_boxes = BOX_HEADING.findall(notes)
    assert len(note_boxes) == len(set(note_boxes)), "duplicate box heading"
    built = [b for b in note_boxes if not b.startswith("4.R")]
    rulings = [b for b in note_boxes if b.startswith("4.R")]
    assert built and rulings, "notes must define built boxes and RULING boxes"

    # --- the boxes PROGRESS.md carries ----------------------------------
    phase4 = progress[progress.index("## PHASE 4"): progress.index("## PHASE 5")]
    prog_boxes = {}
    for tick, bid in BOX_LINE.findall(phase4):
        assert bid not in prog_boxes, f"duplicate PROGRESS box {bid}"
        prog_boxes[bid] = tick
    assert prog_boxes.get("4.0") == "x", "4.0 must be ticked"
    line_40 = next(l for l in phase4.splitlines() if l.startswith("- [x] 4.0 "))
    assert "[CLOUD-OK]" in line_40, "4.0 lost its [CLOUD-OK] tag (rule 4b)"
    assert LEGACY_BOXES <= set(prog_boxes), (
        "legacy Phase 4 boxes deleted: " + str(LEGACY_BOXES - set(prog_boxes)))
    numbered = {b for b in prog_boxes if re.fullmatch(r"4\.R?\d+", b) and b != "4.0"}
    assert numbered == set(note_boxes), (
        f"PROGRESS/notes box mismatch: only in PROGRESS {sorted(numbered - set(note_boxes))},"
        f" only in notes {sorted(set(note_boxes) - numbered)}")
    for b in numbered:
        assert prog_boxes[b] == " ", f"{b} must start unticked"

    # every non-Phase-4 owner named anywhere in the coverage tables must be a
    # real box somewhere in PROGRESS.md (any phase), unless a placeholder
    all_prog_boxes = {bid for _, bid in BOX_LINE.findall(progress)}

    def check_owner(owner: str, where: str) -> None:
        if owner in PLACEHOLDER_OWNERS or owner in note_boxes or owner in LEGACY_BOXES:
            return
        assert owner in all_prog_boxes, f"{where}: owner {owner!r} is not a PROGRESS.md box"

    # --- 4.1 every script claimed exactly once ---------------------------
    script_rows = TABLE_ROW.findall(section(notes, "### 4.1 Every script, claimed"))
    claimed = {}
    for name, boxes in script_rows:
        if name == "Script":
            continue
        assert name not in claimed, f"script listed twice: {name}"
        claimed[name] = split_boxes(boxes)
        assert claimed[name], f"{name} claims no box"
        for b in claimed[name]:
            check_owner(b, f"script table {name}")
    on_disk = sorted(p.name for p in SCRIPTS.glob("*.gd"))
    assert set(on_disk) == set(claimed), (
        f"unclaimed scripts {sorted(set(on_disk) - set(claimed))};"
        f" phantom rows {sorted(set(claimed) - set(on_disk))}")

    # --- 4.2 every QA line assigned -------------------------------------
    qa_ids = sorted(set(re.findall(r"^(QA-\d\d)\b", QA_DOC.read_text(encoding="utf-8"), re.M)))
    qa_rows = {n: split_boxes(b) for n, b in
               TABLE_ROW.findall(section(notes, "### 4.2 Every QA line, assigned")) if n != "QA"}
    assert set(qa_ids) == set(qa_rows), (
        f"QA unassigned {sorted(set(qa_ids) - set(qa_rows))};"
        f" unknown {sorted(set(qa_rows) - set(qa_ids))}")
    for q, boxes in qa_rows.items():
        for b in boxes:
            check_owner(b, f"QA table {q}")

    # --- 4.3 every invariant assigned -----------------------------------
    inv_ids = sorted(set(re.findall(r"^(I\d\d)\b", INV_DOC.read_text(encoding="utf-8"), re.M)))
    inv_rows = {n: split_boxes(b) for n, b in
                TABLE_ROW.findall(section(notes, "### 4.3 Every invariant, assigned")) if n != "Invariant"}
    assert set(inv_ids) == set(inv_rows), (
        f"invariants unassigned {sorted(set(inv_ids) - set(inv_rows))};"
        f" unknown {sorted(set(inv_rows) - set(inv_ids))}")
    for i, boxes in inv_rows.items():
        for b in boxes:
            check_owner(b, f"invariant table {i}")

    # --- 4.4 every Timings.csv constant homed ----------------------------
    with TIMINGS.open(encoding="utf-8") as f:
        timings = {f"{r['file']} {r['constant']}" for r in csv.DictReader(f)}
    timing_row = re.compile(r"^\| `([a-z_]+\.gd)` ([A-Z_]+) \| ([^|]+) \|$", re.M)
    homed = {f"{f} {c}": b.strip() for f, c, b in
             timing_row.findall(section(notes, "### 4.4 Every Timings.csv constant, homed"))}
    assert timings == set(homed), (
        f"constants unhomed {sorted(timings - set(homed))}; phantom {sorted(set(homed) - timings)}")
    for c, b in homed.items():
        check_owner(b, f"timings table {c}")

    # --- every id the notes mention exists at its source ------------------
    ach_ids = set(re.findall(r"\bA\d\d\b", ACH_DOC.read_text(encoding="utf-8")))
    for qid in set(re.findall(r"\bQA-\d\d\b", notes)):
        assert qid in qa_ids, f"notes cite unknown {qid}"
    for iid in set(re.findall(r"\bI\d\d\b", notes)):
        assert iid in inv_ids, f"notes cite unknown invariant {iid}"
    for aid in set(re.findall(r"\bA\d\d\b", notes)):
        assert aid in ach_ids, f"notes cite unknown achievement {aid}"
    for gd in set(re.findall(r"\b([a-z_0-9]+\.gd)\b", notes)):
        assert (SCRIPTS / gd).exists(), f"notes cite missing script {gd}"

    print(f"scripts {len(on_disk)}/{len(on_disk)} claimed · QA {len(qa_ids)} assigned · "
          f"invariants {len(inv_ids)} assigned · constants {len(timings)} homed · "
          f"boxes {len(built)} built + {len(rulings)} rulings, matched to PROGRESS.md")
    print("VERIFY-OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
