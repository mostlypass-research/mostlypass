"""Caption-driven vertical Short (1080x1920) with ffmpeg: chart + captions, no voice, no music.
Optional. If ffmpeg is not installed (normal on Windows), the Short is skipped with a message; nothing else is affected."""
from __future__ import annotations
import os
import shutil
import subprocess
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H, SEC = 1080, 1920, 3.5
FONTS = ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/segoeuib.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"]


def _font(size):
    for p in FONTS:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    try:
        return ImageFont.load_default(size)
    except TypeError:
        return ImageFont.load_default()


def _frame(chart: Path, caption: str, brand: str, out: Path, test: bool):
    img = Image.new("RGB", (W, H), "#0f172a")
    c = Image.open(chart).convert("RGB")
    c.thumbnail((W - 80, 1000))
    img.paste(c, (40, 560))
    d = ImageDraw.Draw(img)
    d.text((60, 120), brand, font=_font(44), fill="#93c5fd")
    y = 220
    for line in textwrap.wrap(caption, 26):
        d.text((60, y), line, font=_font(64), fill="white")
        y += 78
    d.text((60, H - 160), "Paper research. Not betting advice. 21+", font=_font(34), fill="#94a3b8")
    if test:
        d.text((60, H - 260), "TEST DATA - NOT FOR PUBLICATION", font=_font(48), fill="#f87171")
    img.save(out)


def build_short(chart_png, captions, brand, out_mp4: Path, workdir: Path, test: bool = False):
    ff = shutil.which("ffmpeg")
    if not ff:
        print("[video] ffmpeg not installed: Short skipped (optional; GitHub Actions renders it).")
        return None
    if not chart_png or not Path(chart_png).exists():
        return None
    workdir.mkdir(parents=True, exist_ok=True)
    for i, cap in enumerate(captions):
        _frame(Path(chart_png), cap, brand, workdir / f"f{i:03d}.png", test)
    try:
        subprocess.run([ff, "-y", "-loglevel", "error", "-framerate", f"1/{SEC}", "-i", str(workdir / "f%03d.png"),
                        "-c:v", "libx264", "-r", "30", "-pix_fmt", "yuv420p", str(out_mp4)], check=True, timeout=300)
        shutil.rmtree(workdir, ignore_errors=True)
        return out_mp4
    except Exception as e:
        print(f"[video] ffmpeg failed (Short skipped): {e}")
        return None
