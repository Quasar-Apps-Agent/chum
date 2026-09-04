#!/usr/bin/env python3
"""Port of scripts/invariant_parser.gd — the harness test step
(UE5-MIGRATION-MAP: "the parser as a test step reading the identical log
files"). Reads a decision log and emits the INVARIANTS scorecard with the
SAME rules the Godot soak uses. In UE every telemetry line lands in one
decision_log.txt, so the coverage / liveness / premiere sections all read
it. Exit 0 iff nothing FAILs.

Sections:
  I01/I02/I22  coverage   (_coverage, verbatim rules)
  I07          liveness   (_liveness: any VIOLATION line fails; N/A if none)
  I06          premiere   (_premiere: INCIDENT/RESOLVED t= rules; N/A until
                           the finale/premiere system is ported)
  UE-R1        retake     (UE-added, clearly labelled: a full sheet — 4
                           STRIKEs — must be followed by RUN ENDED, i.e. the
                           run fails FORWARD and never soft-locks)

Usage: python3 tools/invariant_parser.py <decision_log.txt> [--bot fail]
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


def liveness(lines):
    ll = [l for l in lines if "LIVENESS" in l or "VIOLATION" in l]
    if not ll:
        return "N/A (cascade did not run)", True
    for l in ll:
        if "VIOLATION" in l:
            return "FAIL (violation logged)", False
    return "PASS (%d checks)" % len(ll), True


def premiere(lines, bot):
    pl = [l for l in lines if l.startswith("INCIDENT") or l.startswith("RESOLVED")]
    if not pl:
        if bot == "fail":
            return "FAIL (fail bot produced no premiere log)", False
        return "N/A (premiere not yet ported)", True
    incidents = slow_fix = auto = 0
    for l in pl:
        if l.startswith("INCIDENT"):
            incidents += 1
        elif l.startswith("RESOLVED"):
            if "club auto-fix" in l:
                auto += 1
            ti = l.find("t=")
            if ti != -1:
                try:
                    if float(l[ti + 2:].split()[0]) > 41.0:
                        slow_fix += 1
                except ValueError:
                    pass
    if slow_fix == 0 and incidents > 0:
        v, ok = "PASS", True
    elif slow_fix > 0:
        v, ok = "FAIL (slow fixes x%d)" % slow_fix, False
    else:
        v, ok = "WEAK (no incidents rolled)", True
    return "%s (%d incidents, %d auto-fixed)" % (v, incidents, auto), ok


def retake(lines):
    strikes = sum(1 for l in lines if "STRIKE " in l)
    ended = sum(1 for l in lines if "RUN ENDED" in l)
    if strikes < 4:
        return "N/A (%d strikes, no full sheet)" % strikes, True
    if ended == 0:
        return "FAIL (%d strikes, run never ended — soft-lock)" % strikes, False
    return "PASS (%d strikes, run ended x%d)" % (strikes, ended), True


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    bot = "fail" if "--bot" in sys.argv and "fail" in sys.argv else ""
    path = args[0] if args else ""
    try:
        lines = open(path, errors="replace").read().splitlines()
    except OSError:
        print("INVARIANTS N/A (no log at %s)" % path)
        return 2
    i01, i02, i22 = coverage(lines)
    l7, ok7 = liveness(lines)
    l6, ok6 = premiere(lines, bot)
    lr, okr = retake(lines)
    print("RESTORATION · INVARIANTS SCORECARD (UE)")
    print("I01 warn-precedes-strike: %s" % ("PASS" if i01 == 0 else "FAIL x%d" % i01))
    print("I02 no-strike-thru-wall: %s" % ("PASS" if i02 == 0 else "FAIL x%d" % i02))
    print("I22 heard-noise-attribution: PASS (%d attributed)" % i22)
    print("I07 cascade-liveness: %s" % l7)
    print("I06 fail-forward-finale: %s" % l6)
    print("UE-R1 full-sheet-ends-run: %s" % lr)
    return 0 if (i01 == 0 and i02 == 0 and ok7 and ok6 and okr) else 1


if __name__ == "__main__":
    sys.exit(main())
