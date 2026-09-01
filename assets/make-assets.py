"""Generate the Bedo theme image assets.

Writes bedo-cover.png and bedo-palette.png next to this script.
Run:  python make-assets.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = Path(__file__).parent

# --- Albedo brand palette -------------------------------------------------
PURPLE = "#412DB5"
INDIGO = "#2D2178"
RAZZ = "#E5197F"
CHART = "#E9FF97"
LGREY = "#F4F4F4"

SPACE_LIGHT = "#6B7398"
SPACE_MID = "#35394C"
SPACE_DARK = "#0C0E1B"

INDIGO_300 = "#604DC6"
INDIGO_200 = "#8173CC"
INDIGO_100 = "#ABA2D4"

SPACE_GREY = "#D9D4E2"
SPACE_GREY_LT = "#E7E4ED"

CHART_LT = "#F7FFD8"
CHART_XLT = "#FCFFF0"

INK = "#14152A"

F_REG = "C:/Windows/Fonts/segoeui.ttf"
F_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
F_LIGHT = "C:/Windows/Fonts/segoeuisl.ttf"
F_MONO = "C:/Windows/Fonts/consola.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def tracked_text(draw, xy, text, fnt, fill, track=0):
    """Draw text with extra letter spacing."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + track


def shadow_layer(size, boxes, blur=18, alpha=90):
    """Return an RGBA layer with blurred dark rectangles under `boxes`."""
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for box, radius in boxes:
        d.rounded_rectangle(box, radius=radius, fill=(6, 7, 14, alpha))
    return layer.filter(ImageFilter.GaussianBlur(blur))


# ==========================================================================
# Mini note preview cards
# ==========================================================================
def draw_card(img, x, y, w, h, mode):
    """Draw a small mock Obsidian window in light or dark mode."""
    d = ImageDraw.Draw(img, "RGBA")
    r = 16

    if mode == "light":
        bg, side, border = "#FFFFFF", LGREY, SPACE_GREY
        h1, body, muted = INDIGO, INK, "#8A8FA6"
        accent, nav_bg = PURPLE, (65, 45, 181, 24)
        code_bg, tag_bg, tag_fg = "#F2F1F7", (65, 45, 181, 26), PURPLE
        hl_fill, hl_line = (233, 255, 151, 140), CHART
        check = PURPLE
    else:
        bg, side, border = SPACE_DARK, "#080A14", "#21253A"
        h1, body, muted = CHART, "#E7E4ED", SPACE_LIGHT
        accent, nav_bg = INDIGO_200, (129, 115, 204, 46)
        code_bg, tag_bg, tag_fg = "#14172A", (233, 255, 151, 31), CHART
        hl_fill, hl_line = (233, 255, 151, 56), CHART
        check = INDIGO_300

    d.rounded_rectangle((x, y, x + w, y + h), radius=r, fill=bg, outline=border, width=1)

    # --- sidebar
    sw = 108
    d.rounded_rectangle((x, y, x + sw + r, y + h), radius=r, fill=side)
    d.rectangle((x + sw - 1, y + r, x + sw, y + h - r), fill=border)

    f_nav = font(F_REG, 13)
    f_nav_b = font(F_BOLD, 13)
    items = ["inbox", "loads", "A-CMG", "vibe data"]
    ny = y + 22
    for i, name in enumerate(items):
        if i == 1:
            d.rounded_rectangle((x + 10, ny - 4, x + sw - 12, ny + 18), radius=5, fill=nav_bg)
            d.text((x + 20, ny), name, font=f_nav_b, fill=accent)
        else:
            d.text((x + 20, ny), name, font=f_nav, fill=muted)
        ny += 30

    # --- main pane
    mx = x + sw + 26
    mw = w - sw - 52
    my = y + 24

    d.text((mx, my), "Random Vibration", font=font(F_BOLD, 25), fill=h1)
    my += 38
    if mode == "light":
        d.line((mx, my, mx + mw, my), fill=border, width=2)
    my += 16

    # body lines
    for frac in (1.0, 0.93, 0.62):
        d.rounded_rectangle((mx, my, mx + int(mw * frac), my + 7), radius=3, fill=muted)
        my += 19

    # highlighted line
    my += 6
    hw = int(mw * 0.55)
    d.rounded_rectangle((mx, my - 3, mx + hw, my + 17), radius=3, fill=hl_fill)
    d.rectangle((mx, my + 15, mx + hw, my + 17), fill=hl_line)
    d.rounded_rectangle((mx + 6, my + 4, mx + hw - 10, my + 10), radius=3, fill=body)
    my += 30

    # tag + code chips
    f_chip = font(F_BOLD, 13)
    tw = int(d.textlength("#grms", font=f_chip)) + 16
    d.rounded_rectangle((mx, my, mx + tw, my + 22), radius=6, fill=tag_bg)
    d.text((mx + 8, my + 3), "#grms", font=f_chip, fill=tag_fg)

    cx = mx + tw + 12
    cw = int(d.textlength("psd.py", font=font(F_MONO, 13))) + 16
    d.rounded_rectangle((cx, my, cx + cw, my + 22), radius=5, fill=code_bg)
    d.text((cx + 8, my + 3), "psd.py", font=font(F_MONO, 13), fill=tag_fg)
    my += 36

    # checkbox row
    d.rounded_rectangle((mx, my, mx + 16, my + 16), radius=5, fill=check)
    d.line((mx + 4, my + 8, mx + 7, my + 12), fill=CHART if mode == "dark" else "#FFFFFF", width=2)
    d.line((mx + 7, my + 12, mx + 13, my + 5), fill=CHART if mode == "dark" else "#FFFFFF", width=2)
    d.rounded_rectangle((mx + 26, my + 5, mx + int(mw * 0.66), my + 12), radius=3, fill=muted)


