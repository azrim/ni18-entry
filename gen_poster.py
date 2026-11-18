"""Generate a newspaper-style news infographic for 18 November 2026.

Creates a 1024x1024 PNG summarizing the day's top world news stories.
Uses Pillow with Windows system fonts for rendering.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024

# Color palette - dark editorial style
BG = (15, 20, 30)
HEADER_BG = (20, 30, 50)
CARD_BG = (28, 38, 58)
CREAM = (240, 236, 224)
WHITE = (255, 255, 255)
RED = (200, 50, 40)
GOLD = (220, 180, 60)
TEAL = (40, 180, 170)
BLUE = (60, 120, 200)
ORANGE = (220, 130, 40)
GREY = (140, 140, 150)
LIGHT_GREY = (180, 180, 185)

def font(name, size):
    """Load a Windows system font."""
    return ImageFont.truetype(f"C:/Windows/Fonts/{name}", size)

def wrap_text(draw, text, fnt, max_width):
    """Word-wrap text to fit within max_width."""
    words = text.split()
    lines = []
    current = ""
    for w in words:
        test = (current + " " + w).strip()
        bbox = draw.textbbox((0, 0), test, font=fnt)
        if bbox[2] - bbox[0] > max_width:
            if current:
                lines.append(current)
            current = w
        else:
            current = test
    if current:
        lines.append(current)
    return lines

def draw_story_card(draw, x, y, w, h, tag, tag_color, headline, detail, fnt_tag, fnt_head, fnt_detail):
    """Draw one story card with colored left accent."""
    # Card background
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=CARD_BG)
    # Left accent bar
    draw.rectangle([x, y + 4, x + 5, y + h - 4], fill=tag_color)
    # Tag
    draw.text((x + 16, y + 8), tag, font=fnt_tag, fill=tag_color)
    # Headline
    lines = wrap_text(draw, headline, fnt_head, w - 32)
    ty = y + 30
    for ln in lines[:2]:
        draw.text((x + 16, ty), ln, font=fnt_head, fill=WHITE)
        ty += 24
    # Detail
    if detail:
        detail_lines = wrap_text(draw, detail, fnt_detail, w - 32)
        for ln in detail_lines[:2]:
            draw.text((x + 16, ty + 2), ln, font=fnt_detail, fill=LIGHT_GREY)
            ty += 18

def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Fonts
    fb_lg = font("arialbd.ttf", 36)
    fb_md = font("arialbd.ttf", 20)
    fb_sm = font("arialbd.ttf", 16)
    fr_md = font("arial.ttf", 18)
    fr_sm = font("arial.ttf", 14)
    fr_xs = font("arial.ttf", 12)
    fi_md = font("ariali.ttf", 16)

    # Header band with gradient effect
    for i in range(100):
        alpha = int(15 + (i / 100) * 15)
        d.rectangle([0, i, W, i + 1], fill=(alpha, alpha + 10, alpha + 30))
    d.rectangle([0, 96, W, 100], fill=RED)

    # Masthead - centered title with decorative lines
    d.line([80, 42, W // 2 - 180, 42], fill=(60, 70, 90), width=1)
    d.line([W // 2 + 180, 42, W - 80, 42], fill=(60, 70, 90), width=1)
    d.text((W // 2, 24), "THE WORLD TODAY", anchor="mt", font=fb_lg, fill=CREAM)
    d.text((W // 2, 68), "Wednesday, 18 November 2026  —  the day's biggest stories",
           anchor="mt", font=fi_md, fill=GREY)
    # Date badge
    d.rounded_rectangle([W // 2 - 40, 80, W // 2 + 40, 96], radius=3, fill=RED)
    d.text((W // 2, 82), "NOV 18", anchor="mt", font=fb_sm, fill=WHITE)

    # Stories data - researched events of Nov 18, 2026
    stories = [
        {
            "tag": "SHENZHEN",
            "color": RED,
            "headline": "APEC Leaders' Summit opens in Shenzhen",
            "detail": "World leaders gather for 33rd APEC summit; Putin-Xi bilateral talks on trade and regional security",
        },
        {
            "tag": "UKRAINE",
            "color": GOLD,
            "headline": "Ukrainian strike damages Crimean Bridge",
            "detail": "Drone attacks target strategic infrastructure; Russia retaliates with missile strikes on Kyiv",
        },
        {
            "tag": "MIDDLE EAST",
            "color": ORANGE,
            "headline": "Gulf tensions escalate as drones intercepted near Bahrain bases",
            "detail": "Regional hostilities continue amid multi-front conflict; oil markets on edge",
        },
        {
            "tag": "WASHINGTON",
            "color": BLUE,
            "headline": "US tightens AI chip export controls",
            "detail": "New semiconductor licensing rules target advanced chips for data centers globally",
        },
        {
            "tag": "MANILA",
            "color": TEAL,
            "headline": "Trump meets Quad leaders in Asia tour",
            "detail": "US President holds talks with Japan, Australia, India; signals North Korea summit",
        },
        {
            "tag": "GLOBAL HEALTH",
            "color": (100, 180, 100),
            "headline": "World COPD Day spotlights early diagnosis",
            "detail": "Campaign urges action on chronic lung disease under-diagnosis worldwide",
        },
        {
            "tag": "MARKETS",
            "color": (160, 100, 200),
            "headline": "Asian stocks rebound on Nvidia earnings",
            "detail": "Tech rally lifts regional markets; semiconductor shares surge across Asia-Pacific",
        },
        {
            "tag": "GAZA",
            "color": (200, 80, 80),
            "headline": "Germany demands more humanitarian aid into Gaza",
            "detail": "Foreign minister urges Israel to increase access ahead of severe winter weather",
        },
    ]

    # Layout: 2 columns, 4 rows
    card_w = (W - 48) // 2  # 488 each
    card_h = 105
    gap_x = 16
    gap_y = 12
    start_y = 108

    for i, story in enumerate(stories):
        row = i // 2
        col = i % 2
        x = 16 + col * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y)
        draw_story_card(
            d, x, y, card_w, card_h,
            story["tag"], story["color"],
            story["headline"], story["detail"],
            fb_sm, fb_md, fr_sm
        )

    # Bottom ticker band with styled breaking news
    ticker_y = start_y + 4 * (card_h + gap_y) + 8
    d.rectangle([0, ticker_y, W, ticker_y + 36], fill=(18, 22, 35))
    d.rectangle([0, ticker_y, W, ticker_y + 1], fill=(40, 50, 70))
    d.rounded_rectangle([8, ticker_y + 4, 100, ticker_y + 32], radius=4, fill=RED)
    d.text((54, ticker_y + 8), "BREAKING", anchor="mt", font=fb_sm, fill=WHITE)
    ticker_text = "COP31 pledges $200M for climate  •  Jordan blocks Telegram  •  Apple global outage resolved  •  NSA network disruption"
    d.text((110, ticker_y + 10), ticker_text, font=fr_sm, fill=LIGHT_GREY)

    # Sources footer with divider
    d.line([40, H - 54, W - 40, H - 54], fill=(40, 50, 70), width=1)
    d.text((W // 2, H - 36), "Sources: BBC World · Al Jazeera · Reuters · AP Wire — 18 November 2026",
           anchor="mt", font=fr_xs, fill=GREY)
    d.text((W // 2, H - 18), "AI-generated world news digest  •  make.fun bounty entry",
           anchor="mt", font=fr_xs, fill=(70, 70, 80))

    # Save
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "poster.png")
    img.save(out_path, "PNG", optimize=True)
    print(f"Saved {out_path}")

    # Verify size constraints
    size = os.path.getsize(out_path)
    print(f"Size: {size} bytes ({size/1024:.1f} KB)")
    assert size <= 1048576, f"Image too large: {size} > 1048576"
    assert img.width <= 1024 and img.height <= 1024, f"Dimensions too large: {img.size}"
    print("All checks passed!")

if __name__ == "__main__":
    main()
