"""Extract brand tokens from a PDF slide deck.

Usage:
    python extract_brand.py deck.pdf [--out brand.json] [--swatch brand_swatch.png] [--logo logo.png] [--summary]

--summary prints a short, chat-ready description of the profile (background, fonts, accent,
logo, footer) to paste into Discord. Paths written into brand.json are file names only, so
the file can be committed to a repo without leaking sandbox paths.

Writes brand.json with page size, background, palette, text colours, fonts (display/body
roles), logo crop, footer text + page-number pattern, and rule lines. Needs PyMuPDF.
Everything is derived from the file: pixel sampling for colours, text spans for fonts
and positions, drawings/images for logo and rules. No network, no guessing.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:  # pragma: no cover
    sys.exit("PyMuPDF is required: pip install pymupdf")

PAGE_NUM_PATTERNS = [
    (r"^\s*(\d+)\s*/\s*(\d+)\s*$", "n / N"),
    (r"^\s*(\d+)\s+of\s+(\d+)\s*$", "n of N"),
    (r"^\s*page\s+(\d+)\s*$", "Page n"),
    (r"^\s*(\d+)\s*$", "n"),
]


def hexc(rgb) -> str:
    r, g, b = (int(round(v * 255)) if isinstance(v, float) and v <= 1 else int(v) for v in rgb)
    return f"#{r:02X}{g:02X}{b:02X}"


def int_to_hex(c: int) -> str:
    return f"#{(c >> 16) & 255:02X}{(c >> 8) & 255:02X}{c & 255:02X}"


def quantize(h: str, step: int = 8) -> str:
    r, g, b = int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)
    q = lambda v: min(255, (v // step) * step + step // 2)
    return f"#{q(r):02X}{q(g):02X}{q(b):02X}"


def luminance(h: str) -> float:
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def sample_colors(page, dpi=36) -> Counter:
    """Pixel histogram of a low-res render; cheap and robust to vector vs raster."""
    pix = page.get_pixmap(dpi=dpi, alpha=False)
    counts = Counter()
    data, n = pix.samples, pix.n
    for i in range(0, len(data), n):
        counts[quantize(f"#{data[i]:02X}{data[i+1]:02X}{data[i+2]:02X}")] += 1
    return counts


def extract(pdf_path: Path, logo_out: Path | None) -> dict:
    doc = fitz.open(pdf_path)
    n_pages = len(doc)
    W, H = doc[0].rect.width, doc[0].rect.height

    pixel_counts = Counter()
    text_color_chars = Counter()
    font_chars = Counter()
    font_sizes = defaultdict(list)
    bottom_lines: list[list[str]] = []  # per page, text lines in bottom 10%
    top_images = Counter()  # (rounded bbox) -> pages seen
    top_drawings = Counter()
    rules = Counter()  # (y rounded, color) near bottom
    exact_fills = Counter()  # exact vector fill colours weighted by area

    for page in doc:
        pixel_counts += sample_colors(page)
        d = page.get_text("dict")
        page_bottom = []
        for block in d["blocks"]:
            if block.get("type") == 1:  # image block
                x0, y0, x1, y1 = block["bbox"]
                if y1 < 0.12 * H:
                    top_images[(round(x0), round(y0), round(x1), round(y1))] += 1
                continue
            for line in block.get("lines", []):
                text = "".join(s["text"] for s in line["spans"]).replace("\xa0", " ").strip()
                for s in line["spans"]:
                    t = s["text"].strip()
                    if not t:
                        continue
                    col = int_to_hex(s["color"])
                    text_color_chars[col] += len(t)
                    font_chars[s["font"]] += len(t)
                    font_sizes[s["font"]].append(round(s["size"], 1))
                if text and line["bbox"][1] > 0.88 * H:
                    page_bottom.append((round(line["bbox"][0]), text))
        bottom_lines.append(page_bottom)
        for dr in page.get_drawings():
            r = dr["rect"]
            fill = dr.get("fill")
            if fill:
                exact_fills[hexc(fill)] += r.width * r.height
            if r.y1 < 0.12 * H and r.width < 0.25 * W and fill:
                top_drawings[(round(r.x0), round(r.y0), round(r.x1), round(r.y1), hexc(fill))] += 1
            if r.y0 > 0.85 * H and r.height <= 2 and r.width > 0.5 * W:
                col = dr.get("color") or fill
                if col:
                    rules[(round(r.y0), hexc(col), round(r.width))] += 1

    # --- colours
    total_px = sum(pixel_counts.values())
    exact = [c for c, _ in exact_fills.most_common()] + [c for c, _ in text_color_chars.most_common()]

    def snap(h: str) -> str:
        """Replace a quantized pixel colour with the nearest exact vector/text colour if close."""
        def dist(a, b):
            return sum((int(a[i:i + 2], 16) - int(b[i:i + 2], 16)) ** 2 for i in (1, 3, 5))
        best = min(exact, key=lambda e: dist(e, h), default=None)
        return best if best and dist(best, h) <= 3 * 12 ** 2 else h

    background = snap(pixel_counts.most_common(1)[0][0])
    seen, palette = {background}, []
    for c, v in pixel_counts.most_common(14):
        c = snap(c)
        if c in seen or v / total_px < 0.002:
            continue
        seen.add(c); palette.append((c, round(v / total_px, 4)))
    palette = palette[:6]
    text_colors = [(c, v) for c, v in text_color_chars.most_common(5)]

    # --- fonts
    fonts = []
    for name, chars in font_chars.most_common():
        sizes = sorted(font_sizes[name])
        fonts.append({"name": name, "chars": chars, "median_size": sizes[len(sizes) // 2],
                      "max_size": sizes[-1], "serif": bool(re.search(r"georgia|times|garamond|cambria|serif|palatino|book", name, re.I))})
    display = max(fonts, key=lambda f: f["max_size"])["name"] if fonts else None
    body = max(fonts, key=lambda f: f["chars"])["name"] if fonts else None

    # --- footer: lines that repeat on most pages in the bottom band
    line_pages = Counter()
    for pb in bottom_lines:
        for _, t in set(pb):
            line_pages[t] += 1
    repeated = [t for t, c in line_pages.items() if c >= max(2, 0.6 * n_pages)]
    footer_text, page_fmt, page_pos = None, None, None
    for pb in bottom_lines:
        for x, t in pb:
            for pat, label in PAGE_NUM_PATTERNS:
                if re.match(pat, t, re.I):
                    page_fmt = label
                    page_pos = "bottom-right" if x > 0.6 * W else "bottom-left" if x < 0.3 * W else "bottom-center"
    if repeated:
        footer_text = max(repeated, key=len)
    footer_rule = None
    if rules:
        (y, col, w), c = rules.most_common(1)[0]
        if c >= 0.6 * n_pages:
            footer_rule = {"y_points": y, "color": col, "width_points": w}

    # --- logo: top-band image or drawing group that repeats
    logo = None
    cand = [(k, c) for k, c in top_images.items() if c >= 0.6 * n_pages]
    if cand:
        (x0, y0, x1, y1), _ = max(cand, key=lambda kc: (kc[0][2] - kc[0][0]) * (kc[0][3] - kc[0][1]))
        logo = {"kind": "image", "bbox_points": [x0, y0, x1, y1]}
    else:
        groups = [(k, c) for k, c in top_drawings.items() if c >= 0.6 * n_pages]
        if groups:
            xs0 = min(k[0] for k, _ in groups); ys0 = min(k[1] for k, _ in groups)
            xs1 = max(k[2] for k, _ in groups); ys1 = max(k[3] for k, _ in groups)
            # include the wordmark text right next to it, if any
            for block in doc[0].get_text("dict")["blocks"]:
                for line in block.get("lines", []):
                    bx0, by0, bx1, by1 = line["bbox"]
                    if by1 < 0.12 * H and abs(bx0 - xs1) < 0.03 * W:
                        xs1, ys0, ys1 = max(xs1, bx1), min(ys0, by0), max(ys1, by1)
            logo = {"kind": "vector+text", "bbox_points": [round(xs0), round(ys0), round(xs1), round(ys1)],
                    "colors": sorted({k[4] for k, _ in groups})}
    if logo:
        x0, y0, x1, y1 = logo["bbox_points"]
        logo["corner"] = ("top-left" if x0 < 0.3 * W else "top-right" if x0 > 0.6 * W else "top-center")
        logo["relative_width"] = round((x1 - x0) / W, 3)
        if logo_out:
            pad = 4
            clip = fitz.Rect(x0 - pad, y0 - pad, x1 + pad, y1 + pad)
            doc[0].get_pixmap(dpi=300, clip=clip, alpha=True).save(logo_out)
            logo["file"] = logo_out.name

    # --- title-slide decoration: large accent-coloured drawing on page 1 only
    decoration = None
    for dr in doc[0].get_drawings():
        r, fill = dr["rect"], dr.get("fill")
        if fill and 0.05 * W * H < r.width * r.height < 0.8 * W * H and hexc(fill) != background:
            decoration = {"color": hexc(fill), "bbox_points": [round(r.x0), round(r.y0), round(r.x1), round(r.y1)],
                          "shape": "diagonal band" if len(dr["items"]) > 4 else "block"}
            break

    dark = luminance(background) < 0.5
    return {
        "source": pdf_path.name, "pages": n_pages,
        "page_size_points": [round(W, 1), round(H, 1)], "aspect": f"{W / H:.3f}:1",
        "background": background, "dark_theme": dark,
        "palette": [{"hex": c, "area_share": a} for c, a in palette],
        "text_colors": [{"hex": c, "chars": n} for c, n in text_colors],
        "fonts": fonts, "roles": {"display": display, "body": body},
        "logo": logo,
        "footer": {"text": footer_text, "page_number_format": page_fmt, "page_number_position": page_pos, "rule": footer_rule},
        "title_decoration": decoration,
    }


def swatch(brand: dict, out: Path):
    """One-image summary so the agent (or a human) can eyeball the extraction."""
    W, H = 900, 420
    doc = fitz.open(); pg = doc.new_page(width=W, height=H)
    bg = brand["background"]
    def rgb(h): return tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    sh = pg.new_shape(); sh.draw_rect(fitz.Rect(0, 0, W, H)); sh.finish(fill=rgb(bg), color=None); sh.commit()
    tcol = rgb(brand["text_colors"][0]["hex"]) if brand["text_colors"] else (0, 0, 0)
    pg.insert_text((24, 40), f"background {bg}   display: {brand['roles']['display']}   body: {brand['roles']['body']}", fontsize=14, color=tcol)
    x = 24
    for p in brand["palette"]:
        s = pg.new_shape(); s.draw_rect(fitz.Rect(x, 70, x + 110, 150)); s.finish(fill=rgb(p["hex"]), color=None); s.commit()
        pg.insert_text((x, 170), f"{p['hex']} {p['area_share']:.1%}", fontsize=10, color=tcol); x += 125
    y = 210
    for t in brand["text_colors"][:4]:
        pg.insert_text((24, y), f"text {t['hex']}  ({t['chars']} chars)", fontsize=12, color=rgb(t["hex"])); y += 22
    f = brand["footer"]
    pg.insert_text((24, 330), f"footer: {f['text']}", fontsize=10, color=tcol)
    pg.insert_text((24, 350), f"page numbers: {f['page_number_format']} at {f['page_number_position']}   rule: {f['rule']}", fontsize=10, color=tcol)
    lg = brand["logo"]
    pg.insert_text((24, 380), f"logo: {lg and lg['kind']} at {lg and lg['corner']}, width {lg and lg['relative_width']}", fontsize=10, color=tcol)
    if lg and lg.get("file") and Path(lg["file"]).exists():
        pg.insert_image(fitz.Rect(W - 260, 60, W - 24, 160), filename=lg["file"])
    pg.get_pixmap(dpi=96).save(out)


def summary(brand: dict) -> str:
    """Five chat-ready lines describing the profile, for posting in Discord."""
    accent = next((p["hex"] for p in brand["palette"] if p["hex"] != brand["background"]), None)
    text = brand["text_colors"][0]["hex"] if brand["text_colors"] else None
    lg, f = brand["logo"], brand["footer"]
    theme = "dark" if brand["dark_theme"] else "light"
    lines = [
        f"Background {brand['background']} ({theme}), text {text}, primary accent {accent}",
        f"Fonts: {brand['roles']['display']} for titles, {brand['roles']['body']} for body",
        (f"Logo: {lg['corner']}, {lg['relative_width']:.0%} of slide width" if lg else "Logo: none found"),
        f"Footer: {f['text']!r}" if f["text"] else "Footer: none found",
        (f"Page numbers: {f['page_number_format']} at {f['page_number_position']}"
         if f["page_number_format"] else "Page numbers: none found"),
    ]
    return "
".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf", type=Path)
    ap.add_argument("--out", type=Path, default=Path("brand.json"))
    ap.add_argument("--swatch", type=Path, default=None)
    ap.add_argument("--logo", type=Path, default=Path("logo.png"))
    ap.add_argument("--summary", action="store_true", help="print a chat-ready summary instead of raw JSON")
    a = ap.parse_args()
    brand = extract(a.pdf, a.logo)
    a.out.write_text(json.dumps(brand, indent=2), encoding="utf-8")
    if a.swatch:
        swatch(brand, a.swatch)
    if a.summary:
        print(summary(brand))
    else:
        print(json.dumps({k: brand[k] for k in ("background", "roles", "footer", "logo")}, indent=2))
    print("wrote", a.out)


if __name__ == "__main__":
    main()
