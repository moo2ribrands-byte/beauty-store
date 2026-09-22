# Every product's mockup, drawn from the brand's current US packaging (researched Sep 2026).
# Each function returns an Svg whose pack stands on y = H. Colours are estimates from product photos.
from mock_kit import *

D = {}  # sku -> () -> Svg
T = Svg.text


def cl(s, d):
    return f'<g clip-path="{s.clip(Svg.path(d, "#000"))}">'


# ---------------------------------------------------------------- small illustrations
def swirl(x, y, k=1, fill="#fff", edge="#D9DEE6"):
    return (f'<g transform="translate({x:g} {y:g}) scale({k:g})"><path d="M-17 6C-17 -9 -3 -15 9 -11C17 -8 19 2 12 8C6 13 -9 14 -17 6Z" fill="{fill}" stroke="{edge}" stroke-width=".8"/>'
            f'<path d="M-13 7C-6 -2 4 -6 14 -4" fill="none" stroke="{edge}" stroke-width="1.1"/><path d="M-4 -8C2 -10 8 -9 11 -6" fill="none" stroke="#fff" stroke-width="1.6"/></g>')


def cucumber(x, y, r=9):
    seeds = "".join(f'<ellipse cx="{x + r * .45 * __import__("math").cos(a / 6 * 6.283):.2f}" cy="{y + r * .45 * __import__("math").sin(a / 6 * 6.283):.2f}" rx="1" ry=".6" fill="#F4F9E4"/>' for a in range(6))
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#4F8F2E"/><circle cx="{x}" cy="{y}" r="{r * .86:g}" fill="#BFE08A"/><circle cx="{x}" cy="{y}" r="{r * .62:g}" fill="#DDEFB7"/>' + seeds


def leaf(x, y, l=12, rot=-30, col="#3E8B3A"):
    return f'<path d="M0 0C{l * .3:g} {-l * .35:g} {l * .8:g} {-l * .35:g} {l:g} 0C{l * .8:g} {l * .35:g} {l * .3:g} {l * .35:g} 0 0Z" fill="{col}" transform="translate({x:g} {y:g}) rotate({rot})"/>'


def blossom(x, y, r=6, col="#F2A7C3", core="#C2447A"):
    ps = "".join(f'<ellipse cx="{x}" cy="{y - r * .55:g}" rx="{r * .45:g}" ry="{r * .6:g}" fill="{col}" transform="rotate({a} {x} {y})"/>' for a in range(0, 360, 72))
    return ps + f'<circle cx="{x}" cy="{y}" r="{r * .22:g}" fill="{core}"/>'


def coconut(x, y, k=1):
    return (f'<g transform="translate({x} {y}) scale({k})"><path d="M-12 0A12 12 0 0 0 12 0Z" fill="#6B4A32"/><path d="M-10 0A10 9 0 0 0 10 0Z" fill="#F7F3EA"/>'
            f'<path d="M-12 0L12 0" stroke="#4E3322" stroke-width="1.2"/></g>')


def petals(x, y, k=1, col="#F48FB0"):
    return (f'<g transform="translate({x} {y}) scale({k})"><ellipse cx="-6" cy="0" rx="7" ry="4.5" fill="{col}" transform="rotate(-25)"/>'
            f'<ellipse cx="5" cy="-2" rx="7" ry="4.5" fill="{mix(col, .35)}" transform="rotate(30)"/><ellipse cx="0" cy="5" rx="6" ry="4" fill="{mix(col, -.08)}"/></g>')


def pearl(x, y, r=5, col="#F4B6CC"):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}"/><circle cx="{x - r * .35:g}" cy="{y - r * .35:g}" r="{r * .35:g}" fill="#fff" opacity=".8"/>'


def dove_bird(x, y, w=16, col="#B8964A"):
    k = w / 20
    return (f'<path transform="translate({x - w / 2:g} {y:g}) scale({k:g})" fill="{col}" '
            f'd="M0 5C4 2 8 2 11 4C12 1 15 0 18 0C16 1 15 2 15 3L20 3C17 5 14 6 12 8C9 10 5 10 2 8C5 8 7 7 8 6C5 6 2 6 0 5Z"/>')


def pump_bottle_d(w, top, bot, shoulder, neck, r=8, x=0):
    return bottle_d(x, w, top, bot, shoulder, neck, r)


# ================================================================= EOS
EOS_PINK = "#E0177F"


def eos_pebble(sku, body, accent, pill_ink, hero, kind, lines, scent, ink="#2A2A2A", closure="flip", icon=None, collar="#F2F2F2"):
    extra = 58 if closure == "pump" else 0
    s = Svg(sku, 210, 400 + extra)
    top, bot = 40 + extra, 400 + extra
    d = (f"M72 {top}L138 {top}C186 {top} 210 {top + 34} 210 {top + 110}L210 {bot - 74}"
         f"C210 {bot - 16} 190 {bot} 146 {bot}L64 {bot}C20 {bot} 0 {bot - 16} 0 {bot - 74}L0 {top + 110}C0 {top + 34} 24 {top} 72 {top}Z")
    if closure == "flip":
        s.add(Svg.rect(64, 10, 82, 38, s.cyl(collar, .6), rx=4),
              Svg.path("M64 12Q64 0 76 0L134 0Q146 0 146 12L146 17Q124 17 113 21Q105 25 97 21Q86 17 64 17Z", s.cyl(EOS_PINK, .8)))
    else:
        cy = top - 30
        s.add(Svg.rect(66, cy, 78, 32, s.cyl("#F4F4F4", .6), rx=4), Svg.rect(96, cy - 5, 18, 5, s.cyl(EOS_PINK, .8)),
              Svg.rect(100, cy - 24, 10, 20, s.cyl("#F2F2F2", .6)),
              Svg.rect(78, cy - 38, 60, 15, s.cyl("#F6F6F6", .6), rx=4), Svg.rect(40, cy - 35, 44, 7, s.grad([(0, "#fff"), (1, "#D8D8D8")], 0, 1), rx=3))
    s.add(Svg.path(d, s.cyl(body, .55, .3)))
    t = top - 40
    g = [cl(s, d),
         f'<ellipse cx="163" cy="{t + 318}" rx="38" ry="62" transform="rotate(16 163 {t + 318})" fill="{mix(body, .2)}"/>',
         f'<ellipse cx="168" cy="{t + 326}" rx="29" ry="50" transform="rotate(16 168 {t + 326})" fill="{mix(body, .08)}"/>',
         f'<circle cx="105" cy="{t + 116}" r="41" fill="{EOS_PINK}"/>',
         f'<circle cx="105" cy="{t + 116}" r="37" fill="none" stroke="#fff" stroke-width="1.3" stroke-dasharray="53 5.1" stroke-dashoffset="-2.5"/>',
         T(105, t + 124, "eos", 33, "#fff", SANS, 300, fit=50),
         T(105, t + 140, "evolution of", 7.5, "#fff", SANS, 700), T(105, t + 149, "smooth®", 7.5, "#fff", SANS, 700)]
    x = 36
    g += [T(x, t + 178, "shea better™", 11.5, ink, SANS, 700, "start"),
          T(x, t + 198, hero, 21, accent, SERIF, 700, "start", fit=136 if len(hero) > 9 else 102),
          T(x, t + 215, kind, 14.5, ink, SANS, 400, "start", ls=.6),
          Svg.rect(x - 1, t + 221, 136, 15, accent, rx=7.5),
          T(x + 67, t + 232.5, scent, 10.5, pill_ink, SANS, 700)]
    y = t + 252
    for i, (txt, bold) in enumerate(lines):
        g.append(T(x, y, txt, 9.3, ink, SANS, 700 if bold else 400, "start"))
        y += 12 if bold else 13
    if icon:
        g.append(icon(x + 12, y + 8, accent))
    for bx, a, b in ((x + 13, "natural", "shea"), (x + 51, "sensitive", "skin")):
        g += [f'<circle cx="{bx}" cy="{t + 322}" r="14" fill="none" stroke="{ink}" stroke-width=".6" stroke-dasharray="1.6 1.4"/>',
              T(bx, t + 321, a, 5.6, ink, SANS, 700), T(bx, t + 328, b, 5.6, ink, SANS, 700)]
    g += [T(x, t + 356, "16 FL. OZ. (473mL)", 9, ink, SANS, 400, "start"),
          Svg.rect(0, top, 210, bot - top, s.shade(.7)), s.gloss(24, top + 50, 14, 230, .2), "</g>"]
    return s.add(*g)


def i_vanilla(x, y, c):
    return blossom(x, y, 7, c, mix(c, -.4))


def i_coconut(x, y, c):
    return coconut(x - 3, y, .6) + leaf(x + 4, y - 2, 11, -40, c)


def i_hibiscus(x, y, c):
    return blossom(x, y, 8, c, "#fff")


def i_outline(x, y, c):
    return "".join(f'<ellipse cx="{x}" cy="{y - 4.5}" rx="3.5" ry="5" fill="none" stroke="{c}" stroke-width="1.2" transform="rotate({a} {x} {y})"/>' for a in range(0, 360, 72))


def i_fern(x, y, c):
    return f'<path d="M{x} {y + 8}L{x} {y - 8}" stroke="{c}" stroke-width="1.2"/>' + "".join(leaf(x, y + 6 - i * 3.4, 7 - i, -30 if i % 2 else -150, c) for i in range(5))


def i_stars(x, y, c):
    return "".join(blossom(x + dx, y + dy, 4, c, "#fff") for dx, dy in ((-6, 2), (3, -4), (7, 5)))


def i_strawberry(x, y, c):
    return (f'<path d="M{x - 7} {y - 3}C{x - 7} {y + 5} {x - 2} {y + 9} {x} {y + 10}C{x + 2} {y + 9} {x + 7} {y + 5} {x + 7} {y - 3}C{x + 4} {y - 6} {x - 4} {y - 6} {x - 7} {y - 3}Z" fill="{c}"/>'
            + leaf(x - 1, y - 5, 6, -150, "#3E8B3A") + leaf(x + 1, y - 5, 6, -30, "#3E8B3A"))


