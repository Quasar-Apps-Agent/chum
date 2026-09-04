#!/usr/bin/env python3
"""Port of scripts/invariant_parser.gd coverage logic — the harness test
step (UE5-MIGRATION-MAP: "the parser as a test step reading the identical
log files"). Reads a decision log and emits the I01/I02/I22 scorecard with
the SAME rules the Godot soak uses. Exit 0 iff all coverage invariants pass.

Usage: python3 tools/invariant_parser.py <decision_log.txt>
"""
import sys


def coverage(lines):
    warned = False
    i01_fail = i02_fail = i22 = 0
    for l in lines:
        if "WARN " in l:
            warned = True
        elif "STRIKE " in l:
            if "THRU-WALL" in l:
                i02_fail += 1
            if not warned and "savor" not in l:
                i01_fail += 1
            warned = False
        elif "toward heard noise" in l:
            i22 += 1
    return i01_fail, i02_fail, i22


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        lines = open(path, errors="replace").read().splitlines()
    except OSError:
        print("INVARIANTS N/A (no log at %s)" % path)
        return 2
    i01, i02, i22 = coverage(lines)
    print("RESTORATION · INVARIANTS SCORECARD (UE)")
    print("I01 warn-precedes-strike: %s" % ("PASS" if i01 == 0 else "FAIL x%d" % i01))
    print("I02 no-strike-thru-wall: %s" % ("PASS" if i02 == 0 else "FAIL x%d" % i02))
    print("I22 heard-noise-attribution: PASS (%d attributed)" % i22)
    return 0 if (i01 == 0 and i02 == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
