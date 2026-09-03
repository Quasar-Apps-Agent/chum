"""Factory-side FBX contract gate (plan §1 export law, unit 0.2).

Round-trips an exported FBX back through Blender and verifies the scale
contract (1 Blender meter -> 100uu: FBX file units are cm, so a 1m object
must re-import at exactly 1m), the SM_/SK_ naming law, and that UCX_
collision children traveled with the mesh. Also scans the binary for the
FBX GlobalSettings UnitScaleFactor as a second, importer-independent read.

This is the pre-engine half of the scale verify; the engine-side half is
import_fbx.py's IMPORT-OK size_uu line. Both must agree.

Run headless:
  blender --background --python tools/verify_fbx.py -- \
      [path/to.fbx] [--expect-dims X,Y,Z] [--expect-ucx N]
Defaults: ue/exports/SM_UnitCube.fbx, dims 1,1,1 (m), 1 UCX child.
Prints FBX-VERIFY-OK / FBX-VERIFY-FAIL lines the driver greps; exits the
process nonzero on failure so shell drivers can `set -e` on it.
"""
import os
import struct
import sys

import bpy

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def arg(name, default=None):
    if name in argv:
        i = argv.index(name)
        return argv[i + 1] if i + 1 < len(argv) else default
    return default


positional = [a for a in argv if not a.startswith("--")
              and (argv.index(a) == 0 or not argv[argv.index(a) - 1].startswith("--"))]
fbx_path = positional[0] if positional else os.path.join(ROOT, "ue", "exports", "SM_UnitCube.fbx")
if not os.path.isabs(fbx_path):
    fbx_path = os.path.join(ROOT, fbx_path)
expect_dims = tuple(float(v) for v in (arg("--expect-dims") or "1,1,1").split(","))
expect_ucx = int(arg("--expect-ucx") or "1")
EPS = 1e-3

failures = []


def check(ok, label, detail):
    line = "%s %s %s" % ("FBX-VERIFY-OK" if ok else "FBX-VERIFY-FAIL", label, detail)
    print(line)
    if not ok:
        failures.append(label)


## ---- 1. importer-independent read: GlobalSettings UnitScaleFactor ------
## Binary FBX Properties70 entry: name string "UnitScaleFactor" followed by
## typed values; the payload double is tagged 'D'. Scan a short window after
## the name for the first 'D'-tagged double.
def scan_unit_scale(path):
    with open(path, "rb") as f:
        blob = f.read()
    idx = blob.find(b"UnitScaleFactor")
    while idx != -1:
        window = blob[idx + len(b"UnitScaleFactor"): idx + len(b"UnitScaleFactor") + 96]
        for j in range(len(window) - 9):
            if window[j:j + 1] == b"D":
                val = struct.unpack("<d", window[j + 1:j + 9])[0]
                if 0.0009 < abs(val) < 1e6:
                    return val
        idx = blob.find(b"UnitScaleFactor", idx + 1)
    return None


usf = scan_unit_scale(fbx_path)
## Blender's exporter with apply_unit_scale + FBX_SCALE_NONE writes cm-unit
## files (UnitScaleFactor 1.0) with geometry already x100 — that IS the
## 1m=100uu contract. 100.0 would mean double-scaling downstream.
check(usf is not None and abs(usf - 1.0) < EPS, "unit-scale-factor",
      "%s (want 1.0: cm-unit file, geometry pre-scaled x100)" % usf)

## ---- 2. round-trip: import and measure in meters ------------------------
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=fbx_path)

base = os.path.splitext(os.path.basename(fbx_path))[0]
check(base.startswith("SM_") or base.startswith("SK_"), "naming-law", base)

meshes = [o for o in bpy.data.objects if o.type == "MESH"]
subject = next((o for o in meshes if not o.name.startswith("UCX_")), None)
ucx = [o for o in meshes if o.name.startswith("UCX_")]

if subject is None:
    check(False, "subject-mesh", "no non-UCX mesh in %s" % base)
else:
    d = subject.dimensions
    ok = all(abs(d[i] - expect_dims[i]) < EPS for i in range(3))
    check(ok, "scale-contract",
          "%s dims_m=(%.4f,%.4f,%.4f) expect=(%.3f,%.3f,%.3f) -> %d uu"
          % (subject.name, d.x, d.y, d.z, *expect_dims, round(d.x * 100)))

check(len(ucx) == expect_ucx, "ucx-collision",
      "found=%d expect=%d %s" % (len(ucx), expect_ucx,
                                 ",".join(o.name for o in ucx) or "-"))

verdict = "FBX-VERIFY-DONE %s all_ok=%s" % (base, not failures)
print(verdict)
if failures:
    sys.exit(1)