# (bottle, accent, pill text, icon)
EOS_LOTION = {
    "Vanilla Cashmere": ("#B4B6DC", "#D4DD2A", "#2A2A2A", i_vanilla),
    "Coconut Waters": ("#BCB4B2", "#E3323F", "#fff", i_coconut),
    "Pomegranate Raspberry": ("#F2A8C1", "#9B1147", "#fff", i_hibiscus),
    "Pink Champagne": ("#F5A586", "#D4177C", "#fff", i_outline),
    "Fresh & Cozy": ("#EADAEB", "#1E9CBA", "#fff", i_fern),
    "Jasmine Peach": ("#F4C0C9", "#E3192D", "#fff", i_stars),
    "Strawberry Dream": ("#F1E4D7", "#E0467F", "#fff", i_strawberry),
}
# (bottle, text, pill, pill text)
EOS_WASH = {
    "Vanilla Cashmere": ("#BEBEEB", "#3D3A8C", "#E3EA2F", "#3D3A8C"),
    "Fresh & Cozy": ("#EAD7EC", "#4A2139", "#1BB0D8", "#fff"),
    "Pink Champagne": ("#F8C191", "#7D4A1F", "#D11F84", "#fff"),
    "Coconut Waters": ("#CFC8C8", "#3B2A26", "#EE5A63", "#fff"),
}
_EOS_CODE = {"Vanilla Cashmere": "VC", "Coconut Waters": "CW", "Pomegranate Raspberry": "PR", "Pink Champagne": "PC",
             "Fresh & Cozy": "FC", "Jasmine Peach": "JP", "Strawberry Dream": "SD"}

for sc, (b, a, pi, ic) in EOS_LOTION.items():
    k = f"EOS-LOT-{_EOS_CODE[sc]}-473"
    label = "fresh + cozy" if sc == "Fresh & Cozy" else sc.lower()
    D[k] = (lambda k=k, b=b, a=a, pi=pi, ic=ic, label=label: eos_pebble(
        k, b, a, pi, "24H Moisture", "BODY LOTION",
        [("7 nourishing oils + butters", 0), ("soothing protection", 1), ("for dry skin", 1)], label, closure="pump", icon=ic))
for sc, (b, ink, pill, pi) in EOS_WASH.items():
    k = f"EOS-WASH-{_EOS_CODE[sc]}-473"
    D[k] = (lambda k=k, b=b, ink=ink, pill=pill, pi=pi, sc=sc: eos_pebble(
        k, b, pill, pi, "Cashmere", "BODY WASH", [("gentle cleansing + pH-balanced", 0)], sc.lower(), ink=ink,
        collar=mix(b, .45), icon=EOS_LOTION[sc][3]))


def eos_butter():
    s = Svg("eosbut", 232, 200)
    c = "#B9BCE6"
    d = "M4 36L228 36L228 112C228 170 196 200 150 200L82 200C36 200 4 170 4 112Z"
    s.add(Svg.rect(0, 0, 232, 38, s.cyl(c, .45, .25), rx=6), Svg.rect(0, 34, 232, 3, mix(c, -.2)), Svg.path(d, s.cyl(c, .5, .3)))
    ink = "#2B2C6E"
    s.add(cl(s, d), f'<ellipse cx="196" cy="160" rx="34" ry="44" transform="rotate(20 196 160)" fill="{mix(c, .18)}"/>',
          f'<circle cx="52" cy="96" r="36" fill="{EOS_PINK}"/><circle cx="52" cy="96" r="32.5" fill="none" stroke="#fff" stroke-width="1.1" stroke-dasharray="46 5" stroke-dashoffset="-2.5"/>',
          T(52, 102, "eos", 28, "#fff", SANS, 300, fit=42), T(52, 116, "evolution of", 6.3, "#fff", SANS, 700), T(52, 123.5, "smooth®", 6.3, "#fff", SANS, 700),
          T(98, 74, "shea better™", 9.5, ink, SANS, 700, "start"), T(97, 97, "Cashmere", 24, ink, SERIF, 700, "start", fit=112),
          T(98, 110, "WHIPPED OIL BUTTER", 9.5, ink, SANS, 400, "start", ls=.3),
          Svg.rect(97, 115, 104, 12.5, "#E4E83A", rx=6.25), T(149, 124.5, "vanilla cashmere", 8.5, ink, SANS, 700),
          T(98, 142, "NET WT. 10 OZ. (283g)", 7.5, ink, SANS, 400, "start"),
          Svg.rect(0, 36, 232, 164, s.shade(.6)), "</g>")
    return s


D["EOS-BUT-VC-283"] = eos_butter


def eos_oil():
    s = Svg("eosoil", 84, 270)
    c = "#B6B7E0"
    d = "M18 44L66 44C78 44 84 54 84 76L84 244C84 262 76 270 60 270L24 270C8 270 0 262 0 244L0 76C0 54 6 44 18 44Z"
    ink = "#2B2A6E"
    s.add(Svg.rect(20, 4, 44, 42, s.cyl("#A8ACE0", .5, .3), rx=5), Svg.rect(20, 14, 44, 1.2, mix("#A8ACE0", -.25)),
          Svg.path(d, s.cyl(c, .55, .35)), cl(s, d),
          Svg.rect(0, 150, 84, 120, mix("#A9A6CF", 0), extra='opacity=".45"'),
          f'<ellipse cx="74" cy="150" rx="7" ry="48" fill="{mix(c, .2)}"/>',
          f'<circle cx="42" cy="96" r="23" fill="{EOS_PINK}"/><circle cx="42" cy="96" r="20.5" fill="none" stroke="#fff" stroke-width=".8" stroke-dasharray="29 3.2" stroke-dashoffset="-1.6"/>',
          T(42, 100, "eos", 18, "#fff", SANS, 300, fit=27), T(42, 109, "evolution of", 4, "#fff", SANS, 700), T(42, 114, "smooth®", 4, "#fff", SANS, 700),
          T(11, 176, "shea better™", 6.5, ink, SANS, 700, "start"), T(10, 191, "Cashmere", 15, ink, SERIF, 700, "start", fit=60),
          T(11, 201, "BODY OIL", 7, "#3E3C8F", SANS, 400, "start", ls=.4),
          Svg.rect(10, 205, 62, 9, "#E1E830", rx=4.5), T(41, 211.8, "vanilla cashmere", 5.6, ink, SANS, 700),
          T(11, 224, "24H moisture", 5.4, ink, SANS, 400, "start"), T(11, 231, "plant-based squalane", 5.4, ink, SANS, 400, "start"),
          T(11, 254, "6 FL. OZ. (177 mL)", 5.4, ink, SANS, 400, "start"),
          Svg.rect(0, 44, 84, 226, s.shade(.7)), s.gloss(12, 60, 8, 180, .25), "</g>")
    return s


D["EOS-OIL-VC-177"] = eos_oil


# ================================================================= DOVE
NAVY, GOLD, GREY = "#0F1F5C", "#B8964A", "#8A8A8A"
DOVE_STICK = {  # sku: (scent, pill colour, picture, 'advanced care' | 'invisible')
    "DOV-ST-BF-74": ("beauty finish", "#E8508A", lambda x, y: swirl(x - 4, y, 1.3) + pearl(x + 12, y + 8, 6), "advanced care"),
    "DOV-ST-CC-74": ("caring coconut", "#B85A78", lambda x, y: swirl(x - 6, y - 2, 1.3) + coconut(x + 10, y + 6, .8) + blossom(x + 2, y - 2, 7), "advanced care"),
    "DOV-ST-CE-74": ("cool essentials", "#5BA83A", lambda x, y: swirl(x - 8, y - 4, 1.2) + cucumber(x + 6, y + 4, 9) + cucumber(x - 6, y + 10, 7) + leaf(x + 10, y - 8, 11, -60), "advanced care"),
    "DOV-ST-RP-74": ("rose petals", "#E36C8C", lambda x, y: swirl(x - 4, y, 1.3) + petals(x + 8, y + 6, 1), "advanced care"),
    "DOV-ST-SC-74": ("sheer cool", "#4DBDB4", lambda x, y: f'<circle cx="{x}" cy="{y}" r="16" fill="#4DBDB4"/><circle cx="{x}" cy="{y}" r="12.5" fill="#fff"/>'
                     + T(x, y - 2, "NO", 5, "#2A8F87", SANS, 700) + T(x, y + 4, "WHITE", 5, "#2A8F87", SANS, 700) + T(x, y + 10, "MARKS", 5, "#2A8F87", SANS, 700), "invisible"),
}


def dove_stick(sku):
    scent, pc, pic, line = DOVE_STICK[sku]
    s = Svg(sku, 84, 262)
    body = "M0 58L84 58L84 250Q84 262 72 262L12 262Q0 262 0 250Z"
    cap = "M0 16Q0 0 16 0L68 0Q84 0 84 16L84 62L0 62Z"
    s.add(Svg.path(body, s.cyl("#FFFFFF", .5, .2)), Svg.path(cap, s.cyl("#FBFBFB", .45, .2)), Svg.rect(0, 60, 84, 1.4, "#DADDE2"))
    s.add(Svg.rect(8, 13, 68, 17, pc, rx=8.5), T(20, 25.5, "72H", 10, "#fff", SANS, 700), Svg.rect(30.5, 16, .6, 11, "#fff"),
          T(33, 20.8, "CERAMIDE BARRIER REPAIR", 3.9, "#fff", SANS, 600, "start", fit=38) +
          (T(33, 26.2, "VISIBLY HEALTHY SKIN", 3.9, "#fff", SANS, 600, "start", fit=32) if line != "invisible" else ""))
    s.add(dove_bird(42, 74, 17), T(42, 106, "Dove", 29, NAVY, SERIF, 400, style="italic", fit=56),
          T(42, 120, line, 9.5, GOLD, SERIF, 700, fit=60 if line == "advanced care" else 38),
          Svg.rect(14, 124, 56, 10, pc, rx=5), T(42, 131.3, scent, 6.3, "#fff", SANS, 500), pic(42, 166))
    s.add(T(42, 228, "antiperspirant deodorant", 5.2, GREY, SANS, 400), T(42, 236, "NET WT. 2.6 OZ (74g)", 3.8, GREY, SANS, 400))
    s.add(Svg.rect(0, 0, 84, 262, s.shade(.45)))
    return s


