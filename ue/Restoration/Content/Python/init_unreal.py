"""Auto-run at editor startup (UE convention). Acts ONLY when the driver
sets UE_AUTOCAPTURE=1 — otherwise a silent no-op, so commandlets and
interactive sessions are unaffected. Exists because -ExecCmds="py <path>"
cannot survive a repo path containing spaces (the 10-CPU-hour zombie of
2026-09-03 taught this)."""
import os

if os.environ.get("UE_AUTOCAPTURE") == "1":
    import importlib.util
    _p = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "..", "..", "..", "pyscripts", "stage_and_capture.py")
    _p = os.path.normpath(_p)
    spec = importlib.util.spec_from_file_location("stage_and_capture", _p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
