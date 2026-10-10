"""Build the before/after slide comparison image for the Track 03 submission.

Usage:
    python probes/make_comparison.py --before probes/before_video/before_slide1_in_discord.jpg \
        --after probes/after_video/after_slide1.png --out probes/after_video/before_after_slide1.png

--before / --after accept a PNG/JPG of the slide, or a PDF (page 1 is rendered with PyMuPDF).
A Discord image-viewer screenshot is auto-cropped to the slide (largest bright rectangle).
"""
from __future__ import annotations

import argparse
from pathlib import Path

import fitz
from PIL import Image, ImageDraw, ImageFont, ImageOps

SLIDE_W, SLIDE_H = 1280, 720


def load_slide(path: Path) -> Image.Image:
    if path.suffix.lower() == ".pdf":
        pix = fitz.open(path)[0].get_pixmap(dpi=144)
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    else:
        img = Image.open(path).convert("RGB")
        img = crop_to_slide(img)
    return ImageOps.fit(img, (SLIDE_W, SLIDE_H), Image.LANCZOS)


def crop_to_slide(img: Image.Image) -> Image.Image:
    """If the image is a Discord viewer screenshot (dark overlay around a 16:9 slide), crop
    to the slide. Works for light and dark slides by finding the largest region that
    differs from the overlay colour sampled at the corners."""
    w, h = img.size
    px = img.load()
    corner = px[2, 2]
    def diff(c): return sum(abs(a - b) for a, b in zip(c, corner)) > 40
    rows = [y for y in range(h) if sum(diff(px[x, y]) for x in range(0, w, 8)) > w / 16]
    cols = [x for x in range(w) if sum(diff(px[x, y]) for y in range(0, h, 8)) > h / 16]
    if not rows or not cols:
        return img
    box = (min(cols), min(rows), max(cols) + 1, max(rows) + 1)
    bw, bh = box[2] - box[0], box[3] - box[1]
    if bw < 0.3 * w or bh < 0.3 * h:
        return img
    return img.crop(box)


def font(size: int) -> ImageFont.FreeTypeFont:
    for name in ("segoeui.ttf", "arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--before", type=Path, required=True)
    ap.add_argument("--after", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--before-label", default="BEFORE  -  Daimon default (no skill): PyMC Labs house style")
    ap.add_argument("--after-label", default="AFTER  -  branded-slides skill: company brand, reviewed, published")
    a = ap.parse_args()

    before, after = load_slide(a.before), load_slide(a.after)
    gap, pad, label_h = 40, 40, 70
    W = pad * 2 + SLIDE_W * 2 + gap
    H = pad * 2 + label_h + SLIDE_H
    canvas = Image.new("RGB", (W, H), "#101014")
    d = ImageDraw.Draw(canvas)
    f = font(26)
    for i, (img, label) in enumerate(((before, a.before_label), (after, a.after_label))):
        x = pad + i * (SLIDE_W + gap)
        d.text((x, pad), label, fill="#EDEDF2", font=f)
        canvas.paste(img, (x, pad + label_h))
        d.rectangle((x - 2, pad + label_h - 2, x + SLIDE_W + 1, pad + label_h + SLIDE_H + 1), outline="#3A3A44", width=2)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(a.out)
    print("wrote", a.out, canvas.size)


if __name__ == "__main__":
    main()