for _k in DOVE_STICK:
    D[_k] = (lambda k=_k: dove_stick(k))


def dove_original():
    s = Svg("dovoc", 84, 262)
    body = "M2 60L82 60C80 110 76 150 78 190C80 220 84 240 84 250Q84 262 72 262L12 262Q0 262 0 250C0 240 4 220 6 190C8 150 4 110 2 60Z"
    cap = "M2 18Q2 2 18 2L66 2Q82 2 82 18L82 64L2 64Z"
    s.add(Svg.path(body, s.cyl("#FFFFFF", .5, .2)), Svg.path(cap, s.cyl("#BFD8EA", .5, .5), 'opacity=".92"'),
          Svg.rect(14, 6, 56, 10, "#E3EEF7", rx=5, extra='opacity=".7"'), Svg.rect(2, 62, 80, 1.4, "#A9C3D8"))
    s.add(dove_bird(42, 80, 17), T(42, 112, "Dove", 29, NAVY, SERIF, 400, style="italic", fit=56),
          Svg.rect(15, 118, 54, 10, "#2E6FD1", rx=5), T(42, 125.3, "original clean", 6.3, "#fff", SANS, 500),
          f'<path d="M20 140A14 14 0 0 0 44 140A11 11 0 0 1 20 140Z" fill="{GOLD}"/>', T(38, 150, "¼ moisturizers", 4.6, GOLD, SANS, 600),
          f'<path d="M12 186C28 164 58 160 74 170C58 170 36 176 22 194Z" fill="#C9DDF2"/>',
          T(72, 206, "all day sweat &", 4.6, "#2E6FD1", SANS, 600, "end"), T(72, 212, "odor protection", 4.6, "#2E6FD1", SANS, 600, "end"),
          T(42, 230, "ANTIPERSPIRANT DEODORANT", 4, GREY, SANS, 600), T(42, 236, "NET WT. 2.6 OZ (74g)", 3.6, GREY, SANS, 400),
          Svg.rect(0, 0, 84, 262, s.shade(.45)))
    return s


D["DOV-ST-OC-74"] = dove_original


def dove_spray():
    s = Svg("dovds", 60, 290)
    can = "M4 66C4 58 10 54 18 54L42 54C50 54 56 58 56 66L56 280Q56 290 46 290L14 290Q4 290 4 280Z"
    s.add(Svg.path("M6 58L6 26C6 8 18 0 30 0C42 0 54 8 54 26L54 58Z", s.cyl("#B9D98F", .6, .45)),
          f'<ellipse cx="30" cy="14" rx="9" ry="4" fill="{mix("#B9D98F", -.15)}"/>',
          Svg.path(can, s.cyl("#FFFFFF", .7, .1)), Svg.rect(4, 280, 52, 10, s.cyl("#D9DDE2", .8), rx=4))
    s.add(dove_bird(30, 84, 14), T(30, 110, "Dove", 23, NAVY, SERIF, 400, style="italic", fit=44),
          T(30, 124, "advanced", 8.5, GOLD, SERIF, 700), T(30, 134, "care", 8.5, GOLD, SERIF, 700),
          Svg.rect(8, 139, 44, 9, "#5BA83A", rx=4.5), T(30, 145.5, "cool essentials", 5.4, "#fff", SANS, 500),
          swirl(22, 176, 1), cucumber(36, 184, 9), cucumber(24, 196, 7), leaf(38, 166, 10, -70),
          T(30, 250, "antiperspirant deodorant", 4, GREY, SANS, 400), T(30, 257, "NET WT 3.8 OZ (107g)", 3.3, GREY, SANS, 400),
          Svg.rect(4, 54, 52, 236, s.shade(.5)))
    return s


D["DOV-DS-CE-107"] = dove_spray


def dove_wash():
    s = Svg("dovbw", 100, 320)
    b = "M24 36L76 36C92 40 96 58 96 84L100 304Q100 320 84 320L16 320Q0 320 0 304L4 84C4 58 8 40 24 36Z"
    s.add(Svg.rect(24, 4, 52, 36, s.cyl("#FAFAFA", .5), rx=5), Svg.rect(24, 4, 52, 8, s.cyl("#8CC63F", .6), rx=4),
          Svg.path(b, s.cyl("#FFFFFF", .5, .15)))
    s.add(dove_bird(50, 76, 18), T(50, 110, "Dove", 32, NAVY, SERIF, 400, style="italic", fit=62),
          f'<circle cx="84" cy="100" r="6" fill="none" stroke="{GOLD}" stroke-width="1.2"/>', T(84, 102.3, "#1", 5.5, GOLD, SANS, 700),
          T(50, 128, "refresh", 13, "#6BAF2E", SERIF, 700), Svg.rect(16, 133, 68, 10, "#8CC63F", rx=5),
          T(50, 140.3, "cucumber + green tea", 6, "#fff", SANS, 500),
          T(34, 164, "24", 20, GOLD, SANS, 700), T(47, 154, "hr RENEWING", 4.6, GOLD, SANS, 700, "start"), T(47, 160, "MICROMOISTURE", 4.6, GOLD, SANS, 700, "start"),
          swirl(42, 212, 1.4), cucumber(62, 220, 11), cucumber(46, 232, 9), leaf(66, 196, 13, -70),
          T(50, 270, "24hr lotion-soft skin", 5.6, "#6BAF2E", SANS, 600), T(50, 288, "body wash  |  20 FL OZ (591 mL)", 4.6, GREY, SANS, 400),
          Svg.rect(0, 36, 100, 284, s.shade(.5)), s.gloss(12, 70, 8, 200, .5))
    return s


D["DOV-REF-CGT-BW-591"] = dove_wash


# ================================================================= DIFEEL
def difeel_logo(x, y, k=1):
    return (f'<g transform="translate({x} {y}) scale({k})"><ellipse rx="17" ry="9" fill="#fff" stroke="#C9A04A" stroke-width="1.4"/>'
            + T(0, 2, "Difeel", 9, "#111", SERIF, 700) + T(0, 6.4, "DIFFERENT FEEL", 2.4, "#111", SANS, 600) + "</g>")


def difeel_rm(s, x0, kind):
    w, top, bot = 100, 70, 300
    d = bottle_d(x0, w, top, bot, 30, 30, 8)
    s.add(*pump(s, x0 + 50, top + 2, "#1C1C1C", head_w=34, stem=14, nozzle=26, left=False, collar_w=30, collar_h=14))
    s.add(Svg.path(d, s.cyl("#66752A", .7, .6)), cl(s, d),
          Svg.rect(x0, 118, w, 166, "#0B6B4B"), Svg.rect(x0, 123, w, 1, "#A8DCC0"), Svg.rect(x0, 279, w, 1, "#A8DCC0"),
          difeel_logo(x0 + 50, 136, 1),
          T(x0 + 10, 170, "rosemary", 17, "#fff", SERIF, 700, "start", fit=74), T(x0 + 10, 187, "& mint", 17, "#fff", SERIF, 700, "start"),
          T(x0 + 10, 204, kind, 12, "#A8DCC0", COND, 700, "start", fit=56 if kind == "SHAMPOO" else 76),
          Svg.rect(x0 + 10, 209, 62, 8, "#A8DCC0"), T(x0 + 41, 215, "INFUSED WITH BIOTIN", 4.6, "#0B6B4B", COND, 700),
          T(x0 + 10, 228, "Strengthens dry and damaged hair to", 4, "#fff", SERIF, 400, "start"),
          T(x0 + 10, 233.5, "help promote growth, manageability", 4, "#fff", SERIF, 400, "start"),
          T(x0 + 10, 239, "and shine", 4, "#fff", SERIF, 400, "start"),
          T(x0 + 10, 248, "Smooths split ends and helps dry,", 4, "#fff", SERIF, 400, "start"),
          T(x0 + 10, 253.5, "flaky scalp", 4, "#fff", SERIF, 400, "start"),
          T(x0 + 10, 272, "1 Liter / 33.8 Fl Oz (U.S.)", 4, "#fff", SANS, 400, "start"),
          Svg.rect(x0 + 64, 266.5, 9, 5.4, "#B22234"), Svg.rect(x0 + 64, 266.5, 4, 2.9, "#3C3B6E"),
          T(x0 + 75, 271, "MADE IN USA", 3, "#fff", SANS, 700, "start", fit=16),
          Svg.rect(x0, top, w, bot - top, s.shade(.8)), s.gloss(x0 + 12, 90, 7, 190, .35), "</g>")