# ==========================================================================
# Cover
# ==========================================================================
def make_cover():
    W, H = 1600, 800
    img = Image.new("RGB", (W, H), SPACE_DARK)

    # vertical gradient, Space Mid down to Space Dark
    top, bot = hex_rgb("#1B1F33"), hex_rgb(SPACE_DARK)
    g = ImageDraw.Draw(img)
    for row in range(H):
        t = row / (H - 1)
        g.line(
            (0, row, W, row),
            fill=tuple(round(top[i] + (bot[i] - top[i]) * t) for i in range(3)),
        )

    # purple glow behind the text block
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((-260, 120, 700, 900), fill=(65, 45, 181, 70))
    ImageDraw.Draw(glow).ellipse((1150, -300, 1900, 340), fill=(129, 115, 204, 34))
    img = Image.alpha_composite(img.convert("RGBA"), glow.filter(ImageFilter.GaussianBlur(140)))

    # card shadows
    light_box = (820, 118, 820 + 580, 118 + 300)
    dark_box = (1000, 392, 1000 + 580, 392 + 300)
    img = Image.alpha_composite(
        img,
        shadow_layer((W, H), [((light_box[0], light_box[1] + 14, light_box[2], light_box[3] + 20), 16),
                              ((dark_box[0], dark_box[1] + 14, dark_box[2], dark_box[3] + 20), 16)],
                     blur=24, alpha=120),
    )
    img = img.convert("RGB")

    draw_card(img, *light_box[:2], 580, 300, "light")
    draw_card(img, *dark_box[:2], 580, 300, "dark")

    d = ImageDraw.Draw(img, "RGBA")

    # --- text block
    x = 96
    tracked_text(d, (x, 168), "OBSIDIAN THEME", font(F_BOLD, 20), INDIGO_200, track=5)
    d.text((x - 8, 208), "Bedo", font=font(F_BOLD, 168), fill=CHART)
    d.rectangle((x, 400, x + 132, 405), fill=RAZZ)
    d.text((x, 434), "The Albedo brand palette,", font=font(F_LIGHT, 34), fill=INDIGO_100)
    d.text((x, 476), "light and dark.", font=font(F_LIGHT, 34), fill=INDIGO_100)
    d.text(
        (x, 540),
        "One accent hue. 249\u00b0.",
        font=font(F_MONO, 20),
        fill=SPACE_LIGHT,
    )

    # --- swatch chips
    chips = [PURPLE, INDIGO, RAZZ, CHART, INDIGO_300, INDIGO_200, SPACE_LIGHT, LGREY]
    cx, cy, s, gap = x, 630, 58, 12
    for c in chips:
        d.rounded_rectangle((cx, cy, cx + s, cy + s), radius=9, fill=c)
        cx += s + gap

    img.save(OUT / "bedo-cover.png")
    print("wrote bedo-cover.png", img.size)

    # Obsidian's community gallery reads screenshot.png from the repo root.
    img.save(OUT.parent / "screenshot.png")
    print("wrote ../screenshot.png", img.size)


# ==========================================================================
# Palette sheet
# ==========================================================================
GROUPS = [
    ("CORE BRAND", [("Purple", PURPLE), ("Indigo", INDIGO), ("Razzmatazz", RAZZ),
                    ("Chartreuse", CHART), ("Light Grey", LGREY)]),
    ("SPACE GRADIENT \u2014 dark mode surfaces",
     [("Space Light", SPACE_LIGHT), ("Space Mid", SPACE_MID), ("Space Dark", SPACE_DARK)]),
    ("INDIGO TINTS", [("Indigo 300", INDIGO_300), ("Indigo 200", INDIGO_200),
                      ("Indigo 100", INDIGO_100)]),
    ("GREYS \u2014 light mode surfaces", [("Space Grey", SPACE_GREY),
                                          ("Lt Space Grey", SPACE_GREY_LT),
                                          ("Light Grey", LGREY)]),
    ("CHARTREUSE TINTS", [("Chartreuse", CHART), ("Light", CHART_LT), ("X-Light", CHART_XLT)]),
]


def luma(h):
    r, g, b = hex_rgb(h)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def make_palette():
    pad, cw, ch, gap = 36, 208, 116, 18
    W = pad * 2 + cw * 5 + gap * 4
    row_h = 34 + ch + 26
    H = 130 + row_h * len(GROUPS)

    img = Image.new("RGB", (W, H), "#FFFFFF")
    d = ImageDraw.Draw(img, "RGBA")

    d.text((pad, 42), "Albedo Brand Palette", font=font(F_BOLD, 34), fill=INDIGO)
    d.text(
        (pad, 88),
        "Source: color pallette.png  \u00b7  full HEX / RGB / CMYK / PMS values in Albedo-Color-Palette.md",
        font=font(F_REG, 18),
        fill="#6E6A85",
    )

    y = 130
    for title, swatches in GROUPS:
        tracked_text(d, (pad, y), title, font(F_BOLD, 17), PURPLE, track=1.4)
        cy = y + 34
        for i, (name, hexv) in enumerate(swatches):
            cx = pad + i * (cw + gap)
            d.rounded_rectangle((cx, cy, cx + cw, cy + ch), radius=12, fill=hexv,
                                outline=SPACE_GREY, width=1)
            fg = "#FFFFFF" if luma(hexv) < 150 else INK
            d.text((cx + 20, cy + 26), name, font=font(F_BOLD, 21), fill=fg)
            d.text((cx + 20, cy + 62), hexv, font=font(F_MONO, 20), fill=fg)
        y += row_h

    img.save(OUT / "bedo-palette.png")
    print("wrote bedo-palette.png", img.size)


if __name__ == "__main__":
    make_cover()
    make_palette()
