#!/usr/bin/env python3
"""Generate LinkedIn Featured asset PNGs and PDFs from a JSON config.

Requires Pillow:
    python -m pip install pillow

Example:
    python scripts/generate_featured_assets.py \
      --config assets/featured-assets-template/example_config.json \
      --out featured-assets-output
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageStat
except ImportError as exc:  # pragma: no cover - exercised only without Pillow
    raise SystemExit("Pillow is required. Install with: python -m pip install pillow") from exc


W = 1080
H = 1080

NAVY = "#06162C"
NAVY_2 = "#0B2E5C"
PANEL = "#0A2A50"
PANEL_2 = "#0E3A70"
BLUE = "#1E6BFF"
CYAN = "#35D5FF"
MINT = "#27D6A3"
GOLD = "#FFC857"
WHITE = "#F7FBFF"
SOFT = "#DCEBFF"
MUTED = "#91A9C6"
LINE = "#244E80"


def font_path(name: str) -> str:
    candidates = [
        Path("C:/Windows/Fonts") / name,
        Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return str(path)
    return str(candidates[-1])


def font(size: int, weight: str = "regular") -> ImageFont.FreeTypeFont:
    windows = {
        "regular": "segoeui.ttf",
        "semibold": "seguisb.ttf",
        "bold": "segoeuib.ttf",
    }
    dejavu = {
        "regular": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "semibold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "bold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    }
    win_path = Path("C:/Windows/Fonts") / windows.get(weight, "segoeui.ttf")
    if win_path.exists():
        return ImageFont.truetype(str(win_path), size)
    path = Path(dejavu.get(weight, dejavu["regular"]))
    if path.exists():
        return ImageFont.truetype(str(path), size)
    return ImageFont.truetype(font_path("arial.ttf"), size)


def rgb(color: str) -> tuple[int, int, int]:
    color = color.strip("#")
    return tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))


def blend(a: str, b: str, t: float) -> tuple[int, int, int]:
    ar = rgb(a)
    br = rgb(b)
    return tuple(int(ar[i] * (1 - t) + br[i] * t) for i in range(3))


def text_size(draw: ImageDraw.ImageDraw, text: str, ft: ImageFont.FreeTypeFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=ft)
    return box[2] - box[0], box[3] - box[1]


def wrapped_lines(draw: ImageDraw.ImageDraw, text: str, ft: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        if not paragraph.strip():
            lines.append("")
            continue
        current = ""
        for word in paragraph.split():
            candidate = word if not current else f"{current} {word}"
            if text_size(draw, candidate, ft)[0] <= max_w:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
    return lines


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    text: str,
    xy: tuple[int, int],
    max_w: int,
    ft: ImageFont.FreeTypeFont,
    fill: str = WHITE,
    line_gap: int = 10,
) -> int:
    x, y = xy
    line_h = text_size(draw, "Ag", ft)[1] + line_gap
    for line in wrapped_lines(draw, text, ft, max_w):
        if line:
            draw.text((x, y), line, font=ft, fill=fill)
        y += line_h
    return y


def fit_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    xy: tuple[int, int],
    box: tuple[int, int],
    start_size: int,
    weight: str = "regular",
    fill: str = WHITE,
    line_gap: int = 10,
) -> int:
    max_w, max_h = box
    for size in range(start_size, 17, -2):
        ft = font(size, weight)
        lines = wrapped_lines(draw, text, ft, max_w)
        line_h = text_size(draw, "Ag", ft)[1] + line_gap
        if len(lines) * line_h <= max_h:
            return draw_wrapped(draw, text, xy, max_w, ft, fill, line_gap)
    return draw_wrapped(draw, text, xy, max_w, font(18, weight), fill, line_gap)


def round_rect(draw: ImageDraw.ImageDraw, box, radius=28, fill=PANEL, outline=None, width=2) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def background(theme: dict[str, str]) -> Image.Image:
    bg_color = theme.get("background", NAVY)
    primary = theme.get("primary", BLUE)
    accent = theme.get("accent", CYAN)
    img = Image.new("RGB", (W, H), bg_color)
    draw = ImageDraw.Draw(img)
    for y in range(H):
        draw.line([(0, y), (W, y)], fill=blend(bg_color, NAVY_2, y / H))

    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((-180, -220, 640, 530), fill=(*rgb(primary), 50))
    gd.ellipse((600, 40, 1350, 800), fill=(*rgb(accent), 34))
    glow = glow.filter(ImageFilter.GaussianBlur(48))
    img = Image.alpha_composite(img.convert("RGBA"), glow)

    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gr = ImageDraw.Draw(grid)
    for x in range(80, W, 120):
        gr.line((x, 0, x, H), fill=(255, 255, 255, 8), width=1)
    for y in range(80, H, 120):
        gr.line((0, y, W, y), fill=(255, 255, 255, 7), width=1)
    return Image.alpha_composite(img, grid).convert("RGB")


def footer(draw: ImageDraw.ImageDraw, person: str, asset: str, page: str) -> None:
    draw.line((70, 1005, 1010, 1005), fill=(255, 255, 255, 35), width=1)
    draw.text((70, 1024), person.upper(), font=font(20, "semibold"), fill=MUTED)
    draw.text((860, 1024), page, font=font(20, "semibold"), fill=MUTED)
    draw.text((70, 970), asset.upper(), font=font(16, "semibold"), fill=MUTED)


def brand_mark(draw: ImageDraw.ImageDraw, x=865, y=76, theme: dict[str, str] | None = None) -> None:
    theme = theme or {}
    primary = theme.get("primary", BLUE)
    accent = theme.get("accent", CYAN)
    secondary = theme.get("secondary", MINT)
    highlight = theme.get("highlight", GOLD)
    round_rect(draw, (x, y, x + 134, y + 54), 18, fill=(14, 45, 83), outline=accent, width=2)
    draw.ellipse((x + 18, y + 17, x + 36, y + 35), fill=accent)
    draw.line((x + 36, y + 26, x + 71, y + 26), fill=primary, width=3)
    draw.ellipse((x + 70, y + 17, x + 88, y + 35), fill=secondary)
    draw.line((x + 88, y + 26, x + 116, y + 26), fill=primary, width=3)
    draw.ellipse((x + 112, y + 17, x + 130, y + 35), fill=highlight)


def pill(draw: ImageDraw.ImageDraw, x: int, y: int, text: str, theme: dict[str, str]) -> int:
    accent = theme.get("accent", CYAN)
    ft = font(24, "semibold")
    tw, th = text_size(draw, text, ft)
    round_rect(draw, (x, y, x + tw + 44, y + th + 22), 999, fill=(9, 37, 72), outline=LINE, width=2)
    draw.text((x + 22, y + 10), text, font=ft, fill=SOFT)
    draw.rounded_rectangle((x, y, x + tw + 44, y + th + 22), radius=999, outline=accent, width=1)
    return x + tw + 44


def new_slide(config: dict[str, Any], asset_name: str, page: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    theme = config.get("theme", {})
    img = background(theme)
    draw = ImageDraw.Draw(img, "RGBA")
    brand_mark(draw, theme=theme)
    footer(draw, config.get("person_name", "Name"), asset_name, page)
    return img, draw


def title(draw: ImageDraw.ImageDraw, text: str, sub: str | None = None) -> None:
    fit_text(draw, text, (70, 112), (880, 130), 58, "bold", WHITE, 10)
    if sub:
        draw_wrapped(draw, sub, (74, 245), 880, font(28), SOFT, 10)


def cover(config: dict[str, Any], asset: dict[str, Any], page: str) -> Image.Image:
    theme = config.get("theme", {})
    img, draw = new_slide(config, asset["title"], page)
    pill(draw, 70, 78, "LINKEDIN FEATURED ASSET", theme)
    end = fit_text(draw, asset["title"], (70, 210), (900, 165), 72, "bold", WHITE, 12)
    y = max(390, end + 42)
    y = draw_wrapped(draw, asset.get("subtitle", ""), (74, y), 850, font(38), SOFT, 16)
    x = 74
    for chip in asset.get("chips", []):
        x = pill(draw, x, y + 46, chip, theme) + 12
    round_rect(draw, (70, 760, 1010, 900), 32, fill=(8, 35, 67), outline=theme.get("primary", BLUE), width=2)
    draw.text((108, 795), "Make the buying path clear.", font=font(38, "semibold"), fill=WHITE)
    draw.text((108, 848), "Attention -> follow-up -> booked call.", font=font(30), fill=theme.get("accent", CYAN))
    return img


def simple_card(draw: ImageDraw.ImageDraw, heading: str, body: str, box, accent=CYAN) -> None:
    x1, y1, x2, y2 = box
    round_rect(draw, box, 24, fill=(10, 42, 80), outline=(35, 84, 138), width=2)
    draw.rounded_rectangle((x1, y1, x1 + 7, y2), radius=8, fill=accent)
    draw.text((x1 + 30, y1 + 24), heading, font=font(29, "bold"), fill=WHITE)
    fit_text(draw, body, (x1 + 30, y1 + 72), (x2 - x1 - 56, y2 - y1 - 90), 23, "regular", SOFT, 7)


def cta_slide(config: dict[str, Any], asset_name: str, page: str) -> Image.Image:
    theme = config.get("theme", {})
    keyword = config.get("positioning", {}).get("cta_keyword", "FLOW")
    img, draw = new_slide(config, asset_name, page)
    title(draw, "Want A Cleaner Client Flow?")
    round_rect(draw, (95, 312, 985, 755), 38, fill=(9, 39, 75), outline=theme.get("accent", CYAN), width=3)
    draw.text((145, 365), "Message", font=font(54), fill=SOFT)
    draw.text((145, 435), keyword, font=font(104, "bold"), fill=theme.get("accent", CYAN))
    draw_wrapped(draw, "If your business gets inquiries but loses momentum in the follow-up, send one message and start with the leak.", (150, 585), 760, font(30), WHITE, 14)
    draw.text((150, 810), "Clear path. Less chasing. More booked conversations.", font=font(28, "semibold"), fill=theme.get("highlight", GOLD))
    return img


def numbered_card(draw: ImageDraw.ImageDraw, n: int, heading: str, body: str, box, theme: dict[str, str]) -> None:
    x1, y1, x2, y2 = box
    round_rect(draw, box, 26, fill=(10, 42, 80), outline=(35, 84, 138), width=2)
    draw.ellipse((x1 + 24, y1 + 28, x1 + 82, y1 + 86), fill=theme.get("primary", BLUE))
    draw.text((x1 + 43, y1 + 38), str(n), font=font(26, "bold"), fill=WHITE)
    draw.text((x1 + 104, y1 + 26), heading, font=font(30, "bold"), fill=WHITE)
    draw_wrapped(draw, body, (x1 + 104, y1 + 72), x2 - x1 - 140, font(23), SOFT, 8)


def make_what_i_build(config: dict[str, Any], asset: dict[str, Any]) -> list[Image.Image]:
    theme = config.get("theme", {})
    pos = config.get("positioning", {})
    pages = [cover(config, asset, "01 / 06")]
    img, draw = new_slide(config, asset["title"], "02 / 06")
    title(draw, "Who It Is For", f"{pos.get('buyer', 'Service businesses')} that already get interest, but lose momentum after the first sign of demand.")
    cards = [
        ("Warm inquiries", "People comment, message, call, or fill a form - then wait for a clear next step."),
        ("Slow response", "The team is busy, so interest cools before it becomes a booked conversation."),
        ("Manual follow-up", "Replies, reminders, and booking prompts depend on memory and spare time."),
        ("Unclear path", "The buyer wants help, but the process does not make yes feel easy."),
    ]
    accents = [theme.get("accent", CYAN), theme.get("secondary", MINT), theme.get("primary", BLUE), theme.get("highlight", GOLD)]
    for i, (h, b) in enumerate(cards):
        simple_card(draw, h, b, (70 + (i % 2) * 480, 285 + (i // 2) * 250, 510 + (i % 2) * 480, 490 + (i // 2) * 250), accents[i])
    pages.append(img)

    img, draw = new_slide(config, asset["title"], "03 / 06")
    title(draw, "The Problem", "Attention is valuable, but the money is usually lost in the handoff.")
    flow = [("Attention", "Content, referral, ad, or post."), ("Interest", "DM, comment, form, or call."), ("Delay", "Reply is late or vague."), ("Drop-off", "Momentum disappears.")]
    for i, (h, b) in enumerate(flow):
        x = 95 + i * 240
        y = 510
        draw.ellipse((x, y, x + 110, y + 110), fill=accents[i % len(accents)])
        draw.text((x + 33, y + 33), str(i + 1), font=font(38, "bold"), fill=NAVY)
        if i < 3:
            draw.line((x + 118, y + 55, x + 215, y + 55), fill=theme.get("accent", CYAN), width=5)
        draw.text((x - 20, y + 145), h, font=font(28, "bold"), fill=WHITE)
        draw_wrapped(draw, b, (x - 45, y + 190), 205, font(21), SOFT, 5)
    pages.append(img)

    img, draw = new_slide(config, asset["title"], "04 / 06")
    title(draw, "The 5-Step Flow", "A practical path from attention to booked conversation.")
    steps = [
        ("Find the leak", "Map where warm leads slow down or disappear."),
        ("Create the angle", "Use content ideas that match buyer objections."),
        ("Clarify the reply", "Make the next message helpful and obvious."),
        ("Prompt the booking", "Move from interest to scheduled call."),
        ("Nurture the maybe", "Remind, reassure, and recover delayed buyers."),
    ]
    for i, (h, b) in enumerate(steps):
        numbered_card(draw, i + 1, h, b, (90, 235 + i * 132, 990, 345 + i * 132), theme)
    pages.append(img)

    img, draw = new_slide(config, asset["title"], "05 / 06")
    title(draw, "What Clients Get", "Not more tools first - a clearer buying path.")
    outcomes = [
        ("Message clarity", "Replies that sound human and reduce confusion."),
        ("Follow-up rhythm", "Prompts and reminders that keep momentum alive."),
        ("Content-to-call path", "A visible connection between attention and booking."),
        ("Less manual chasing", "Simple automation around the client conversation."),
        ("Easier yes", "A buying experience that feels clear and safe."),
    ]
    for i, (h, b) in enumerate(outcomes):
        simple_card(draw, h, b, (88 + (i % 2) * 462, 235 + (i // 2) * 185, 508 + (i % 2) * 462, 385 + (i // 2) * 185), accents[i % len(accents)])
    pages.append(img)
    pages.append(cta_slide(config, asset["title"], "06 / 06"))
    return pages


def make_checklist(config: dict[str, Any], asset: dict[str, Any]) -> list[Image.Image]:
    theme = config.get("theme", {})
    pages = [cover(config, asset, "01 / 05")]
    img, draw = new_slide(config, asset["title"], "02 / 05")
    title(draw, "Score The Client Flow", "Mark each item: clear, weak, or missing. The weak spots are where warm leads leak.")
    checks = ["DMs answered fast", "Comments followed up", "Missed calls recovered", "Inquiries reminded", "Objections handled clearly", "Booking is one obvious next step"]
    for i, item in enumerate(checks):
        x = 100 + (i % 2) * 460
        y = 285 + (i // 2) * 160
        round_rect(draw, (x, y, x + 390, y + 112), 24, fill=(10, 42, 80), outline=(35, 84, 138), width=2)
        draw.rounded_rectangle((x + 26, y + 33, x + 72, y + 79), radius=12, outline=theme.get("accent", CYAN), width=4)
        draw.text((x + 95, y + 35), item, font=font(26, "semibold"), fill=WHITE)
    pages.append(img)
    for page, headline, body in [
        ("03 / 05", "The Reply Gap", "Someone shows interest, then waits. The reply arrives late, vague, or asks them to repeat context."),
        ("04 / 05", "The Booking Gap", "A warm lead should never wonder what to do next. Ask one qualifier, reassure once, and offer the booking step."),
    ]:
        img, draw = new_slide(config, asset["title"], page)
        title(draw, headline, "The smallest communication gaps can become lost opportunities.")
        simple_card(draw, "What to fix", body, (110, 350, 970, 560), theme.get("accent", CYAN))
        simple_card(draw, "Better path", "Helpful reply -> one clear question -> reassurance -> booking prompt -> reminder.", (110, 610, 970, 810), theme.get("secondary", MINT))
        pages.append(img)
    pages.append(cta_slide(config, asset["title"], "05 / 05"))
    return pages


def make_angle_map(config: dict[str, Any], asset: dict[str, Any]) -> list[Image.Image]:
    pages = [cover(config, asset, "01 / 07")]
    theme = config.get("theme", {})
    img, draw = new_slide(config, asset["title"], "02 / 07")
    title(draw, "Example Buyer Context", "Use this map for coaches, consultants, clinics, agencies, or local service providers.")
    for i, (h, b) in enumerate([("Audience", "Interested, but unsure if the service fits."), ("Goal", "Move from passive attention to confident inquiry."), ("Content job", "Answer the question already in the buyer's mind.")]):
        simple_card(draw, h, b, (105, 275 + i * 175, 975, 420 + i * 175), [theme.get("accent", CYAN), theme.get("secondary", MINT), theme.get("highlight", GOLD)][i])
    pages.append(img)
    angles = [
        ("Problem-Aware", "Show the symptom the buyer recognizes.", "You are not lazy. Your follow-up path may be built for a slower business."),
        ("Objection-Aware", "Answer the fear before the sales call.", "If automation sounds robotic, start with reminders and helpful replies - not full replacement."),
        ("Proof-Aware", "Make the result easier to believe.", "Show the before and after: vague response vs. booking-ready response."),
        ("Urgency-Aware", "Explain the cost of waiting without pressure.", "Every delayed reply gives the buyer time to forget, compare, or cool down."),
        ("Comparison-Aware", "Help the buyer choose the smarter path.", "More content creates attention. Better follow-up turns attention into calls."),
    ]
    for idx, (h, b, ex) in enumerate(angles, 3):
        img, draw = new_slide(config, asset["title"], f"{idx:02d} / 07")
        title(draw, h, b)
        round_rect(draw, (100, 330, 980, 720), 36, fill=(9, 39, 75), outline=theme.get("accent", CYAN), width=3)
        draw.text((150, 382), "Sample angle", font=font(28, "semibold"), fill=theme.get("accent", CYAN))
        fit_text(draw, ex, (150, 460), (760, 185), 42, "bold", WHITE, 14)
        pages.append(img)
    return pages


def make_flow_demo(config: dict[str, Any], asset: dict[str, Any]) -> list[Image.Image]:
    pages = [cover(config, asset, "01 / 07")]
    theme = config.get("theme", {})
    img, draw = new_slide(config, asset["title"], "02 / 07")
    title(draw, "The Sequence", "The goal is not to automate noise. The goal is to make the next step easier.")
    for i, step in enumerate(["Inquiry", "Helpful reply", "Qualify", "Reassure", "Book", "Remind"]):
        x = 100 + (i % 3) * 310
        y = 315 + (i // 3) * 260
        draw.ellipse((x, y, x + 126, y + 126), fill=[theme.get("primary", BLUE), theme.get("accent", CYAN), theme.get("secondary", MINT), theme.get("highlight", GOLD), BLUE, CYAN][i])
        draw.text((x + 45, y + 37), str(i + 1), font=font(42, "bold"), fill=NAVY)
        draw.text((x - 20, y + 155), step, font=font(28, "semibold"), fill=WHITE)
    pages.append(img)
    samples = [
        ("1. Inquiry", "Buyer: Hi, I saw your post. How does this work?", "Acknowledge context before pitching."),
        ("2. Helpful Reply", "Business: Happy to help. Usually we start by understanding your goal.", "The reply should feel calm, useful, and specific."),
        ("3. Qualify", "Business: Are you looking for help this month, or still comparing options?", "Ask one question. Do not turn the chat into a form."),
        ("4. Reassure", "Business: The first call is mainly to map the right path, not pressure you.", "Good follow-up lowers the emotional cost of booking."),
        ("5. Book + Remind", "Business: Here are two times. I will send a prep note once booked.", "Make booking obvious, then protect attendance."),
    ]
    for idx, (h, quote, lesson) in enumerate(samples, 3):
        img, draw = new_slide(config, asset["title"], f"{idx:02d} / 07")
        title(draw, h, "Sample message and design principle.")
        round_rect(draw, (90, 300, 990, 585), 34, fill=(9, 39, 75), outline=theme.get("accent", CYAN), width=3)
        fit_text(draw, quote, (135, 360), (800, 130), 34, "semibold", WHITE, 14)
        simple_card(draw, "Why it works", lesson, (120, 655, 960, 815), theme.get("secondary", MINT))
        pages.append(img)
    return pages


def make_philosophy(config: dict[str, Any], asset: dict[str, Any]) -> list[Image.Image]:
    pages = [cover(config, asset, "01 / 06")]
    theme = config.get("theme", {})
    statements = [
        ("Clear Beats Clever", "A buyer should never need to decode what happens next."),
        ("Automation Should Reassure", "The best systems make people feel guided, not processed."),
        ("One Next Step", "Every message should move the buyer toward one clear action."),
        ("Human Before Tool", "The workflow should sound like the business on its best day."),
        ("Easy Yes", "When communication is clear, trust has less friction."),
    ]
    for idx, (h, b) in enumerate(statements, 2):
        img, draw = new_slide(config, asset["title"], f"{idx:02d} / 06")
        title(draw, h)
        round_rect(draw, (105, 340, 975, 720), 38, fill=(9, 39, 75), outline=theme.get("accent", CYAN), width=3)
        fit_text(draw, b, (155, 430), (760, 170), 52, "bold", WHITE, 14)
        draw.text((155, 770), "Principle for client flow systems", font=font(28, "semibold"), fill=theme.get("accent", CYAN))
        pages.append(img)
    return pages


MAKERS = {
    "what_i_build": make_what_i_build,
    "checklist": make_checklist,
    "angle_map": make_angle_map,
    "flow_demo": make_flow_demo,
    "philosophy": make_philosophy,
}


def save_pages(slug: str, pages: list[Image.Image], out: Path) -> None:
    png_root = out / "png" / slug
    pdf_root = out / "pdf"
    png_root.mkdir(parents=True, exist_ok=True)
    pdf_root.mkdir(parents=True, exist_ok=True)
    for i, page in enumerate(pages, 1):
        page.save(png_root / f"{slug}-{i:02d}.png")
    rgb_pages = [page.convert("RGB") for page in pages]
    rgb_pages[0].save(pdf_root / f"{slug}.pdf", save_all=True, append_images=rgb_pages[1:], resolution=144)


def contact_sheet(covers: list[tuple[str, Image.Image]], out: Path) -> None:
    thumb = 360
    gap = 28
    sheet = Image.new("RGB", (thumb * 3 + gap * 4, thumb * 2 + gap * 3), "#07172D")
    draw = ImageDraw.Draw(sheet)
    for i, (slug, img) in enumerate(covers):
        x = gap + (i % 3) * (thumb + gap)
        y = gap + (i // 3) * (thumb + gap)
        sheet.paste(img.resize((thumb, thumb), Image.LANCZOS), (x, y))
        draw.text((x, y + thumb - 32), slug.replace("-", " ").upper(), font=font(13, "semibold"), fill=SOFT)
    sheet.save(out / "png" / "featured-assets-contact-sheet.png")


def validate_images(out: Path) -> list[str]:
    issues: list[str] = []
    for path in sorted((out / "png").rglob("*.png")):
        img = Image.open(path).convert("RGB")
        if img.size != (W, H) and path.name != "featured-assets-contact-sheet.png":
            issues.append(f"{path}: unexpected size {img.size}")
        if max(ImageStat.Stat(img).var) < 1:
            issues.append(f"{path}: likely blank")
    return issues


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate LinkedIn Featured asset kit.")
    parser.add_argument("--config", type=Path, required=True, help="JSON config file.")
    parser.add_argument("--out", type=Path, required=True, help="Output directory.")
    parser.add_argument("--skip-validation", action="store_true", help="Skip nonblank/size validation.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    args.out.mkdir(parents=True, exist_ok=True)

    covers: list[tuple[str, Image.Image]] = []
    for asset in config.get("assets", []):
        maker = MAKERS.get(asset.get("type"))
        if not maker:
            raise SystemExit(f"Unsupported asset type: {asset.get('type')}")
        pages = maker(config, asset)
        save_pages(asset["slug"], pages, args.out)
        covers.append((asset["slug"], pages[0]))

    contact_sheet(covers, args.out)
    if not args.skip_validation:
        issues = validate_images(args.out)
        if issues:
            raise SystemExit("\n".join(issues))
    print(f"Generated {len(covers)} assets in {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