def difeel_batana(s, x0, kind):
    w, top, bot = 78, 66, 320
    d = bottle_d(x0, w, top, bot, 24, 24, 7)
    s.add(*pump(s, x0 + 39, top + 2, "#C8963E", head_w=26, stem=12, nozzle=30, left=False, collar_w=26, collar_h=16, metal=True))
    s.add(Svg.rect(x0 + 26, top - 44, 26, 11, s.cyl("#D0D0D0", 1.2, .9), rx=3))
    s.add(Svg.path(d, s.cyl("#7A3A1C", .7, .7)), cl(s, d),
          Svg.rect(x0, 128, w, 150, s.grad([(0, "#F08A6C"), (1, "#EE8466")], 0, 1)),
          Svg.rect(x0, 136, w, .8, "#D4A24A"), Svg.rect(x0, 270, w, .8, "#D4A24A"),
          f'<g fill="none" stroke="#F8C0AA" stroke-width=".8" opacity=".9"><path d="M{x0 + 78} 190C{x0 + 60} 205 {x0 + 50} 230 {x0 + 48} 268"/>'
          f'<path d="M{x0 + 60} 206C{x0 + 70} 200 {x0 + 78} 204 {x0 + 80} 212"/><path d="M{x0 + 54} 222C{x0 + 42} 214 {x0 + 36} 218 {x0 + 34} 226"/>'
          f'<ellipse cx="{x0 + 62}" cy="244" rx="6" ry="8"/><ellipse cx="{x0 + 70}" cy="254" rx="5" ry="7"/></g>',
          difeel_logo(x0 + 39, 138, .85),
          T(x0 + 8, 176, "batana", 19, "#fff", SERIF, 700, "start", fit=60),
          T(x0 + 8, 188, "SULFATE-FREE", 5.4, "#fff", COND, 700, "start"),
          T(x0 + 8, 199, kind, 9.5, "#fff", COND, 700, "start", fit=42 if kind == "SHAMPOO" else 56),
          T(x0 + 8, 212, "Promotes thicker, smoother, and", 3.5, "#fff", SERIF, 400, "start"),
          T(x0 + 8, 217, "more manageable hair.", 3.5, "#fff", SERIF, 400, "start"),
          T(x0 + 8, 225, "Our strengthening formula leaves", 3.5, "#fff", SERIF, 400, "start"),
          T(x0 + 8, 230, "hair stronger and fuller", 3.5, "#fff", SERIF, 400, "start"),
          T(x0 + 8, 262, "1 Liter / 33.8 fl oz (U.S.)", 3.5, "#fff", SANS, 400, "start"),
          Svg.rect(x0 + 60, 257, 8, 5, "#B22234"), Svg.rect(x0 + 60, 257, 3.6, 2.7, "#3C3B6E"),
          Svg.rect(x0, top, w, bot - top, s.shade(.8)), s.gloss(x0 + 10, 84, 6, 210, .4), "</g>")


def difeel_duo(sku, fn, w, gap):
    def make():
        s = Svg(sku, 2 * w + gap, 320)
        fn(s, 0, "SHAMPOO")
        fn(s, w + gap, "CONDITIONER")
        return s
    return make


D["DIF-RM-DUO-1L"] = difeel_duo("difrm", difeel_rm, 100, 8)
D["DIF-BAT-DUO-1L"] = difeel_duo("difbat", difeel_batana, 78, 8)


def difeel_leavein():
    s = Svg("diflci", 70, 300)
    top, bot = 84, 300
    d = bottle_d(4, 62, top, bot, 18, 22, 6)
    s.add(Svg.rect(24, 64, 22, 22, s.cyl("#151515", .6), rx=2),
          Svg.path("M20 66L20 40C20 30 26 24 36 24L54 24C62 24 66 28 66 34L66 40L50 42L46 66Z", s.cyl("#111", .6, .4)),
          Svg.path("M46 46L58 48L54 80C52 84 48 84 48 80Z", "#1A1A1A"), Svg.rect(62, 30, 8, 7, "#222", rx=2))
    s.add(Svg.path(d, s.cyl("#E6EEEA", .4, .6), 'opacity=".6"'), cl(s, d),
          Svg.rect(4, top + 20, 62, bot - top - 20, "#EEF3EC", extra='opacity=".5"'),
          Svg.rect(4, 118, 62, 162, "#0B6B4B"), Svg.rect(4, 118, 62, 10, "#F7D117"),
          T(35, 125.5, "30% MORE FREE!", 6, "#D2232A", SANS, 800),
          Svg.rect(4, 134, 62, .8, "#A8DCC0"), difeel_logo(35, 140, .75),
          T(10, 164, "rosemary", 12, "#fff", SERIF, 700, "start", fit=50), T(10, 176, "& mint", 12, "#fff", SERIF, 700, "start"),
          T(10, 188, "LEAVE-IN", 7, "#A8DCC0", COND, 700, "start"), T(10, 196, "CONDITIONING", 7, "#A8DCC0", COND, 700, "start"),
          T(10, 204, "SPRAY", 7, "#A8DCC0", COND, 700, "start"),
          Svg.rect(10, 208, 44, 6, "#A8DCC0"), T(32, 212.6, "INFUSED WITH BIOTIN", 3.4, "#0B6B4B", COND, 700),
          T(10, 224, "Helps promote growth,", 3.4, "#fff", SERIF, 400, "start"), T(10, 229, "manageability and shine", 3.4, "#fff", SERIF, 400, "start"),
          T(10, 237, "Helps repair split ends", 3.4, "#fff", SERIF, 400, "start"), T(10, 242, "and moisturizes dry scalp", 3.4, "#fff", SERIF, 400, "start"),
          T(10, 268, "237 mL / 8 Fl Oz (U.S.)", 3.4, "#fff", SANS, 400, "start"),
          Svg.rect(4, top, 62, bot - top, s.shade(.7)), s.gloss(10, 100, 5, 180, .5), "</g>")
    return s


D["DIF-RM-LCS-267"] = difeel_leavein


# ================================================================= FENTY HAIR
FH, FH_INK = "#A9D3CC", "#3A3F3E"


def fenty_jar():
    s = Svg("fhjar", 232, 104)
    d = "M4 30L228 30L228 90Q228 104 212 104L20 104Q4 104 4 90Z"
    s.add(Svg.rect(0, 0, 232, 32, s.cyl(FH, .45, .2), rx=8), Svg.rect(2, 29, 228, 2.5, mix(FH, -.18)),
          Svg.path(d, s.cyl(FH, .5, .2)))
    sp = 3.2
    s.add(f'<circle cx="34" cy="67" r="9" fill="none" stroke="{FH_INK}" stroke-width=".8"/><circle cx="34" cy="67" r="5.5" fill="none" stroke="{FH_INK}" stroke-width=".6"/>',
          T(52, 64, "FENTY", 9, FH_INK, SANS, 500, "start", ls=sp), T(52, 76, "HAIR", 9, FH_INK, SANS, 500, "start", ls=sp),
          T(128, 55, "THE RICHER ONE", 6.4, FH_INK, SANS, 800, "start"),
          T(128, 64, "moisture repair", 5.2, FH_INK, SANS, 400, "start"), T(128, 70.5, "deep conditioner", 5.2, FH_INK, SANS, 400, "start"),
          T(128, 78, "après-shampooing réparateur", 4.4, FH_INK, SANS, 400, "start"), T(128, 83.5, "hydratant intense", 4.4, FH_INK, SANS, 400, "start"),
          T(128, 92, "340ML / 11.5FL. OZ.", 4.6, FH_INK, COND, 700, "start"),
          Svg.rect(4, 30, 224, 74, s.shade(.45)))
    return s


D["FEN-DC-RICH-340"] = fenty_jar


def fenty_bottle():
    s = Svg("fhbot", 84, 290)
    top, bot = 70, 290
    d = bottle_d(0, 84, top, bot, 22, 34, 5)
    s.add(Svg.rect(24, top - 18, 36, 20, s.cyl(FH, .5), rx=3), Svg.rect(38, top - 34, 8, 16, s.cyl(FH, .5)),
          Svg.rect(24, top - 46, 36, 13, s.cyl(FH, .5), rx=4), Svg.rect(4, top - 43, 24, 6, s.cyl(mix(FH, -.05), .5), rx=3),
          Svg.path(d, s.cyl(FH, .5, .2)))
    s.add(f'<g transform="translate(46 108) rotate(90)">' + T(0, 0, "FENTY", 9, FH_INK, SANS, 500, "start", ls=6) + "</g>",
          f'<g transform="translate(34 108) rotate(90)">' + T(0, 0, "HAIR", 9, FH_INK, SANS, 500, "start", ls=6) + "</g>",
          f'<circle cx="42" cy="212" r="6" fill="none" stroke="{FH_INK}" stroke-width=".7"/>' + T(42, 214.5, "5", 6, FH_INK, SANS, 700),
          T(42, 229, "THE RICH ONE", 6, FH_INK, SANS, 800), T(42, 237, "moisture repair conditioner", 4, FH_INK, SANS, 400),
          T(42, 243, "après-shampooing", 3.6, FH_INK, SANS, 400), T(42, 248, "réparateur hydratant", 3.6, FH_INK, SANS, 400),
          T(42, 256, "300ML / 10FL. OZ.", 3.8, FH_INK, COND, 700), Svg.rect(0, top, 84, bot - top, s.shade(.5)))
    return s


D["HAI-CON-RICH-300"] = fenty_bottle


# ================================================================= SHOWER MATE (Aekyung)
def shower_mate(sku, body, pumpc, script, scol, band, bandtxt, extra_pic=False):
    def make():
        s = Svg(sku, 120, 340)
        top, bot = 66, 340
        d = bottle_d(0, 120, top, bot, 40, 40, 9)
        s.add(*pump(s, 60, top + 2, pumpc, head_w=30, stem=12, nozzle=34, left=False, collar_w=34, collar_h=20))
        s.add(Svg.path(d, s.cyl(body, .45, .35)), cl(s, d),
              Svg.rect(14, 154, 92, 164, "#FFFFFF"), f'<rect x="17" y="157" width="86" height="158" fill="none" stroke="#C9A04A" stroke-width=".9"/>',
              f'<circle cx="60" cy="172" r="9" fill="#222"/>', T(60, 171, "Shower", 4.4, "#fff", SCRIPT, 400), T(60, 176, "mate", 4.4, "#fff", SCRIPT, 400),
              T(60, 190, "- PURE & NATURAL -", 3.6, "#333", SANS, 600, ls=.5), T(60, 204, "GOAT MILK", 14, "#111", SERIF, 700, fit=70),
              T(60, 213, "BODY WASH", 6.5, "#111", SERIF, 700, ls=.6),
              '<g fill="none" stroke="#222" stroke-width=".7" stroke-linecap="round" stroke-linejoin="round">'
              '<path d="M42 234C44 229 52 228 60 229C66 229.5 70 228 72 225L74 220L77 221L76 226L79 228L77 230L74 230C72 234 70 237 69 240"/>'
              '<path d="M42 234C41 237 43 240 45 240M45 240L45 250M48 240L48 250M66 240L66 250M69 240L69 250M45 240C52 242 60 242 69 240"/>'
              '<path d="M74 220C73 216 70 214 68 214M76 221C76 217 74 214 72 213M42 234L39 231"/></g>',
              T(60, 260, script, 9, scol, SCRIPT, 700), Svg.rect(28, 264, 64, 7, band), T(60, 269.4, bandtxt, 4, "#fff", SANS, 600),
              T(60, 281, "산양유 바디워시", 5.4, "#111", SANS, 800),
              Svg.rect(34, 286, 6, 4, "#21468B"), Svg.rect(34, 286, 6, 1.33, "#AE1C28"), Svg.rect(34, 287.33, 6, 1.34, "#fff"),
              T(42, 289.6, "DUTCH GOAT MILK", 3.4, "#333", SANS, 600, "start"), T(60, 297, "HERB-PURE COMPLEX", 3.2, "#555", SANS, 400),
              T(60, 308, "800 mL / 27.05 fl. oz.", 3.6, "#333", SANS, 400),
              coconut(94, 300, .45) + blossom(86, 304, 3.2, "#fff", "#C0703A") if extra_pic else "",
              Svg.rect(0, top, 120, bot - top, s.shade(.6)), s.gloss(10, 110, 7, 190, .3), "</g>")
        return s
    return make


