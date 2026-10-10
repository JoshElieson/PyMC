"""Build the brand-source deck for the hackathon: a fictional Meridian Supply Co. board deck
with a distinctive, parseable brand. Produces both PPTX (theme XML, real fonts) and PDF
(what Daimon will most likely read), from the same spec.

Run:  python brand_sources/make_meridian_deck.py

Brand cues deliberately baked in, so the skill has something to find:
  - background: deep charcoal (#1F1B24) with a coral diagonal band on the title slide
  - display font: Georgia (serif) for titles; body font: Calibri
  - palette: coral #FF6B4A (primary accent), gold #F2C14E (secondary), ice #DCE6F2 (text), mist #8C8A94 (muted)
  - logo: wordmark "MERIDIAN" with a wave glyph, top-left on every slide
  - footer: "Meridian Supply Co.  |  Confidential - Board use only  |  Q2 2026 Board Review" left, "n / N" right
  - thin coral rule above the footer
"""
from pathlib import Path

import fitz  # PyMuPDF
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Emu, Inches, Pt

OUT = Path(__file__).parent
BG, CORAL, GOLD, ICE, MIST, PANEL = "#1F1B24", "#FF6B4A", "#F2C14E", "#DCE6F2", "#8C8A94", "#2B2633"
TITLE_FONT, BODY_FONT = "Georgia", "Calibri"
FOOTER = "Meridian Supply Co.  |  Confidential - Board use only  |  Q2 2026 Board Review"

SLIDES = [
    {"kind": "title", "eyebrow": "Q2 2026 BOARD REVIEW",
     "title": "Meridian Supply Co.", "sub": "Revenue, margin and what we do next quarter"},
    {"kind": "content", "title": "Revenue grew 14%, but margin fell for the third quarter",
     "bullets": ["Net revenue EUR 48.2M, +14% YoY, led by dive gear in DACH",
                 "Gross margin 31.4%, down 2.1 pts on freight and oyster-sauce discounting",
                 "Returns rate 6.8%, up from 4.9%; concentrated in car-oil SKUs"],
     "kpis": [("EUR 48.2M", "net revenue"), ("31.4%", "gross margin"), ("6.8%", "returns")]},
    {"kind": "content", "title": "Ad spend is up 40%; we cannot yet show it paid for itself",
     "bullets": ["Paid search and social spend EUR 3.1M in H1, +40% YoY",
                 "Attribution model is last-click only; no holdout has been run",
                 "Proposal: geo holdout on search in Q3, read-out before the Q4 budget"],
     "kpis": [("EUR 3.1M", "H1 ad spend"), ("+40%", "YoY"), ("0", "holdouts run")]},
    {"kind": "closing", "title": "Decisions requested today",
     "bullets": ["Approve Q3 geo holdout on paid search (EUR 120k)",
                 "Approve returns-reduction programme for car-oil SKUs",
                 "Note the revised Q3 revenue guidance of EUR 24-26M"]},
]


def hex_rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# ---------------------------------------------------------------- PPTX
def build_pptx(path):
    prs = Presentation(); prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    W, H = prs.slide_width, prs.slide_height
    blank = prs.slide_layouts[6]

    def rect(slide, x, y, w, h, color, shape=MSO_SHAPE.RECTANGLE):
        s = slide.shapes.add_shape(shape, x, y, w, h)
        s.fill.solid(); s.fill.fore_color.rgb = RGBColor(*hex_rgb(color)); s.line.fill.background(); return s

    def text(slide, x, y, w, h, s, size, color, font, bold=False, align=PP_ALIGN.LEFT, italic=False):
        tb = slide.shapes.add_textbox(x, y, w, h); tf = tb.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.alignment = align; r = p.add_run(); r.text = s
        f = r.font; f.size = Pt(size); f.bold = bold; f.italic = italic; f.name = font
        f.color.rgb = RGBColor(*hex_rgb(color)); return tb

    def chrome(slide, n, total):
        rect(slide, 0, 0, W, H, BG)
        # logo: wave glyph + wordmark
        rect(slide, Inches(0.5), Inches(0.42), Inches(0.42), Inches(0.08), CORAL)
        rect(slide, Inches(0.5), Inches(0.56), Inches(0.3), Inches(0.08), GOLD)
        text(slide, Inches(1.0), Inches(0.3), Inches(3), Inches(0.5), "MERIDIAN", 16, ICE, TITLE_FONT, bold=True)
        # footer rule + text
        rect(slide, Inches(0.5), H - Inches(0.62), W - Inches(1.0), Emu(12700), CORAL)
        text(slide, Inches(0.5), H - Inches(0.55), Inches(10), Inches(0.4), FOOTER, 10, MIST, BODY_FONT)
        text(slide, W - Inches(2.0), H - Inches(0.55), Inches(1.5), Inches(0.4), f"{n} / {total}", 10, MIST, BODY_FONT, align=PP_ALIGN.RIGHT)

    total = len(SLIDES)
    for i, sp in enumerate(SLIDES, 1):
        sl = prs.slides.add_slide(blank); chrome(sl, i, total)
        if sp["kind"] == "title":
            band = rect(sl, Inches(8.2), Inches(-1), Inches(2.2), Inches(10), CORAL, MSO_SHAPE.PARALLELOGRAM)
            band.rotation = 0
            text(sl, Inches(0.5), Inches(2.3), Inches(8), Inches(0.5), sp["eyebrow"], 14, GOLD, BODY_FONT, bold=True)
            text(sl, Inches(0.5), Inches(2.8), Inches(8), Inches(1.4), sp["title"], 48, ICE, TITLE_FONT, bold=True)
            text(sl, Inches(0.5), Inches(4.2), Inches(8), Inches(1), sp["sub"], 20, MIST, BODY_FONT, italic=True)
        else:
            text(sl, Inches(0.5), Inches(1.1), Inches(12.3), Inches(1.3), sp["title"], 32, ICE, TITLE_FONT, bold=True)
            y = Inches(2.7)
            for b in sp["bullets"]:
                rect(sl, Inches(0.55), y + Inches(0.14), Inches(0.12), Inches(0.12), CORAL, MSO_SHAPE.OVAL)
                text(sl, Inches(0.85), y, Inches(7.2), Inches(0.7), b, 18, ICE, BODY_FONT); y += Inches(0.85)
            if "kpis" in sp:
                rect(sl, Inches(8.6), Inches(2.6), Inches(4.2), Inches(3.4), PANEL)
                ky = Inches(2.8)
                for val, lab in sp["kpis"]:
                    text(sl, Inches(8.8), ky, Inches(3.8), Inches(0.6), val, 28, CORAL, TITLE_FONT, bold=True)
                    text(sl, Inches(8.8), ky + Inches(0.55), Inches(3.8), Inches(0.4), lab, 12, MIST, BODY_FONT); ky += Inches(1.05)
    prs.save(path)


