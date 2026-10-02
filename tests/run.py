"""Minimal runner so tests work without pytest: python tests/run.py"""
import importlib, inspect, sys, traceback, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
mods = sorted(p.stem for p in pathlib.Path(__file__).parent.glob("test_*.py"))
fails = 0; n = 0
for m in mods:
    mod = importlib.import_module(f"tests.{m}")
    for name, fn in inspect.getmembers(mod, inspect.isfunction):
        if name.startswith("test_"):
            n += 1
            try: fn(); print(f"PASS {m}.{name}")
            except Exception: fails += 1; print(f"FAIL {m}.{name}"); traceback.print_exc()
print(f"{n - fails}/{n} passed"); sys.exit(1 if fails else 0)