D["SHM-GM-CV-800"] = shower_mate("shmcv", "#E8A878", "#B8845A", "Hydrating", "#C0703A", "#C98A55", "WITH COCONUT & VANILLA", True)
D["SHM-GM-MH-800"] = shower_mate("shmmh", "#D8C3A5", "#F0B232", "nourishing", "#C99A2E", "#D9A93A", "WITH MANUKA HONEY")


# ================================================================= BATH & BODY WORKS
def bbw_mist(sku, style):
    """8 fl oz fine fragrance mist: about 9.8 x 1.9 in bottle, clear over-cap on a metal-collar sprayer."""
    def make():
        s = Svg(sku, 60, 320)
        d = "M4 70C4 62 10 58 18 58L42 58C50 58 56 62 56 70L56 310Q56 320 46 320L14 320Q4 320 4 310Z"
        overcap = "M5 60L5 12C5 5 10 1 17 1L43 1C50 1 55 5 55 12L55 60Z"
        cx = 30
        if style == "warm":
            s.add(Svg.path(d, s.grad([(0, "#F2C3A2"), (1, "#C9B2C4")], 0, 1)), cl(s, d),
                  T(cx, 176, "WARM", 12, "#B8735A", SANS, 300, fit=40), T(cx, 190, "MUSK", 8.5, "#8A4F3A", SANS, 800, ls=1.6),
                  T(cx, 198, "BY", 3.2, "#8A4F3A", SANS, 500), T(cx, 205, "BATH & BODY WORKS", 3.2, "#B8735A", SANS, 700, fit=40),
                  T(cx, 270, "DERMATOLOGIST TESTED", 2.8, "#fff", SANS, 600, fit=36), T(cx, 280, "FINE FRAGRANCE MIST", 3.6, "#fff", SERIF, 700, fit=42),
                  T(cx, 287, "FOR BODY & HAIR", 3, "#fff", SANS, 500), T(cx, 306, "8 FL OZ / 236 mL", 3.2, "#fff", SANS, 500),
                  Svg.rect(4, 58, 52, 262, s.shade(.6)), s.gloss(11, 74, 4, 220, .4), "</g>",
                  Svg.path(overcap, s.cyl("#5A3A2E", .6, .6), 'opacity=".94"'),
                  "".join(Svg.rect(8 + i * 4.4, 5, .8, 52, "#3A2218", extra='opacity=".5"') for i in range(10)),
                  Svg.rect(20, 22, 20, 36, "#C98A6A", extra='opacity=".35"'))
            return s
        if style == "country":
            liquid, pumpc = "#E4EDB0", "#2A3C9E"
        else:
            liquid, pumpc = "#1E8C8C", "#C9B48A"
        s.add(Svg.rect(22, 44, 16, 16, s.cyl("#C0C4CC", 1.2, .9)), Svg.rect(24, 22, 12, 24, s.cyl(pumpc, .8, .6)),
              Svg.rect(21, 18, 18, 8, s.cyl(pumpc, .8, .6), rx=2))
        if style == "country":
            s.add(Svg.path(d, s.cyl(liquid, .4, .7)), cl(s, d),
                  Svg.rect(4, 214, 52, 106, s.grad([(0, "#C5DE7A"), (1, "#7DB43A")], 0, 1)),
                  T(cx, 82, "BATH & BODY WORKS", 3.4, "#1E2A6E", SANS, 700, fit=40),
                  "".join(f'<path d="M{10 + i * 8} 92L{10 + i * 8} 150" stroke="#B7A98A" stroke-width=".6" stroke-dasharray="2.4 2.4"/>' for i in range(6)),
                  T(cx, 170, "COUNTRY", 11, "#1E2A6E", COND, 400, fit=40), T(cx, 184, "CHIC", 11, "#1E2A6E", COND, 400, fit=22),
                  "".join(blossom(x, y, r, "#E0301E", "#3A1A10") for x, y, r in ((14, 204, 5), (34, 198, 6.5), (46, 214, 4.5), (24, 218, 4))),
                  "".join(f'<path d="M{x} {y}L{x} {y + 18}" stroke="#4E7A2A" stroke-width=".7"/>' for x, y in ((14, 208), (34, 204), (46, 218), (24, 221))),
                  f'<circle cx="{cx}" cy="250" r="7" fill="none" stroke="#fff" stroke-width=".6"/>', T(cx, 249, "DERM.", 2.4, "#fff", SANS, 700), T(cx, 252.5, "TESTED", 2.1, "#fff", SANS, 700),
                  T(cx, 272, "FINE FRAGRANCE MIST", 3.6, "#fff", SANS, 800, fit=42), T(cx, 279, "FOR BODY & HAIR", 3, "#fff", SANS, 500),
                  T(cx, 306, "8 FL OZ / 236 mL", 3.2, "#fff", SANS, 500))
        else:
            s.add(Svg.path(d, s.grad([(0, "#1E8C8C"), (.55, "#D9965E"), (1, "#E9B7A0")], 0, 1)), cl(s, d),
                  T(14, 96, "Open", 13, "#0F4F55", SERIF, 700, "start"), T(22, 111, "Sky", 13, "#0F4F55", SERIF, 700, "start"),
                  T(cx, 120, "BY BATH & BODY WORKS", 2.8, "#0F4F55", SANS, 600, fit=38),
                  "".join(f'<path d="M{x} {y}L{x - 6} {y + 24}L{x + 6} {y + 24}Z" fill="{c}"/><path d="M{x} {y + 8}L{x - 7} {y + 30}L{x + 7} {y + 30}Z" fill="{c}"/>'
                          for x, y, c in ((12, 172, "#D7A28C"), (22, 160, "#0F4F55"), (32, 168, "#D7A28C"), (43, 156, "#0F4F55"), (50, 176, "#D7A28C"))),
                  Svg.rect(10, 222, 40, .6, "#0F4F55"), f'<circle cx="{cx}" cy="238" r="7" fill="none" stroke="#0F4F55" stroke-width=".6"/>',
                  T(cx, 237, "DERM.", 2.4, "#0F4F55", SANS, 700), T(cx, 240.5, "TESTED", 2.1, "#0F4F55", SANS, 700),
                  T(cx, 262, "FINE FRAGRANCE MIST", 3.6, "#0F2F33", SANS, 800, fit=42), T(cx, 269, "FOR BODY & HAIR", 3, "#0F2F33", SANS, 500),
                  T(cx, 306, "8 FL OZ / 236 mL", 3.2, "#0F2F33", SANS, 500))
        s.add(Svg.rect(4, 58, 52, 262, s.shade(.5)), s.gloss(11, 72, 4, 230, .55), "</g>",
              Svg.path(overcap, s.cyl("#EEF2F6", .3, .9), 'opacity=".45"'), s.gloss(12, 6, 3, 50, .7))
        return s
    return make


D["BBW-FFM-CC-236"] = bbw_mist("bbwcc", "country")
D["BBW-FFM-OS-236"] = bbw_mist("bbwos", "opensky")
D["BBW-FFM-WM-236"] = bbw_mist("bbwwm", "warm")


def bbw_freshmusk():
    s = Svg("bbwfm", 110, 300)
    top, bot = 44, 300
    d = bottle_d(0, 110, top, bot, 30, 50, 10)
    s.add(Svg.rect(28, 0, 54, 48, s.cyl("#F08A6A", .5, .25), rx=6), Svg.rect(28, 10, 54, 1, mix("#F08A6A", -.2)),
          Svg.path(d, s.cyl("#E9B8CF", .45, .6)), cl(s, d),
          "".join(Svg.rect(6 + i * 7, 60, 1.2, 50, "#fff", extra='opacity=".35"') for i in range(14)),
          "".join(Svg.rect(6 + i * 7, 236, 1.2, 60, "#fff", extra='opacity=".35"') for i in range(14)),
          Svg.rect(0, 112, 110, 120, s.grad([(0, "#F4C1D0"), (1, "#F29A7E")], 0, 1)),
          T(55, 150, "FRESH", 18, "#fff", SANS, 300, fit=74), T(55, 166, "MUSK", 11, "#B8735A", SANS, 800, ls=2),
          T(55, 175, "BY", 4, "#B8735A", SANS, 500), T(55, 183, "BATH & BODY WORKS", 5, "#B8735A", SANS, 700, fit=66),
          T(55, 198, "DERMATOLOGIST TESTED", 3.4, "#fff", SANS, 600), T(55, 208, "BODY WASH", 7, "#fff", SANS, 800, ls=.8),
          T(55, 216, "WITH PRO-VITAMIN B5 + ALOE", 3.4, "#fff", SANS, 500), T(55, 226, "10 FL OZ / 295 mL", 3.8, "#fff", SANS, 500),
          Svg.rect(0, top, 110, bot - top, s.shade(.55)), s.gloss(10, 70, 7, 200, .45), "</g>")
    return s


