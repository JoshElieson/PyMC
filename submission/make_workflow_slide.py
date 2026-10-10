"""Render the 'proposed user workflow' slide for the Track 03 submission.

Run:  python submission/make_workflow_slide.py
Writes submission/workflow_slide.png (1920x1080) and submission/workflow_slide.pdf.
"""
from pathlib import Path

import fitz
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).parent
W, H = 1920, 1080
BG, PANEL, INK, MUTED = "#1F1B24", "#2B2633", "#DCE6F2", "#8C8A94"  # Meridian brand tokens
CORAL, GOLD, TEAL, VIOLET = "#FF6B4A", "#F2C14E", "#DCE6F2", "#8C8A94"


def font(size, bold=False, serif=False):
    names = (("georgiab.ttf" if bold else "georgia.ttf"),) if serif else ()
    for name in names + (("calibrib.ttf" if bold else "calibri.ttf"), ("arialbd.ttf" if bold else "arial.ttf")):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


STEPS = [
    (CORAL, "1", "Set the brand once",
     ["Attach your company deck (PDF) in Discord and say:",
      "“This is our template. Set it as our brand.”",
      "Daimon extracts the colours, fonts, logo and footer and stores brand.json + logo.png for the agent."]),
    (GOLD, "2", "Ask anywhere",
     ["Any thread, any time, nothing attached:",
      "“Which channels drove revenue? Make a 2-slide deck.”",
      "The analysis runs as usual. Every slide is rendered in your brand, not PyMC Labs’."]),
    (TEAL, "3", "Review with buttons",
     ["A form appears in the thread: font, size, colour scheme, style, logo & footer, slide text edits.",
      "Click through, submit, see the re-render.",
      "Undo any round."]),
    (VIOLET, "4", "Publish",
     ["One click: PDF or PPTX, plus style.json so the same look is reused next time.",
      "Footer, page numbers and logo stay exactly as the company deck had them."]),
]


def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # header
    d.text((96, 70), "PROPOSED WORKFLOW", fill=CORAL, font=font(26, True))
    d.text((96, 104), "Your brand, every deck, without re-explaining it", fill=INK, font=font(56, True, serif=True))
    d.text((96, 186), "Two Daimon skills: brand-matched-slides (remembers and applies the brand) "
                      "+ slide-review (interactive restyle and publish)", fill=MUTED, font=font(28))

    # step cards
    n = len(STEPS)
    gap, margin, top, card_h = 32, 96, 300, 560
    card_w = (W - 2 * margin - gap * (n - 1)) // n
    for i, (col, num, title, lines) in enumerate(STEPS):
        x = margin + i * (card_w + gap)
        d.rounded_rectangle((x, top, x + card_w, top + card_h), radius=22, fill=PANEL)
        d.rounded_rectangle((x, top, x + card_w, top + 10), radius=5, fill=col)
        d.ellipse((x + 32, top + 44, x + 96, top + 108), fill=col)
        d.text((x + 64, top + 76), num, fill=BG, font=font(36, True), anchor="mm")
        d.text((x + 112, top + 58), title, fill=INK, font=font(29, True, serif=True))
        y = top + 150
        body = font(25)
        for para in lines:
            colour = col if para.startswith("“") else INK
            for line in wrap(d, para, body, card_w - 64):
                d.text((x + 32, y), line, fill=colour, font=body); y += 38
            y += 18
        # arrow to next card
        if i < n - 1:
            ax = x + card_w + gap // 2
            ay = top + card_h // 2
            d.polygon([(ax - 10, ay - 16), (ax + 10, ay), (ax - 10, ay + 16)], fill=MUTED)

    # footer strip: before / after
    fy = 890
    d.rounded_rectangle((96, fy, W - 96, fy + 110), radius=18, fill=PANEL)
    d.text((128, fy + 22), "Before", fill=MUTED, font=font(24, True))
    d.text((128, fy + 56), "Every thread starts from zero: PyMC Labs style, or re-read the template each time",
           fill=INK, font=font(22))
    d.text((1100, fy + 22), "After", fill=CORAL, font=font(24, True))
    d.text((1100, fy + 56), "Brand set once, applied in every thread, reviewed with clicks, published",
           fill=INK, font=font(22))

    d.line((96, H - 60, W - 96, H - 60), fill=CORAL, width=1)
    d.text((96, H - 36), "Meridian Supply Co.  |  Daimon Hackathon 2026  |  Track 03", fill=MUTED, font=font(20), anchor="lb")
    d.text((W - 96, H - 36), "github.com/JoshElieson/PyMC", fill=MUTED, font=font(20), anchor="rb")
    if False: d.text((W - 96, H - 36), "Daimon Hackathon 2026 · Track 03 · github.com/JoshElieson/PyMC",
           fill=MUTED, font=font(20), anchor="rb")

    png = OUT / "workflow_slide_meridian.png"
    img.save(png)
    pdf = fitz.open(); page = pdf.new_page(width=960, height=540)
    page.insert_image(page.rect, filename=str(png)); pdf.save(OUT / "workflow_slide_meridian.pdf")
    print("wrote", png, "and workflow_slide.pdf")


if __name__ == "__main__":
    main()