# ----------------------------------------------------------------- PDF
def build_pdf(path):
    W, H = 960, 540; doc = fitz.open()
    def c(h): return tuple(v / 255 for v in hex_rgb(h))
    total = len(SLIDES)
    for i, sp in enumerate(SLIDES, 1):
        pg = doc.new_page(width=W, height=H); sh = pg.new_shape()
        sh.draw_rect(fitz.Rect(0, 0, W, H)); sh.finish(fill=c(BG), color=None)
        if sp["kind"] == "title":  # diagonal coral band
            sh.draw_polyline([(600, -10), (760, -10), (680, 550), (520, 550), (600, -10)]); sh.finish(fill=c(CORAL), color=None)
        # logo
        sh.draw_rect(fitz.Rect(36, 30, 66, 36)); sh.finish(fill=c(CORAL), color=None)
        sh.draw_rect(fitz.Rect(36, 40, 58, 46)); sh.finish(fill=c(GOLD), color=None)
        # footer rule
        sh.draw_line((36, H - 44), (W - 36, H - 44)); sh.finish(color=c(CORAL), width=1)
        sh.commit()
        pg.insert_text((72, 46), "MERIDIAN", fontsize=13, fontname="tibo", color=c(ICE))  # Times bold ~ serif stand-in
        pg.insert_text((36, H - 26), FOOTER, fontsize=8, fontname="helv", color=c(MIST))
        pg.insert_text((W - 36 - 30, H - 26), f"{i} / {total}", fontsize=8, fontname="helv", color=c(MIST))
        if sp["kind"] == "title":
            pg.insert_text((36, 190), sp["eyebrow"], fontsize=11, fontname="hebo", color=c(GOLD))
            pg.insert_text((36, 240), sp["title"], fontsize=40, fontname="tibo", color=c(ICE))
            pg.insert_text((36, 280), sp["sub"], fontsize=16, fontname="heit", color=c(MIST))
        else:
            pg.insert_textbox(fitz.Rect(36, 70, 900, 150), sp["title"], fontsize=26, fontname="tibo", color=c(ICE))
            y = 200
            for b in sp["bullets"]:
                s2 = pg.new_shape(); s2.draw_circle((44, y - 5), 4); s2.finish(fill=c(CORAL), color=None); s2.commit()
                pg.insert_textbox(fitz.Rect(60, y - 18, 600, y + 40), b, fontsize=14, fontname="helv", color=c(ICE)); y += 60
            if "kpis" in sp:
                s3 = pg.new_shape(); s3.draw_rect(fitz.Rect(620, 185, 920, 430)); s3.finish(fill=c(PANEL), color=None); s3.commit()
                ky = 230
                for val, lab in sp["kpis"]:
                    pg.insert_text((640, ky), val, fontsize=24, fontname="tibo", color=c(CORAL))
                    pg.insert_text((640, ky + 18), lab, fontsize=10, fontname="helv", color=c(MIST)); ky += 75
    doc.save(path)


if __name__ == "__main__":
    build_pptx(OUT / "meridian_board_deck.pptx")
    build_pdf(OUT / "meridian_board_deck.pdf")
    d = fitz.open(OUT / "meridian_board_deck.pdf")
    for i, p in enumerate(d, 1):
        p.get_pixmap(dpi=96).save(OUT / f"meridian_preview_{i}.png")
    print("wrote pptx, pdf and", len(d), "preview pngs to", OUT)