D["BBW-BW-FM-295"] = bbw_freshmusk


# ================================================================= LUSETA (1 L)
def lz_shell(x, y, c):
    return (f'<g fill="none" stroke="{c}" stroke-width=".8"><path d="M{x - 10} {y + 4}C{x - 10} {y - 8} {x + 10} {y - 8} {x + 10} {y + 4}Z"/>'
            + "".join(f'<path d="M{x} {y + 4}L{x + dx} {y - 5}"/>' for dx in (-7, -3.5, 0, 3.5, 7)) + f'</g><circle cx="{x}" cy="{y + 6}" r="3" fill="{c}"/>')


def lz_feather(x, y, c):
    return (f'<g fill="none" stroke="{c}" stroke-width=".7" transform="rotate(-18 {x} {y})"><path d="M{x} {y + 22}L{x} {y - 20}"/>'
            f'<ellipse cx="{x}" cy="{y - 10}" rx="6" ry="10"/><ellipse cx="{x}" cy="{y - 11}" rx="2.6" ry="4"/>'
            + "".join(f'<path d="M{x} {y + i * 4}L{x - 6} {y + i * 4 - 5}M{x} {y + i * 4}L{x + 6} {y + i * 4 - 5}"/>' for i in range(5)) + "</g>")


def lz_citrus(x, y, c):
    return (f'<g fill="none" stroke="{c}" stroke-width=".8"><circle cx="{x}" cy="{y}" r="10"/><circle cx="{x}" cy="{y}" r="8"/>'
            + "".join(f'<path d="M{x} {y}L{x + 8 * __import__("math").cos(a * .785):.2f} {y + 8 * __import__("math").sin(a * .785):.2f}"/>' for a in range(8)) + "</g>")


def lz_shea(x, y, c):
    return (f'<g fill="none" stroke="{c}" stroke-width=".8"><ellipse cx="{x - 2}" cy="{y + 4}" rx="7" ry="8"/>'
            f'<path d="M{x - 2} {y - 4}C{x + 4} {y - 16} {x + 12} {y - 14} {x + 12} {y - 14}C{x + 8} {y - 6} {x + 2} {y - 4} {x - 2} {y - 4}Z"/>'
            f'<path d="M{x + 6} {y + 8}C{x + 10} {y + 2} {x + 12} {y + 8} {x + 9} {y + 11}C{x + 7} {y + 13} {x + 5} {y + 11} {x + 6} {y + 8}Z"/></g>')


def lz_teatree(x, y, c):
    return (f'<g fill="none" stroke="{c}" stroke-width=".8"><path d="M{x} {y + 16}C{x - 8} {y} {x - 8} {y - 12} {x - 4} {y - 22}C{x - 2} {y - 10} {x - 2} {y + 4} {x} {y + 16}Z"/>'
            f'<path d="M{x + 2} {y + 16}C{x + 10} {y} {x + 12} {y - 10} {x + 8} {y - 20}C{x + 5} {y - 8} {x + 3} {y + 4} {x + 2} {y + 16}Z"/></g>')


def lz_rosemary(x, y, c):
    return (f'<g fill="none" stroke="{c}" stroke-width=".8"><path d="M{x} {y + 18}L{x + 2} {y - 18}"/>'
            + "".join(f'<path d="M{x + i * .1:.1f} {y + 14 - i * 5}l-6 -4M{x + i * .1 + .3:.1f} {y + 12 - i * 5}l6 -4"/>' for i in range(7)) + "</g>")


def lz_palm(x, y, c):
    return (f'<path d="M{x} {y + 16}C{x + 1} {y + 6} {x + 1} {y - 2} {x + 2} {y - 6}" stroke="{c}" stroke-width="1.6" fill="none"/>'
            + "".join(leaf(x + 2, y - 6, 11, r, c) for r in (-160, -120, -60, -20, -90)) + f'<path d="M{x + 6} {y + 16}A5 5 0 0 1 {x + 16} {y + 16}Z" fill="none" stroke="{c}" stroke-width=".8"/>')


def lz_drop(x, y, c):
    return (f'<g fill="none" stroke="{c}" stroke-width=".8"><path d="M{x} {y - 14}C{x + 8} {y - 2} {x + 9} {y + 3} {x + 9} {y + 6}A9 9 0 0 1 {x - 9} {y + 6}C{x - 9} {y + 3} {x - 8} {y - 2} {x} {y - 14}Z"/>'
            + "".join(f'<path d="M{x + dx - 3} {y + dy}l1.5 -2.6h3l1.5 2.6l-1.5 2.6h-3z"/>' for dx, dy in ((0, 6), (5.5, 3), (-5.5, 3))) + "</g>")


def lz_lavender(x, y, c):
    return (f'<g stroke="{c}" stroke-width=".8" fill="none"><path d="M{x} {y + 18}L{x - 2} {y - 18}M{x + 1} {y + 18}L{x + 7} {y - 12}"/></g>'
            + "".join(f'<ellipse cx="{x - 2 + i * -.1:.1f}" cy="{y - 16 + i * 4}" rx="1.4" ry="2" fill="none" stroke="{c}" stroke-width=".6"/>' for i in range(6))
            + "".join(f'<ellipse cx="{x + 7 - i * .6:.1f}" cy="{y - 10 + i * 4}" rx="1.3" ry="1.8" fill="none" stroke="{c}" stroke-width=".6"/>' for i in range(4)))


def lz_peptide(x, y, c):
    pts = ((-8, 6), (-3, -2), (4, 2), (8, -7), (2, -12), (-6, -10))
    return (f'<polyline points="{" ".join(f"{x + a},{y + b}" for a, b in pts)}" fill="none" stroke="{c}" stroke-width=".8"/>'
            + "".join(f'<circle cx="{x + a}" cy="{y + b}" r="2.2" fill="none" stroke="{c}" stroke-width=".8"/>' for a, b in pts))


def luseta_label(s, x0, w, y, ink, med_fill, med_ink, name, serif, kind, trans, benefit, claims, fortxt, icon, icon_col=None):
    x = x0 + w * .16
    out = [f'<circle cx="{x + 9}" cy="{y}" r="9" fill="{med_fill}"/>', T(x + 9, y + 4.5, "L", 13, med_ink, SCRIPT, 700),
           T(x, y + 19, "LUSETA", 6.6, ink, SERIF, 400, "start", ls=2.2, fit=38), T(x + 40, y + 16, "®", 3, ink, SANS, 400, "start")]
    yy = y + 36
    for ln in name:
        out.append(T(x, yy, ln, 8.6, ink, SERIF if serif else SANS, 700, "start", fit=min(len(ln) * 6, w * .66)))
        yy += 9.6
    out.append(T(x, yy + 1, kind, 6, ink, SANS, 700, "start", fit=min(len(kind) * 4.1, w * .7)))
    yy += 8
    for ln in trans:
        out.append(T(x, yy, ln, 4.2, ink, SANS, 400, "start", fit=min(len(ln) * 2.75, w * .66)))
        yy += 5.2
    yy += 3
    for ln in benefit:
        out.append(T(x, yy, ln, 4.4, ink, SERIF, 400, "start", style="italic", fit=min(len(ln) * 2.2, w * .52)))
        yy += 5.4
    yy += 3
    for ln in claims:
        out.append(T(x, yy, ln, 3.9, ink, SANS, 700, "start", style="italic"))
        yy += 4.9
    out.append(T(x, yy + 2, fortxt, 3.9, ink, SERIF, 400, "start", style="italic"))
    out.append(T(x, yy + 12, "33.8 FL.OZ. - 1 L℮", 4.2, ink, SANS, 400, "start"))
    out.append(icon(x0 + w * .78, y + 104, icon_col or ink))
    return out


HAIR_CLAIMS = ("COLOR SAFE", "FREE OF SULFATES", "PARABENS & GLUTEN")
BODY_CLAIMS = ("FREE OF SULFATES", "PARABENS & GLUTEN")


def luseta_round(s, x0, body, ink, med, med_ink, lab, clear=False):
    w, top, bot = 84, 64, 290
    d = bottle_d(x0, w, top, bot, 34, 30, 10)
    s.add(*pump(s, x0 + 42, top + 2, "#151515", head_w=30, stem=12, nozzle=30, left=True, collar_w=30, collar_h=16))
    if clear:
        s.add(Svg.path(d, s.cyl(body, .5, .8), 'opacity=".95"'))
    else:
        s.add(Svg.path(d, s.cyl(body, .55, .45)))
    s.add(cl(s, d), *luseta_label(s, x0, w, 142, ink, med, med_ink, *lab),
          Svg.rect(x0, top, w, bot - top, s.shade(.6)), s.gloss(x0 + 11, top + 30, 6, 180, .5 if clear else .35), "</g>")


def luseta_rect(s, x0, body, ink, med, med_ink, lab):
    w, top, bot = 110, 60, 280
    d = f"M{x0 + 38} {top}L{x0 + 72} {top}L{x0 + 96} {top + 2}Q{x0 + 110} {top + 4} {x0 + 110} {top + 18}L{x0 + 110} {bot - 14}Q{x0 + 110} {bot} {x0 + 96} {bot}L{x0 + 14} {bot}Q{x0} {bot} {x0} {bot - 14}L{x0} {top + 18}Q{x0} {top + 4} {x0 + 14} {top + 2}Z"
    s.add(*pump(s, x0 + 55, top + 2, "#151515", head_w=30, stem=12, nozzle=30, left=True, collar_w=30, collar_h=16))
    s.add(Svg.path(d, s.grad([(0, mix(body, -.25)), (.12, body), (.3, mix(body, .25)), (.5, body), (.88, mix(body, -.1)), (1, mix(body, -.3))])),
          cl(s, d), Svg.rect(x0 + 53, top, 4, bot - top - 6, mix(body, -.18), extra='opacity=".6"'),
          *luseta_label(s, x0 + 8, w - 8, 130, ink, med, med_ink, *lab),
          s.gloss(x0 + 9, top + 20, 6, 190, .55), "</g>")


