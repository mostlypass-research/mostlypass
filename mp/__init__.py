"""Package init: make text I/O UTF-8 on every platform (Windows defaults to cp1252)."""
import os
import sys
import pathlib

try:  # console output never crashes on a non-ASCII character
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

if not sys.flags.utf8_mode:  # Windows without PYTHONUTF8=1: force UTF-8 for Path.read_text/write_text
    _rt, _wt = pathlib.Path.read_text, pathlib.Path.write_text

    def _read_text(self, *a, **k):
        if not a:
            k.setdefault("encoding", "utf-8")
        return _rt(self, *a, **k)

    def _write_text(self, data, *a, **k):
        if not a:
            k.setdefault("encoding", "utf-8")
        return _wt(self, data, *a, **k)

    pathlib.Path.read_text = _read_text
    pathlib.Path.write_text = _write_text
