#!/usr/bin/env python3
"""Tripwire for ue/PORT-NOTES-STATE.md against scripts/game_state.gd.

The notes are a transcription of the reference implementation (the code is
the spec). This script asserts the transcription has not drifted: every
_save_dict key, every `var`, every `signal`, and every public `func` in
game_state.gd must appear in the notes; the save-key count and SAVE_VERSION
must match. Run after any edit to either file. Exit 0 = in sync.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "scripts" / "game_state.gd"
NOTES = ROOT / "ue" / "PORT-NOTES-STATE.md"

src = SRC.read_text()
notes = NOTES.read_text()

version = int(re.search(r"^const SAVE_VERSION := (\d+)", src, re.M).group(1))
body = re.search(r"func _save_dict\(\) -> Dictionary:\n(.*?)\n\n\nfunc ", src, re.S).group(1)
save_keys = re.findall(r'^\s+"(\w+)":', body, re.M)
fields = re.findall(r"^var (\w+)", src, re.M)
signals = re.findall(r"^signal (\w+)", src, re.M)
funcs = [f for f in re.findall(r"^func (\w+)", src, re.M) if not f.startswith("_")]
loaded = set(re.findall(r'data\.get\("(\w+)"', src))

# reset_new_game coverage: which saved vars are NOT reset (carry across runs)
reset_body = re.search(r"func reset_new_game\(\) -> void:\n(.*?)\n\n\n", src, re.S).group(1)
reset_vars = set(re.findall(r"^\t(\w+) =", reset_body, re.M))
key_to_var = {"tbc": "tbc_enabled", "tape": "current_tape", "version": None}
not_reset = sorted(
    (key_to_var.get(k, k) for k in save_keys if key_to_var.get(k, k) and key_to_var.get(k, k) not in reset_vars)
)

problems = []

def must(cond, msg):
    if not cond:
        problems.append(msg)

must(f"SAVE_VERSION := {version}" in src, "source SAVE_VERSION unreadable")
must(f"v{version}" in notes, f"notes do not name v{version}")
must(f"**{len(save_keys)} keys**" in notes,
     f"notes must state **{len(save_keys)} keys** (source has {len(save_keys)})")
for k in save_keys:
    must(f"| `{k}`" in notes, f"save key `{k}` missing from the schema table")
    must(k in loaded, f"save key `{k}` written but never read back in load_log")
for v in fields:
    must(f"`{v}`" in notes, f"var `{v}` not mentioned in notes")
for s in signals:
    must(f"| `{s}`" in notes, f"signal `{s}` missing from the signal table")
for f in funcs:
    must(f"`{f}(" in notes, f"public func `{f}(` missing from the API table")
for v in not_reset:
    must(f"`{v}`" in notes.split("## 3", 1)[1] if "## 3" in notes else False,
         f"saved var `{v}` survives reset_new_game but is not listed in §3")

# §7 gap audit: the "missing keys (N of 55)" claim is computed from the C++
# SaveGame class, not typed by hand (snake_case of the UPROPERTY names).
HDR = ROOT / "ue" / "Restoration" / "Source" / "Restoration" / "RestorationState.h"
if HDR.exists():
    hdr = HDR.read_text()
    sg = re.search(r"class RESTORATION_API URestorationSaveGame.*?\};", hdr, re.S).group(0)
    props = re.findall(r"UPROPERTY\(\)\s+\S+\s+(\w+)", sg)
    snake = lambda p: re.sub(r"(?<!^)(?=[A-Z])", "_", p).lower()
    present = {snake(p) for p in props}
    alias = {"tape": "current_tape"}
    missing = [k for k in save_keys if alias.get(k, k) not in present]
    claim = f"**Missing keys ({len(missing)} of {len(save_keys)}):**"
    must(claim in notes, f"§7 must read {claim} (SaveGame has {len(props)} props)")
    sec7 = notes.split("## 7", 1)[1] if "## 7" in notes else ""
    for k in missing:
        must(k in sec7, f"§7 missing-key list lacks `{k}`")
    print(f"RestorationState.h: SaveGame props={len(props)} missing_keys={len(missing)}")

print(f"game_state.gd: SAVE_VERSION={version} save_keys={len(save_keys)} "
      f"vars={len(fields)} signals={len(signals)} public_funcs={len(funcs)}")
print("saved-but-not-reset:", ", ".join(not_reset))
if problems:
    print("\nDRIFT:")
    for p in problems:
        print("  -", p)
    sys.exit(1)
print("PORT-NOTES-STATE in sync with game_state.gd")