def luseta(sku, fmt, body, ink, med, med_ink, lab, clear=False, duo=None):
    def make():
        if duo:
            s = Svg(sku, 176, 290)
            luseta_round(s, 0, body, ink, med, med_ink, lab, clear)
            lab2 = (lab[0], lab[1], "CONDITIONER", ("CONDITIONNEUR", "ACONDICIONADOR")) + lab[4:]
            luseta_round(s, 92, body, ink, med, med_ink, lab2, clear)
            return s
        if fmt == "rect":
            s = Svg(sku, 110, 280)
            luseta_rect(s, 0, body, ink, med, med_ink, lab)
        else:
            s = Svg(sku, 84, 290)
            luseta_round(s, 0, body, ink, med, med_ink, lab, clear)
        return s
    return make


SH_T, BW_T = ("SHAMPOOING", "CHAMPÚ"), ("GEL DOUCHE", "GEL DE DUCHA")
L = {
    "LUS-GP-DUO-1L": ("round", "#EDE7E2", "#D6187F", "#D6187F", "#F8E6EF", (["GLOSSY", "PEARL"], False, "SHAMPOO", SH_T, ("Smooth Frizziness", "& Add Shine"), HAIR_CLAIMS, "For all hair types", lz_shell), False, True),
    "LUS-KER-DUO-1L": ("round", "#E8354F", "#FFFFFF", "#FFFFFF", "#E8354F", (["KERATIN"], True, "SHAMPOO", SH_T, ("Smoothing &", "Nourishing Formula"), HAIR_CLAIMS, "For damaged & dry hair", lz_feather), False, True),
    "LUS-CC-BW-1L": ("round", "#F59A1E", "#FFFFFF", "#FFFFFF", "#F59A1E", (["CITRUS &", "COLLAGEN"], False, "BODY WASH", BW_T, ("Energizing &", "Hydrating Formula"), BODY_CLAIMS, "For all skin types", lz_citrus), True, False),
    "LUS-SA-BW-1L": ("round", "#F5A914", "#FFFFFF", "#FFFFFF", "#F5A914", (["SHEA BUTTER", "& ARGAN OIL"], False, "BODY WASH", BW_T, ("Hydrating &", "Moisturizing Formula"), BODY_CLAIMS, "For all skin types", lz_shea), True, False),
    "LUS-TTA-SH-1L": ("round", "#2A4F26", "#FFFFFF", "#FFFFFF", "#2A4F26", (["TEA TREE &", "ARGAN OIL"], False, "SHAMPOO", SH_T, ("Clarify &", "Repair Formula"), HAIR_CLAIMS, "For damaged & oily hair", lz_teatree), False, False),
    "LUS-RMC-SH-1L": ("round", "#A9CBA6", "#262626", "#262626", "#DCEBD9", (["ROSEMARY", "MINT COMPLEX"], False, "STRENGTHENING SHAMPOO", ("SHAMPOOING FORTIFIANT", "CHAMPÚ FORTALECEDOR"), ("Infused with Rosemary,", "Peppermint, Biotin & Argan Oil"), HAIR_CLAIMS, "For all hair types", lz_rosemary), False, False),
    "LUS-CM-BW-1L": ("round", "#7FD3CF", "#1B8DC8", "#1B8DC8", "#E6F6FB", (["COCONUT", "MILK"], True, "BODY WASH", BW_T, ("Nourishing &", "Moisturizing Formula"), BODY_CLAIMS, "For all skin types", lz_palm), True, False),
    "LUS-HA-BW-1L": ("rect", "#1E8FC7", "#FFFFFF", "#FFFFFF", "#1E8FC7", (["HYALURONIC", "ACID"], False, "BODY WASH", BW_T, ("Hydrating &", "Smoothing Formula"), BODY_CLAIMS, "For all skin types", lz_drop), True, False),
    "LUS-LC-BW-1L": ("round", "#3B20A0", "#FFFFFF", "#FFFFFF", "#3B20A0", (["LAVENDER", "& COLLAGEN"], False, "BODY WASH", BW_T, ("Soothing &", "Hydrating Formula"), BODY_CLAIMS, "For all skin types", lz_lavender), True, False),
    "LUS-CP-BW-1L": ("rect", "#1BB3A0", "#FFFFFF", "#FFFFFF", "#1BB3A0", (["COLLAGEN", "PEPTIDES"], False, "BODY WASH", BW_T, ("Rejuvenating &", "Hydrating Formula"), BODY_CLAIMS, "For all skin types", lz_peptide), True, False),
}
for _k, (fmt, body, ink, med, med_ink, lab, clear, duo) in L.items():
    D[_k] = luseta(_k.lower(), fmt, body, ink, med, med_ink, lab, clear, duo)


# ================================================================= BYPHASSE
def byphasse():
    s = Svg("byp", 100, 300)
    top, bot = 70, 300
    d = bottle_d(0, 100, top, bot, 14, 34, 10, square=1)
    ink = "#2F3A48"
    s.add(Svg.rect(33, top - 24, 34, 26, s.cyl("#F2F2F2", .5), rx=3), Svg.rect(46, top - 42, 8, 18, s.cyl("#EDEDED", .5)),
          Svg.rect(36, top - 54, 30, 13, s.cyl("#F4F4F4", .5), rx=3), Svg.rect(8, top - 51, 32, 6, s.grad([(0, "#fff"), (1, "#D5D5D5")], 0, 1), rx=3),
          Svg.path(d, s.cyl("#FBB117", .45, .9)), cl(s, d),
          Svg.rect(15, 100, 70, 186, "#FFE7A8", rx=8, extra='opacity=".45"'),
          T(50, 110, "SOIN DU CORPS", 3.2, ink, SANS, 500, ls=1.2), T(50, 121, "BYPHASSE", 8, ink, SANS, 300, ls=1.4),
          f'<path d="M36 124C44 128 56 128 64 123" stroke="#27407A" stroke-width="1.2" fill="none"/>',
          T(50, 139, "GEL DOUCHE", 10, ink, COND, 800, fit=56), T(50, 150, "DERMO", 10, ink, COND, 800), T(50, 159, "MICELLAIRE", 7, ink, SANS, 400),
          '<ellipse cx="48" cy="183" rx="11" ry="13" fill="#F28C1A"/><ellipse cx="45" cy="179" rx="4" ry="5" fill="#fff" opacity=".7"/>',
          leaf(58, 176, 16, -35, "#5E8C2E"), leaf(38, 172, 14, -150, "#6E9C36"),
          T(50, 209, "ARGAN", 11, "#E67E0E", SANS, 800, extra='stroke="#fff" stroke-width=".6" paint-order="stroke"'), Svg.rect(30, 212, 40, 1.4, "#fff"),
          T(50, 222, "Formulé avec des tensioactifs émollients", 3.2, ink, SANS, 400), T(50, 226.5, "et des agents hydratants", 3.2, ink, SANS, 400),
          T(50, 233, "Huile d'argan · pH neutre", 3.6, ink, SANS, 700), T(50, 238, "Tous types de peaux", 3.2, ink, SANS, 400),
          T(50, 246, "Dermo micellar shower gel argan", 3.2, ink, SANS, 400), T(50, 250.5, "All skin types", 3.2, ink, SANS, 400),
          T(50, 270, "1 L℮ (33.8 fl.oz.)", 4.2, ink, SANS, 700),
          Svg.rect(0, top, 100, bot - top, s.shade(.5)), s.gloss(10, 90, 6, 190, .6), "</g>")
    return s


D["BYP-SG-ARG-1L"] = byphasse


# ================================================================= CIROA
def ciroa():
    s = Svg("cir", 104, 276)
    top, bot = 40, 276
    d = f"M30 {top}L74 {top}L96 {top + 4}Q104 {top + 6} 104 {top + 14}L104 {bot - 7}Q104 {bot} 97 {bot}L7 {bot}Q0 {bot} 0 {bot - 7}L0 {top + 14}Q0 {top + 6} 8 {top + 4}Z"
    m = "#C9A048"
    s.add(Svg.rect(34, top - 16, 36, 18, s.cyl(m, .6), rx=2), Svg.rect(47, top - 30, 10, 15, s.cyl(m, .6)),
          Svg.rect(36, top - 40, 34, 12, s.cyl(m, .6), rx=2), Svg.rect(64, top - 38, 26, 8, s.grad([(0, mix(m, .15)), (1, mix(m, -.2))], 0, 1)),
          Svg.path(d, s.grad([(0, mix("#C9A865", -.3)), (.15, "#C9A865"), (.35, mix("#C9A865", .3)), (.6, "#C9A865"), (1, mix("#C9A865", -.35))])),
          cl(s, d),
          f'<path d="M14 150C30 136 60 170 90 150" stroke="#F4E6C2" stroke-width="3" fill="none" opacity=".35"/>',
          f'<path d="M10 190C36 176 62 206 96 186" stroke="#F4E6C2" stroke-width="2" fill="none" opacity=".3"/>',
          f'<g transform="translate(66 196) rotate(-90)">' + T(0, 0, "ciroa", 44, "#fff", ROUND, 400, "start", fit=146,
                                                                extra='fill-opacity=".22" stroke="#fff" stroke-opacity=".45" stroke-width=".8"') + "</g>",
          T(52, 214, "vanilla", 12, "#fff", SERIF, 700, style="italic"), T(52, 225, "-icious", 12, "#fff", SERIF, 700, style="italic"),
          T(52, 235, "SHOWER GEL", 5, "#fff", SANS, 300, ls=.8), T(52, 242, "VANILLA, BROWN SUGAR", 3.6, "#fff", SANS, 500),
          T(52, 246.5, "& AMBER", 3.6, "#fff", SANS, 500), T(52, 254, "AUSTRALIAN OWNED", 3.2, "#fff", SANS, 500),
          T(52, 262, "1,000 ML ℮/33.8 FL OZ", 3.8, "#fff", SANS, 800),
          s.gloss(8, 60, 6, 190, .45), "</g>")
    return s


