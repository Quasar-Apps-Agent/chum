#!/usr/bin/env python3
"""Verify ue/PORT-NOTES-STATE.md against scripts/game_state.gd (the spec).

Plan rule 4b: tracker/spec edits are code — assert, never assume. This
parses the GDScript and the 0.8a C++ header and fails loudly if the notes
omit any save key, public var, signal, or public method, or if the counts
quoted in the notes drift from the source.

Run from the repo root:  python3 tools/check_port_notes_state.py
Exit 0 = notes complete; non-zero with a list = fix the notes.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GD = (ROOT / "scripts" / "game_state.gd").read_text()
NOTES = (ROOT / "ue" / "PORT-NOTES-STATE.md").read_text()
HDR = (ROOT / "ue" / "Restoration" / "Source" / "Restoration" / "RestorationState.h").read_text()


def backticked(name: str) -> bool:
    return f"`{name}`" in NOTES or f"`{name}(" in NOTES or f"`{name} " in NOTES


# --- save keys: the _save_dict() literal ---------------------------------
m = re.search(r"func _save_dict\(\) -> Dictionary:\n(.*?)\n\t\}\)", GD, re.S)
assert m, "could not find _save_dict"
save_keys = re.findall(r'^\s*"([a-z_0-9]+)":', m.group(1), re.M)
assert len(save_keys) == len(set(save_keys)), "duplicate save key"

# --- public vars / consts / signals / funcs (top-level only) --------------
pub_vars = [v for v in re.findall(r"^var ([a-z][a-z_0-9]*)", GD, re.M)]
priv_vars = re.findall(r"^var (_[a-z_0-9]*)", GD, re.M)
consts = re.findall(r"^const ([A-Z_]+)", GD, re.M)
signals = re.findall(r"^signal ([a-z_0-9]+)", GD, re.M)
funcs = re.findall(r"^func ([a-z_0-9]+)\(", GD, re.M)

# --- load_log coverage: every save key except version must be read back --
loaded = set(re.findall(r'data\.get\("([a-z_0-9]+)"', GD))

# --- reset_new_game assignments ------------------------------------------
rm = re.search(r"func reset_new_game\(\) -> void:\n(.*?)\n\n\n", GD, re.S)
assert rm, "could not find reset_new_game"
reset_vars = set(re.findall(r"^\t([a-z_0-9]+) = ", rm.group(1), re.M))

# --- 0.8a header UPROPERTY names, Pascal -> snake ---------------------------
sg = re.search(r"class RESTORATION_API URestorationSaveGame.*?\};", HDR, re.S).group(0)
hdr_props = re.findall(r"UPROPERTY\(\)\s+[A-Za-z0-9<>_]+\s+([A-Za-z0-9]+)", sg)


def pascal_to_snake(p: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", p).lower()


hdr_snake = {pascal_to_snake(p) for p in hdr_props}
# header uses the GDScript VAR names for a few keys; map var -> save key
var_to_key = {"tbc_enabled": "tbc", "current_tape": "tape"}
hdr_keys = {var_to_key.get(s, s) for s in hdr_snake}

errors = []

for k in save_keys:
    if not backticked(k):
        errors.append(f"save key not in notes: {k}")
    if k != "version" and k not in loaded:
        errors.append(f"save key never read back by load_log: {k}")
for v in pub_vars:
    if not backticked(v):
        errors.append(f"public var not in notes: {v}")
for v in priv_vars:
    if not backticked(v):
        errors.append(f"private var not in notes: {v}")
for c in consts:
    if not backticked(c):
        errors.append(f"const not in notes: {c}")
for s in signals:
    if not backticked(s):
        errors.append(f"signal not in notes: {s}")
for f in funcs:
    if not backticked(f):
        errors.append(f"func not in notes: {f}")

# --- counts quoted in the notes must match the source ---------------------
missing_in_hdr = [k for k in save_keys if k not in hdr_keys]
survivors = [k for k in save_keys if k != "version" and k not in reset_vars
             and k not in ("ng_relic",)]
# save keys whose var name differs from the key
key_to_var = {"tbc": "tbc_enabled", "tape": "current_tape"}
survivors = [k for k in save_keys if k != "version"
             and key_to_var.get(k, k) not in reset_vars]
survivors_no_relic = [k for k in survivors if k != "ng_relic"]

expect = {
    "all 55 keys": len(save_keys) == 55,
    "all 20": len(signals) == 20,
    f"({len(missing_in_hdr)} of the 55)": True,
    f"({len(survivors_no_relic)} of the 55": True,
}
for phrase, ok in expect.items():
    if not ok:
        errors.append(f"count claim wrong: {phrase}")
    if phrase not in NOTES:
        errors.append(f"notes do not carry the computed phrase: {phrase!r}")

demo_erase = re.search(r'if DEMO:\n\s*for k in \[(.*?)\]:', GD, re.S).group(1)
demo_keys = re.findall(r'"([a-z_0-9]+)"', demo_erase)
if f"DEMO-erased set ({len(demo_keys)} keys)" not in NOTES:
    errors.append(f"DEMO erase count drifted: source has {len(demo_keys)}")
for k in demo_keys:
    if k not in save_keys:
        errors.append(f"DEMO erase key not a save key: {k}")

print(f"save keys {len(save_keys)} · vars {len(pub_vars)}+{len(priv_vars)} · "
      f"consts {len(consts)} · signals {len(signals)} · funcs {len(funcs)}")
print(f"0.8a header carries {len(hdr_keys)} of {len(save_keys)} keys; "
      f"missing: {len(missing_in_hdr)}")
print(f"reset survivors (excl. ng_relic): {len(survivors_no_relic)} → "
      f"{' '.join(survivors_no_relic)}")
print(f"DEMO-erased: {len(demo_keys)}")

if errors:
    print("\nFAIL")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print("\nPORT-NOTES-STATE OK")
