#!/usr/bin/env python3
"""Unit 4.0 verifier: the Phase 4 enumeration is code (plan rule 4b).

Asserts, against the repo as checked out:
  * every `4.N` box in PROGRESS.md has an entry in ue/PORT-NOTES-MECHANICS.md
    and vice versa, ids unique on both sides;
  * every PROGRESS box cites at least one of its entry's evidence ids (QA/I/A)
    when the entry has any;
  * every QA-01..QA-61, I01..I31 and A01..A28 in the canon is homed exactly
    at least once (a 4.N entry's `proves:` line, or the §0 "homed elsewhere"
    table), and every homed id actually exists in the canon docs;
  * every scripts/*.gd is either cited by an entry or listed in §0's
    not-a-mechanic list, and every cited path exists;
  * every `NAME = value` quoted in the notes with a name from Timings.csv
    matches the CSV to the digit;
  * the 4.0 box is ticked and still carries its [CLOUD-OK] tag.

Prints VERIFY-OK with counts, or raises. No engine, no network.
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "ue" / "PORT-NOTES-MECHANICS.md"
PROGRESS = ROOT / "PROGRESS.md"
TIMINGS = ROOT / "ue" / "Restoration" / "Data" / "Timings.csv"
QA_DOC = ROOT / "docs" / "production" / "restoration-qa-regression.md"
INV_DOC = ROOT / "docs" / "production" / "restoration-invariant-suite.md"
ACH_DOC = ROOT / "docs" / "production" / "restoration-achievements-design.md"
SCRIPTS = ROOT / "scripts"

ID_RE = re.compile(r"\b(QA-\d{2}|I\d{2}|A\d{2})\b")
BOX_ID_RE = re.compile(r"^- \[([ x])\] (4\.\d+[a-z]?)\b", re.M)
ENTRY_RE = re.compile(r"^### (4\.\d+[a-z]?) · (.+)$", re.M)
SCRIPT_RE = re.compile(r"scripts/([a-z_0-9]+\.gd)")
CONST_RE = re.compile(r"`([A-Z][A-Z_0-9]{2,})\s*=\s*([0-9.]+)`")


def canon_ids() -> set[str]:
    ids: set[str] = set()
    # QA and I ids open their lines; the achievements addendum defines A27 and
    # A28 mid-line, so that doc is scanned on word boundaries
    for doc, pat in ((QA_DOC, r"^QA-\d{2}\b"), (INV_DOC, r"^I\d{2}\b"), (ACH_DOC, r"\bA\d{2}\b")):
        text = doc.read_text(encoding="utf-8")
        found = set(re.findall(pat, text, re.M))
        assert found, f"no ids found in {doc}"
        ids |= found
    return ids


def parse_notes(text: str):
    # entries: id -> (title, block)
    matches = list(ENTRY_RE.finditer(text))
    assert matches, "no ### 4.N entries in notes"
    entries = {}
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[m.start():end]
        # cut at the next '## ' section header if one appears inside the block
        cut = block.find("\n## ")
        if cut != -1:
            block = block[:cut]
        eid = m.group(1)
        assert eid not in entries, f"duplicate entry {eid} in notes"
        entries[eid] = (m.group(2).strip(), block)
    # §0 homed table rows: | ids | box | why |
    sec0 = text.split("## §0")[1].split("## §1")[0]
    homed: dict[str, set[str]] = {}
    for row in re.findall(r"^\|\s*([^|]+?)\s*\|\s*([0-9]\.[0-9A-Za-z\-]+)\s*\|", sec0, re.M):
        ids = set(ID_RE.findall(row[0]))
        if not ids:
            continue
        homed.setdefault(row[1], set()).update(ids)
    assert homed, "no homed-elsewhere rows parsed from §0"
    excluded = set(SCRIPT_RE.findall("\n".join(l for l in sec0.splitlines() if l.startswith("- `scripts/"))))
    assert excluded, "no not-a-mechanic scripts parsed from §0"
    return entries, homed, excluded


def proves_of(block: str) -> set[str]:
    m = re.search(r"^- proves:\s*(.*)$", block, re.M)
    assert m, "entry lacks a proves: line:\n" + block[:120]
    line = m.group(1)
    if line.lstrip().startswith("("):
        return set()  # explicit "(none ...)" entries
    return set(ID_RE.findall(line))


def main() -> int:
    notes = NOTES.read_text(encoding="utf-8")
    progress = PROGRESS.read_text(encoding="utf-8")
    entries, homed, excluded = parse_notes(notes)

    # --- PROGRESS boxes ---------------------------------------------------
    boxes = BOX_ID_RE.findall(progress)
    box_ids = [b for _, b in boxes]
    assert len(box_ids) == len(set(box_ids)), f"duplicate 4.N box ids in PROGRESS: {box_ids}"
    box_state = dict((b, s) for s, b in boxes)
    assert box_state.get("4.0") == "x", "4.0 must be ticked"
    m40 = re.search(r"^- \[x\] 4\.0 (\[CLOUD-OK\]) ", progress, re.M)
    assert m40, "4.0 lost its [CLOUD-OK] tag (rule 4b: preserve tags)"
    numeric = set(b for b in box_ids if b != "4.0")
    assert numeric == set(entries), (
        f"box/entry mismatch\n only in PROGRESS: {sorted(numeric - set(entries))}\n"
        f" only in notes: {sorted(set(entries) - numeric)}")
    for eid in entries:
        assert box_state[eid] == " ", f"{eid} must stay unticked (only 4.0 closes this unit)"

    # each box line cites >=1 of its entry's evidence ids when it has any;
    # ids not yet in the canon (a "QA-62 to be written") are notes, not claims
    canon = canon_ids()
    box_text = {}
    for m in re.finditer(r"^- \[[ x]\] (4\.\d+[a-z]?)\b(.*?)(?=^- \[|\Z)", progress, re.M | re.S):
        box_text[m.group(1)] = m.group(2)
    for eid, (_, block) in entries.items():
        pv = proves_of(block)
        cited = set(ID_RE.findall(box_text[eid])) & canon
        if pv:
            assert cited & pv, f"{eid}: PROGRESS box cites none of its evidence {sorted(pv)}"
        assert cited <= pv, f"{eid}: box cites canon ids its entry does not prove: {sorted(cited - pv)}"

    # --- coverage of the canon evidence ----------------------------------
    claimed: dict[str, set[str]] = {}
    for eid, (_, block) in entries.items():
        for i in proves_of(block):
            claimed.setdefault(i, set()).add(eid)
    for home, ids in homed.items():
        for i in ids:
            claimed.setdefault(i, set()).add(home)
    unknown = set(claimed) - canon
    assert not unknown, f"ids homed that do not exist in the canon docs: {sorted(unknown)}"
    unhomed = canon - set(claimed)
    assert not unhomed, f"canon ids with no home box: {sorted(unhomed)}"
    # homed-elsewhere boxes must exist somewhere in PROGRESS
    all_progress_ids = set(re.findall(r"^- \[[ x]\] (\d+\.[0-9A-Za-z\-]+)", progress, re.M))
    for home in homed:
        assert home in all_progress_ids, f"§0 homes ids in a box that is not in PROGRESS: {home}"

    # --- scripts ---------------------------------------------------------
    all_scripts = set(p.name for p in SCRIPTS.glob("*.gd"))
    cited_scripts: set[str] = set()
    for eid, (_, block) in entries.items():
        for s in SCRIPT_RE.findall(block):
            assert (SCRIPTS / s).exists(), f"{eid} cites a script that does not exist: {s}"
            cited_scripts.add(s)
    for s in excluded:
        assert (SCRIPTS / s).exists(), f"§0 excludes a script that does not exist: {s}"
    missing = all_scripts - cited_scripts - excluded
    assert not missing, f"scripts with no home: {sorted(missing)}"

    # --- constants -------------------------------------------------------
    timings: dict[str, list[str]] = {}
    with TIMINGS.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            timings.setdefault(row["constant"], []).append(row["value"])
    checked = 0
    for name, val in CONST_RE.findall(notes):
        if name not in timings:
            continue
        vals = timings[name]
        assert len(vals) == 1, f"{name} is ambiguous in Timings.csv ({vals}); do not quote it by name"
        assert float(val) == float(vals[0]), f"{name}: notes say {val}, Timings.csv says {vals[0]}"
        checked += 1
    assert checked >= 10, f"only {checked} constants cross-checked; expected the quoted set"

    n_port = sum("status: PORT" in b for _, b in entries.values())
    n_impl = sum("status: IMPLEMENT" in b for _, b in entries.values())
    n_rule = sum("status: RULING" in b for _, b in entries.values())
    print(
        "VERIFY-OK  boxes=%d (PORT %d, IMPLEMENT-only %d, RULING %d)  "
        "canon ids homed=%d/%d (QA %d, I %d, A %d)  scripts homed=%d/%d (%d cited, %d not-mechanics)  "
        "constants checked=%d"
        % (
            len(entries), n_port, n_impl, n_rule,
            len(claimed), len(canon),
            sum(i.startswith("QA-") for i in canon), sum(i.startswith("I") for i in canon), sum(i.startswith("A") for i in canon),
            len(cited_scripts | excluded), len(all_scripts), len(cited_scripts), len(excluded),
            checked,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
