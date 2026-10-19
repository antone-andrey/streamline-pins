"""Halloween 2026 sale pins (40% off, ends Oct 31) for Streamline Studio. 1000 x 1500."""
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, "/home/claude/ees/scripts")
from palettes import font_path  # noqa: E402

ROOT = "/home/claude/streamline-pins"
OUT = os.path.join(ROOT, "halloween-2026")
BUNDLE = "/mnt/user-data/uploads/streamline studio/files/05 - The AI Builder Bundle/05 - The AI Builder Bundle/02 Listing images/01-hero.png"
BUNDLE_PIN = "/mnt/user-data/uploads/streamline studio/files/05 - The AI Builder Bundle/05 - The AI Builder Bundle/05 Marketing/pin-1-bundle.png"
LOGO = "/home/claude/ees/assets/brand/lockup-on-dark-1800.png"
W, H = 1000, 1500
ORANGE = (255, 122, 26)
NIGHT1, NIGHT2 = (16, 13, 32), (22, 35, 63)
WHITE = (255, 255, 255)
SOFT = (205, 212, 230)


def F(k, s):
    return ImageFont.truetype(font_path(k), s)


def background():
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(NIGHT1[i] * (1 - t) + NIGHT2[i] * t) for i in range(3)) + (255,))
    # moon glow + moon
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([700, -120, 1120, 300], fill=(255, 170, 90, 90))
    glow = glow.filter(ImageFilter.GaussianBlur(70))
    img.alpha_composite(glow)
    d = ImageDraw.Draw(img)
    d.ellipse([790, -40, 1040, 210], fill=(255, 214, 160, 255))
    d.ellipse([740, -70, 980, 170], fill=NIGHT1 + (255,))  # crescent cut
    random.seed(31)
    for _ in range(40):
        x, y = random.randint(0, W), random.randint(0, 520)
        r = random.choice([1, 1, 2])
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, random.randint(90, 200)))
    # simple bat silhouettes
    for (bx, by, s) in [(640, 120, 1.0), (560, 190, 0.7), (720, 230, 0.55)]:
        pts = [(0, 0), (18, -10), (30, -2), (40, -12), (46, 0), (52, -12), (62, -2), (74, -10), (92, 0), (70, 6), (58, 2), (46, 12), (34, 2), (22, 6)]
        d.polygon([(bx + px * s, by + py * s) for px, py in pts], fill=(10, 8, 20, 255))
    return img


def ctext(d, y, text, font, fill):
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, y), text, font=font, fill=fill)
    return y + font.size * 1.2