D["CIR-VI-SG-1L"] = ciroa


# ================================================================= MICHAEL KORS handbags (from photos of our own stock)
GOLD_HW, SILVER_HW = "#C9A55A", "#C3C8CF"


def saffiano(s, c):
    """Fine cross-hatched grain of saffiano leather."""
    i = s.nid("p")
    s.defs.append(f'<pattern id="{i}" width="3" height="3" patternUnits="userSpaceOnUse" patternTransform="rotate(35)">'
                  f'<path d="M0 0L0 3M0 0L3 0" stroke="{mix(c, .16 if c < "#80" else -.1)}" stroke-width=".35" opacity=".55"/></pattern>')
    return f"url(#{i})"


def hw(s, c):
    return s.grad([(0, mix(c, -.35)), (.35, mix(c, .45)), (.6, c), (1, mix(c, -.4))], 1, 1)


def tab(x, y, w, h, fill, edge):
    """Pointed leather handle tab."""
    return (f'<path d="M{x - w / 2} {y}L{x + w / 2} {y}L{x + w / 2} {y + h * .7}L{x} {y + h}L{x - w / 2} {y + h * .7}Z" fill="{fill}" stroke="{edge}" stroke-width=".6"/>'
            f'<path d="M{x - w / 2 + 2} {y + 1}L{x - w / 2 + 2} {y + h * .68}L{x} {y + h - 2.5}L{x + w / 2 - 2} {y + h * .68}L{x + w / 2 - 2} {y + 1}" fill="none" stroke="{edge}" stroke-width=".4" stroke-dasharray="1.2 1"/>')


def mk_satchel(sku, c, metal, w=240, h=250):
    def make():
        s = Svg(sku, w, h)
        top, bot = h - 150, h
        L, R = 18, w - 18
        edge, dark = mix(c, -.28), mix(c, -.16)
        m = hw(s, metal)
        # back panel + side wings, then handles, then front
        s.add(Svg.path(f"M{L + 6} {top - 14}L{R - 6} {top - 14}L{R - 6} {top + 10}L{L + 6} {top + 10}Z", mix(c, -.1)),
              Svg.path(f"M{L} {top - 4}L{L - 16} {top - 12}L{L - 6} {bot - 10}L{L + 4} {bot}Z", s.grad([(0, mix(c, -.3)), (1, dark)])),
              Svg.path(f"M{R} {top - 4}L{R + 16} {top - 12}L{R + 6} {bot - 10}L{R - 4} {bot}Z", s.grad([(0, dark), (1, mix(c, -.3))])),
              Svg.rect(L + 8, top - 10, R - L - 16, 4, m, rx=1))
        for off, o in ((10, .75), (0, 1)):
            hx1, hx2 = L + 40 + off, R - 40 + off
            s.add(f'<path d="M{hx1} {top + 8}C{hx1} {top - 118} {hx2} {top - 118} {hx2} {top + 8}" fill="none" stroke="{mix(c, -.2 if off else 0)}" stroke-width="11" stroke-linecap="round" opacity="{o}"/>',
                  f'<path d="M{hx1 - 2} {top + 4}C{hx1 - 2} {top - 110} {hx2 + 2} {top - 110} {hx2 + 2} {top + 4}" fill="none" stroke="#fff" stroke-width="1.4" opacity=".18"/>')
        front = f"M{L} {top}L{R} {top}L{R} {bot - 8}Q{R} {bot} {R - 8} {bot}L{L + 8} {bot}Q{L} {bot} {L} {bot - 8}Z"
        s.add(Svg.path(front, c), Svg.path(front, saffiano(s, c)), Svg.path(front, s.shade(.35)),
              f'<path d="{front}" fill="none" stroke="{edge}" stroke-width="1"/>',
              f'<rect x="{L + 4}" y="{top + 4}" width="{R - L - 8}" height="{bot - top - 8}" rx="6" fill="none" stroke="{edge}" stroke-width=".5" stroke-dasharray="1.6 1.2"/>')
        for x in (L + 40, R - 40):
            s.add(f'<circle cx="{x}" cy="{top + 4}" r="6.5" fill="none" stroke="{m}" stroke-width="2.4"/>',
                  Svg.rect(x - 5, top + 9, 10, 5, m, rx=1.5), tab(x, top + 13, 20, 40, c, edge))
        s.add(T(w / 2, top + 34, "MICHAEL KORS", 9, m, SANS, 500, ls=1.2, fit=70))
        return s
    return make


def mk_greenwich(sku, c, metal):
    def make():
        s = Svg(sku, 230, 230)
        top, bot, L, R = 70, 230, 20, 210
        edge = mix(c, .22)
        m = hw(s, metal)
        s.add(f'<path d="M{L + 10} {top + 8}C{L - 10} {top - 80} {R + 10} {top - 80} {R - 10} {top + 8}" fill="none" stroke="{mix(c, .1)}" stroke-width="7"/>')
        for x in (L + 10, R - 10):
            s.add(f'<circle cx="{x}" cy="{top + 8}" r="6" fill="none" stroke="{m}" stroke-width="2.6"/>')
        body = f"M{L} {top + 10}L{R} {top + 10}L{R} {bot - 6}Q{R} {bot} {R - 6} {bot}L{L + 6} {bot}Q{L} {bot} {L} {bot - 6}Z"
        flap = f"M{L - 2} {top + 4}Q{L - 2} {top} {L + 6} {top}L{R - 6} {top}Q{R + 2} {top} {R + 2} {top + 4}L{R + 2} {top + 104}C{R - 40} {top + 118} {L + 40} {top + 118} {L - 2} {top + 104}Z"
        s.add(Svg.path(body, c), Svg.path(body, saffiano(s, c)), Svg.path(body, s.shade(.3)),
              Svg.path(flap, mix(c, .03)), Svg.path(flap, saffiano(s, c)),
              f'<path d="{flap}" fill="none" stroke="{edge}" stroke-width=".8"/>',
              Svg.path(f"M{L - 2} {top + 104}C{L + 40} {top + 118} {R - 40} {top + 118} {R + 2} {top + 104}", "none", f'stroke="#000" stroke-width="2" opacity=".35"'),
              Svg.rect(104, top - 2, 22, 146, mix(c, .05), rx=3, extra=f'stroke="{edge}" stroke-width=".6"'),
              f'<path d="M104 {top + 140}L126 {top + 140}L126 {top + 146}Q115 {top + 152} 104 {top + 146}Z" fill="{mix(c, .05)}" stroke="{edge}" stroke-width=".6"/>',
              f'<circle cx="115" cy="{top + 100}" r="17" fill="{m}"/><circle cx="115" cy="{top + 100}" r="13" fill="{mix(c, .05)}"/>',
              T(115, top + 105.5, "MK", 14, m, SANS, 800, fit=21))
        return s
    return make


def mk_tote(sku, c, metal):
    def make():
        s = Svg(sku, 250, 300)
        top, bot = 130, 300
        L, R = 22, 228
        edge, dark = mix(c, .2), mix(c, .08)
        m = hw(s, metal)
        for x1, x2, o in ((70, 170, .7), (82, 182, 1)):
            s.add(f'<path d="M{x1} {top + 40}C{x1 - 10} {top - 170} {x2 + 10} {top - 170} {x2} {top + 40}" fill="none" stroke="{mix(c, .06 if o < 1 else .12)}" stroke-width="6.5" opacity="{o}"/>')
        s.add(Svg.path(f"M{L - 10} {top + 26}L{L + 8} {top + 20}L{L + 14} {bot}L{L - 2} {bot - 8}Z", dark),
              Svg.path(f"M{R + 10} {top + 26}L{R - 8} {top + 20}L{R - 14} {bot}L{R + 2} {bot - 8}Z", dark))
        body = f"M{L} {top}L{R} {top}L{R - 12} {bot - 6}Q{R - 13} {bot} {R - 19} {bot}L{L + 19} {bot}Q{L + 13} {bot} {L + 12} {bot - 6}Z"
        s.add(Svg.path(body, c), Svg.path(body, saffiano(s, c)), Svg.path(body, s.shade(.3)),
              f'<path d="{body}" fill="none" stroke="{edge}" stroke-width=".8"/>',
              Svg.rect(L, top - 2, R - L, 4, m, rx=1), Svg.rect(L - 4, top - 4, 16, 6, m, rx=2),
              f'<path d="M{L + 44} {top + 20}L{L + 38} {bot - 8}M{R - 44} {top + 20}L{R - 38} {bot - 8}" stroke="{edge}" stroke-width=".7"/>')
        for x in (82, 182):
            s.add(tab(x, top + 34, 13, 34, c, edge))
        s.add(T(125, top + 26, "MICHAEL KORS", 8, m, SANS, 500, ls=1.2, fit=64),
              f'<path d="M82 {top + 50}L76 {top + 120}" stroke="{mix(c, .1)}" stroke-width="2.4"/>',
              f'<circle cx="76" cy="{top + 132}" r="12" fill="{m}"/><circle cx="76" cy="{top + 132}" r="9" fill="{mix(c, .05)}"/>',
              T(76, top + 136, "MK", 9, m, SANS, 800, fit=13))
        return s
    return make


D["MK-MAR-SAT-BLS-G"] = mk_satchel("mkbls", "#E3C4C5", GOLD_HW)
D["MK-GRW-XB-BLK-S"] = mk_greenwich("mkgrw", "#1B1B1E", SILVER_HW)
D["MK-MAR-SAT-BLK-S"] = mk_satchel("mksatS", "#1B1B1E", SILVER_HW)
D["MK-MAR-SAT-BLK-G"] = mk_satchel("mksatG", "#1B1B1E", GOLD_HW)
D["MK-MAR-TOT-BLK-S"] = mk_tote("mktot", "#1B1B1E", SILVER_HW)
