"""Auto-run at editor startup (UE convention). Runs the script named in
UE_RUN_PYSCRIPT (absolute path) when set; else the legacy UE_AUTOCAPTURE
gate; else a silent no-op. Exists because -ExecCmds="py <path>" cannot
survive a repo path containing spaces, and commandlets cannot author
levels (both learned the hard way)."""
import os


def _run(path):
    import importlib.util
    spec = importlib.util.spec_from_file_location("autorun", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)


if os.environ.get("UE_RUN_PYSCRIPT"):
    _run(os.environ["UE_RUN_PYSCRIPT"])
elif os.environ.get("UE_AUTOCAPTURE") == "1":
    _p = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "..", "..", "pyscripts", "stage_and_capture.py"))
    _run(_p)