def pill(d, cx, y, text, font, bg, fg, pad=(28, 12)):
    w = d.textlength(text, font=font)
    bb = font.getbbox(text)
    h = bb[3] - bb[1]
    x = cx - (w + pad[0] * 2) / 2
    d.rounded_rectangle([x, y, x + w + pad[0] * 2, y + h + pad[1] * 2 + 4], radius=(h + pad[1] * 2) // 2, fill=bg)
    d.text((x + pad[0], y + pad[1] - bb[1] + 2), text, font=font, fill=fg)
    return y + h + pad[1] * 2 + 4


def card(img, src, box, y, maxw=880, maxh=690, radius=26):
    im = Image.open(src).convert("RGB")
    if box:
        im = im.crop(box)
    sc = min(maxw / im.width, maxh / im.height)
    im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, im.width, im.height], radius=radius, fill=255)
    x = (W - im.width) // 2
    sh = Image.new("RGBA", (im.width + 80, im.height + 80), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([40, 50, im.width + 40, im.height + 50], radius=radius, fill=(0, 0, 0, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    img.alpha_composite(sh, (x - 40, y - 40))
    img.paste(im, (x, y), mask)
    ImageDraw.Draw(img).rounded_rectangle([x, y, x + im.width, y + im.height], radius=radius, outline=ORANGE + (255,), width=4)
    return y + im.height


def collage(img, y):
    """Four product tiles for the shop-wide pin."""
    tiles = [
        (f"{ROOT}/budget-01-planner.jpg", (40, 620, 960, 1300)),
        (f"{ROOT}/resume-01-kit.jpg", (40, 620, 960, 1300)),
        (BUNDLE_PIN, (120, 505, 880, 1340)),
        (f"{ROOT}/dev-desk/devdesk-signs-01-gift-under-5.jpg", (60, 430, 940, 920)),
    ]
    tw, th, gap = 420, 320, 24
    x0 = (W - 2 * tw - gap) // 2
    for i, (src, box) in enumerate(tiles):
        im = Image.open(src).convert("RGB").crop(box)
        sc = max(tw / im.width, th / im.height)
        im = im.resize((int(im.width * sc) + 1, int(im.height * sc) + 1), Image.LANCZOS)
        im = im.crop(((im.width - tw) // 2, (im.height - th) // 2, (im.width - tw) // 2 + tw, (im.height - th) // 2 + th))
        mask = Image.new("L", (tw, th), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, tw, th], radius=22, fill=255)
        x = x0 + (i % 2) * (tw + gap)
        yy = y + (i // 2) * (th + gap)
        img.paste(im, (x, yy), mask)
        ImageDraw.Draw(img).rounded_rectangle([x, yy, x + tw, yy + th], radius=22, outline=ORANGE + (255,), width=3)
    return y + 2 * th + gap


def make(name, product, sub, visual, box=None, kind="card"):
    img = background()
    d = ImageDraw.Draw(img)
    logo = Image.open(LOGO).convert("RGBA")
    logo = logo.resize((300, int(300 * logo.height / logo.width)), Image.LANCZOS)
    img.alpha_composite(logo, ((W - logo.width) // 2, 34))
    d = ImageDraw.Draw(img)
    y = pill(d, W / 2, 132, "HALLOWEEN SALE", F("head_bold", 34), ORANGE, (20, 14, 30))
    y = ctext(d, y + 10, "40% OFF", F("head_bold", 170), ORANGE) - 10
    y = ctext(d, y, product, F("head_bold", 56), WHITE)
    y = ctext(d, y - 4, sub, F("head_regular", 36), SOFT) + 18
    if kind == "collage":
        y = collage(img, int(y))
    else:
        y = card(img, visual, box, int(y), maxh=1500 - int(y) - 250)
    d = ImageDraw.Draw(img)
    pill(d, W / 2, y + 36, "Ends October 31  ·  No code needed", F("head_medium", 36), WHITE, (20, 14, 30))
    d.rectangle([0, H - 80, W, H], fill=(10, 8, 20))
    ctext(d, H - 62, "STREAMLINE STUDIO ON ETSY", F("head_medium", 34), ORANGE)
    path = os.path.join(OUT, name)
    img.convert("RGB").save(path, quality=92)
    return path


pins = [
    make("halloween-01-shop-sale.jpg", "Everything in the shop", "Planners, resume templates, AI guides, desk signs", None, kind="collage"),
    make("halloween-02-budget.jpg", "2027 Budget Planner", "Excel + Google Sheets, light and dark", f"{ROOT}/budget-01-planner.jpg", (40, 600, 960, 1370)),
    make("halloween-03-resume.jpg", "ATS Resume and CV Kit", "5 designs, Word, Google Docs, Pages", f"{ROOT}/resume-01-kit.jpg", (40, 600, 960, 1370)),
    make("halloween-04-desk-signs.jpg", "Funny Developer Desk Signs", "20 printable tent cards, instant download", f"{ROOT}/dev-desk/devdesk-signs-01-gift-under-5.jpg", (40, 420, 960, 900)),
    make("halloween-05-bingo.jpg", "Standup Bingo for Developers", "40 printable cards for office fun", f"{ROOT}/dev-desk/devdesk-bingo-01-standup-photo.jpg", (60, 760, 940, 1460)),
    make("halloween-06-ai-bundle.jpg", "The AI Builder Bundle", "4 guides + 18 bonus tools for Claude and AI", BUNDLE_PIN, (120, 505, 880, 1340)),
]
sheet = Image.new("RGB", (6 * 340, 510), "white")
for i, p in enumerate(pins):
    sheet.paste(Image.open(p).resize((340, 510)), (i * 340, 0))
sheet.save("/tmp/halloween-sheet.png")
print("\n".join(pins))
