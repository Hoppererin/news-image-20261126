#!/usr/bin/env python3
"""Draw entry.png for news-image-20261126 — "The World Today".

One image summing up Thursday 26 November 2026: 46 real stories from
7 regions, laid out as a newspaper front page. Every string and every
coordinate below is fixed — no network, no randomness, no clock — so
running this script twice writes byte-identical PNG bytes.

Python 3 + Pillow, DejaVu fonts from the system. Usage: python3 render.py
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (252, 252, 246)
INK = (16, 16, 16)
GREY = (98, 98, 98)
RULE = (176, 176, 166)
CARD = (255, 255, 255)
EDGE = (200, 200, 190)
LEAD_BG = (238, 241, 247)
RED = (186, 0, 0)
BLUE = (12, 78, 142)
PURPLE = (108, 44, 152)
TEAL = (0, 124, 136)
GREEN = (44, 118, 46)
ORANGE = (182, 82, 12)
GOLD = (150, 104, 0)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(d, text, path, size, max_w, floor=10):
    """Largest size <= size that fits, else truncate with an ellipsis."""
    s = size
    while s > floor:
        f = font(path, s)
        if d.textlength(text, font=f) <= max_w:
            return f, text
        s -= 1
    f = font(path, floor)
    while text and d.textlength(text + "…", font=f) > max_w:
        text = text[:-1]
    return f, text + "…"


def wrap(d, text, f, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ------------------------------------------------------------------ content
LEAD_KICKER = "LEAD  —  TARIFFS ON THANKSGIVING EVE"
LEAD_HEAD = "Trump unveils new tariffs on 14 partners"
LEAD_DECK = ("China faces up to 40%, the EU up to 20% under Section 301; "
             "the S&P 500 slips as voters fret over prices. (Reuters)")

BIG = [
    ("HORMUZ", RED,
     "More tankers hit mines in Hormuz as war-risk soars",
     "IRGC says two tankers hit mines on Wednesday, a third LNG "
     "carrier too; 37 ships were attacked in October. (Reuters · IRNA)"),
    ("CAIRO", RED,
     "Fuel tanker fire on Cairo ring road kills at least 30",
     "Tanker overturns in Warraq, Giza; 25 hurt and dozens of cars "
     "charred; the toll may still rise. (AP)"),
    ("UKRAINE", BLUE,
     "Ukraine hits Russian air base, knocks out five jets",
     "Savasleyka struck: 3 MiG-31s and 2 Su-34s hit; US approves a "
     "$622m F-16 equipment sale. (Reuters)"),
    ("GAZA", RED,
     "Israel kills second Hamas security chief in 24 hours",
     "Col. Mohammad Abuelouf, his wife and two daughters die in a "
     "Shati camp strike in Gaza City. (Reuters)"),
    ("EUROPE", PURPLE,
     "EU unveils 22nd Russia sanctions; NATO to guard space",
     "60 banks off SWIFT, 70+ shadow-fleet ships; NATO vows space "
     "defence over nuclear-satellite reports. (Reuters)"),
    ("SPACE", TEAL,
     "BepiColombo safe in Mercury orbit after glitch",
     "ESA confirms capture after an 8-year trip; a software fault "
     "cut the burn short; orbiters split 9 Dec. (ESA)"),
]

BRIEFS = [
    ("NORTH AMERICA", BLUE, [
        "US jobless claims fall to 189,000, beating forecasts",
        "CDC: 9 measles deaths in 2026; 6,039 cases in 47 states",
        "Ábrego García leaves US for Spain, ending deportation fight",
        "Plane crashes off Mississippi coast; 6 aboard, incl. 2 children",
        "Trump pardons turkeys Freedom and Feathers for Thanksgiving",
        "Second judge blocks Trump's birthright-citizenship order",
        "Meta officials meet Congress over suspended accounts",
    ]),
    ("LATIN AMERICA", ORANGE, [
        "Colombia: police free ~30 hostages after 17-hour supermarket siege",
        "Venezuela discloses $237.5bn public debt; wage protests go on",
        "Argentina enters technical recession",
        "Chile: teachers strike nationwide over education spending cuts",
        "Cuba: life expectancy fell for first time since 1950, WHO says",
    ]),
    ("EUROPE", PURPLE, [
        "NATO sends AWACS to Poland after Russian missiles enter airspace",
        "Germany's Merz: Russia 'escalating massively' in Germany and Europe",
        "MI5 warns UK defence firms over Russian attacks; staff at risk",
        "Estonia to close its border with Russia on 1 December",
        "Russia: leaked figures point to nearly 500,000 war dead in Ukraine",
        "Ukraine needs €115bn for 2027; €25bn still to be found",
        "EU to join next Ukraine-Russia talks as Kyiv awaits four-way date",
    ]),
    ("AFRICA", RED, [
        "Libya: satellite images show Russian corvette sunk off Benghazi",
        "Sudan: drone attacks on Khartoum; abductions reported in Blue Nile",
        "DR Congo: military aircraft missing; rebels claim they shot it down",
        "Zambia: opposition leader indicted on treason charges",
    ]),
    ("MIDDLE EAST", GREEN, [
        "Houthis threaten Jeddah and all Saudi Red Sea ports if Hodeidah hit",
        "Saudi strikes hit south-western Yemen; Houthis report deaths",
        "US tells citizens to leave Iran at once as Hormuz tensions rise",
        "Oil spills from damaged tankers reach shores of Oman, images show",
        "Israel: Eisenkot secures first coalition pact, with Lieberman",
        "Iraq stresses independence of decisions amid US deployment reports",
    ]),
    ("ASIA", GOLD, [
        "India marks Constitution Day; Modi holds talks with Germany's Merz",
        "India urges human control over AI in wars and military operations",
        "China: Politburo member Chen Jining investigated in graft crackdown",
        "North Korea orders Switzerland to close its Pyongyang office",
        "Bangladesh: garment minimum wage up 36%, to 17,000 taka a month",
        "Nepal: 5.6-magnitude quake hits Koshi Province near China border",
        "Sensex drops 1,484 points; Nifty slips below 25,400",
    ]),
    ("OCEANIA & PACIFIC", TEAL, [
        "Australia: inflation rises to 4.9%",
        "Australia: sweeping online-safety bill approved; US criticises it",
        "El Niño raises drought risk for Guam and the N. Mariana Islands",
    ]),
]


# ------------------------------------------------------------------ drawing
def masthead(d):
    d.text((W / 2, 18), "THE WORLD TODAY",
           font=font(SERIF_B, 52), fill=INK, anchor="ma")
    d.text((W / 2, 80),
           "THURSDAY 26 NOVEMBER 2026   ·   46 STORIES FROM 7 REGIONS",
           font=font(SANS, 19), fill=INK, anchor="ma")
    d.line([(28, 112), (W - 28, 112)], fill=INK, width=3)
    d.line([(28, 117), (W - 28, 117)], fill=INK, width=1)


def lead(d):
    top, height = 128, 92
    d.rectangle([28, top, W - 28, top + height], fill=LEAD_BG, outline=EDGE)
    d.rectangle([28, top, 35, top + height], fill=RED)
    d.text((46, top + 8), LEAD_KICKER, font=font(SANS_B, 12), fill=RED)
    hf, ht = fit(d, LEAD_HEAD, SANS_B, 24, W - 56 - 36)
    d.text((46, top + 26), ht, font=hf, fill=INK)
    bf = font(SANS, 14)
    y = top + 58
    for line in wrap(d, LEAD_DECK, bf, W - 56 - 36)[:2]:
        d.text((46, y), line, font=bf, fill=GREY)
        y += 17


def big_stories(d):
    y0 = 232
    d.text((28, y0), "THE DAY’S BIG STORIES", font=font(SANS_B, 15), fill=INK)
    d.line([(240, y0 + 8), (W - 28, y0 + 8)], fill=RULE, width=1)
    cw, ch, gap = (W - 56 - 12) // 2, 76, 12
    for i, (tag, color, head, deck) in enumerate(BIG):
        x = 28 + (i % 2) * (cw + gap)
        y = y0 + 26 + (i // 2) * (ch + gap)
        d.rectangle([x, y, x + cw, y + ch], fill=CARD, outline=EDGE)
        d.rectangle([x, y, x + 6, y + ch], fill=color)
        d.text((x + 14, y + 6), tag, font=font(SANS_B, 11), fill=color)
        hf, ht = fit(d, head, SANS_B, 16, cw - 24)
        d.text((x + 14, y + 21), ht, font=hf, fill=INK)
        bf = font(SANS, 12)
        y2 = y + 41
        for line in wrap(d, deck, bf, cw - 24)[:2]:
            d.text((x + 14, y2), line, font=bf, fill=GREY)
            y2 += 14


def region_col(d, regions, x, y, col_w):
    for name, color, stories in regions:
        d.rectangle([x, y + 3, x + 10, y + 13], fill=color)
        d.text((x + 16, y), "%s (%d)" % (name, len(stories)),
               font=font(SANS_B, 13), fill=color)
        y += 18
        for story in stories:
            f, text = fit(d, story, SANS, 12, col_w - 20)
            d.text((x + 16, y), "•  " + text, font=f, fill=INK)
            y += 14
        y += 4
    return y


def briefs(d):
    y0 = 518
    d.text((28, y0), "THE WORLD IN BRIEF", font=font(SANS_B, 15), fill=INK)
    d.line([(224, y0 + 8), (W - 28, y0 + 8)], fill=RULE, width=1)
    top = y0 + 26
    col_w = (W - 56 - 12) // 2
    left_end = region_col(d, BRIEFS[:3], 28, top, col_w)
    right_end = region_col(d, BRIEFS[3:], 28 + col_w + 12, top, col_w)
    box_x = 28 + col_w + 12
    box_y = right_end + 6
    box_h = 60
    d.rectangle([box_x, box_y, W - 28, box_y + box_h],
                fill=CARD, outline=EDGE)
    d.text((box_x + 14, box_y + 8), "HOW TO READ THIS PAGE",
           font=font(SANS_B, 12), fill=INK)
    nf = font(SANS, 12)
    d.text((box_x + 14, box_y + 27),
           "One day, seven regions: every story here was reported 25–26 Nov 2026.",
           font=nf, fill=GREY)
    d.text((box_x + 14, box_y + 43),
           "Lead + 6 big stories + 39 in brief = 46 stories.",
           font=nf, fill=GREY)
    return left_end


def footer(d):
    fy = H - 30
    d.line([(28, fy), (W - 28, fy)], fill=RULE, width=1)
    d.text((W / 2, fy + 6),
           "THE WORLD TODAY — 26 November 2026  ·  All stories as reported 25–26 Nov 2026",
           font=font(SANS, 11), fill=GREY, anchor="ma")


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    masthead(d)
    lead(d)
    big_stories(d)
    briefs(d)
    footer(d)
    img.save("entry.png", format="PNG")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    render()
