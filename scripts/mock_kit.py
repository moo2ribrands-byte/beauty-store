# Drawing kit for the product mockups (see mockups.py).
# Each design draws in its own units with the base of the pack at y = H; the page scales it to fit.
import html

SANS = "'Helvetica Neue',Helvetica,Arial,Roboto,sans-serif"
SERIF = "Georgia,'Times New Roman','Noto Serif',serif"
DIDOT = "Didot,'Bodoni 72','Bodoni MT',Georgia,serif"
COND = "'Arial Narrow','Helvetica Neue',Arial,sans-serif"
SCRIPT = "'Snell Roundhand','Brush Script MT','Segoe Script',cursive"
ROUND = "'Arial Rounded MT Bold','Varela Round','Helvetica Neue',Arial,sans-serif"


def _rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def mix(h, k):
    """k > 0 lightens toward white, k < 0 darkens toward black."""
    r = _rgb(h)
    t = 255 if k > 0 else 0
    k = abs(k)
    return "#%02x%02x%02x" % tuple(round(c + (t - c) * k) for c in r)


def esc(s):
    return html.escape(str(s), quote=True)


class Svg:
    def __init__(self, uid, w, h):
        self.uid, self.w, self.h = uid, w, h
        self.defs, self.body, self.n = [], [], 0

    def nid(self, p="g"):
        self.n += 1
        return f"{self.uid}{p}{self.n}"

    def add(self, *parts):
        self.body.extend(parts)
        return self

    # ---------- paints ----------
    def grad(self, stops, x2=1, y2=0, x1=0, y1=0):
        i = self.nid()
        s = "".join(
            f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{a}"' if a != 1 else "") + "/>"
            for o, c, a in ((st + (1,))[:3] for st in stops))
        self.defs.append(f'<linearGradient id="{i}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient>')
        return f"url(#{i})"

    def cyl(self, c, k=1.0, gloss=0.45):
        """Horizontal shading that makes a flat shape read as a round bottle."""
        return self.grad([(0, mix(c, -.34 * k)), (.08, mix(c, -.14 * k)), (.27, mix(c, gloss * .55 * k)),
                          (.36, mix(c, gloss * .75 * k)), (.5, c), (.8, mix(c, -.08 * k)),
                          (.94, mix(c, -.24 * k)), (1, mix(c, -.4 * k))])

    def shade(self, k=1.0):
        """Transparent overlay for labels/prints so they curve with the bottle."""
        return self.grad([(0, "#000", .32 * k), (.1, "#000", .1 * k), (.3, "#fff", .16 * k), (.38, "#fff", .1 * k),
                          (.55, "#000", 0), (.85, "#000", .1 * k), (1, "#000", .36 * k)])

    def clip(self, inner):
        i = self.nid("c")
        self.defs.append(f'<clipPath id="{i}">{inner}</clipPath>')
        return f"url(#{i})"

    # ---------- primitives ----------
    @staticmethod
    def rect(x, y, w, h, fill, rx=0, extra=""):
        return f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}"' + (f' rx="{rx:g}"' if rx else "") + f' fill="{fill}" {extra}/>'

    @staticmethod
    def path(d, fill, extra=""):
        return f'<path d="{d}" fill="{fill}" {extra}/>'

    @staticmethod
    def text(x, y, s, size, fill, family=SANS, weight=400, anchor="middle", ls=0, style="", fit=None, extra=""):
        """fit = exact width in units (textLength) so lines look the same whatever font the phone has."""
        a = f' textLength="{fit:g}" lengthAdjust="spacingAndGlyphs"' if fit else ""
        st = f' font-style="{style}"' if style else ""
        l = f' letter-spacing="{ls:g}"' if ls else ""
        return (f'<text x="{x:g}" y="{y:g}" font-family="{family}" font-size="{size:g}" font-weight="{weight}" '
                f'fill="{fill}" text-anchor="{anchor}"{l}{st}{a} {extra}>{esc(s)}</text>')

    def gloss(self, x, y, w, h, o=.45):
        """Soft vertical specular streak."""
        f = self.grad([(0, "#fff", 0), (.5, "#fff", o), (1, "#fff", 0)])
        return self.rect(x, y, w, h, f, rx=w / 2)

    def svg(self, pad=2):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-pad} {self.w + 2 * pad:g} {self.h + 2 * pad:g}">'
                f'<defs>{"".join(self.defs)}</defs>{"".join(self.body)}</svg>')


# ---------- common pack parts ----------
def bottle_d(x, w, top, bottom, shoulder, neck_w, r=6, square=0.0):
    """Rounded-shoulder bottle outline from the neck (top) to the base. square=0 dome shoulder, 1 flat shoulder."""
    L, R, cx = x, x + w, x + w / 2
    nl, nr = cx - neck_w / 2, cx + neck_w / 2
    sy = top + shoulder
    k = .55 + .4 * square
    return (f"M{nl:g} {top:g}L{nr:g} {top:g}"
            f"C{nr + (R - nr) * k:g} {top:g} {R:g} {top + shoulder * (1 - k):g} {R:g} {sy:g}"
            f"L{R:g} {bottom - r:g}Q{R:g} {bottom:g} {R - r:g} {bottom:g}L{L + r:g} {bottom:g}Q{L:g} {bottom:g} {L:g} {bottom - r:g}"
            f"L{L:g} {sy:g}C{L:g} {top + shoulder * (1 - k):g} {nl - (nl - L) * k:g} {top:g} {nl:g} {top:g}Z")


def pump(s, cx, y, col, head_w=34, stem=16, nozzle=26, left=True, collar_w=30, collar_h=14, metal=False, head_h=12):
    """Pump sitting on a neck whose top is at y. Returns svg parts; head top ends near y - collar_h - stem - head_h."""
    k = 1.3 if metal else .9
    g = s.cyl(col, k, gloss=.9 if metal else .5)
    cy = y - collar_h
    out = [s.rect(cx - collar_w / 2, cy, collar_w, collar_h + 2, g, rx=3)]
    out += [s.rect(cx - collar_w / 2 + 1, cy + i, collar_w - 2, .8, mix(col, -.3), extra='opacity=".5"') for i in range(3, int(collar_h), 3)]
    out.append(s.rect(cx - 4, cy - stem, 8, stem, s.cyl(col, k)))
    hy = cy - stem - head_h
    out.append(s.rect(cx - head_w / 2, hy, head_w, head_h, g, rx=head_h / 3))
    nx = cx - head_w / 2 - nozzle + 6 if left else cx + head_w / 2 - 6
    out.append(s.rect(nx, hy + 2, nozzle, 6, s.grad([(0, mix(col, .15)), (1, mix(col, -.25))], x2=0, y2=1), rx=3))
    return out


def shadow(s, cx, y, rx, ry=None):
    f = s.nid("s")
    s.defs.append(f'<radialGradient id="{f}"><stop offset="0" stop-color="#000" stop-opacity=".3"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>')
    return f'<ellipse cx="{cx:g}" cy="{y:g}" rx="{rx:g}" ry="{ry or rx * .09:g}" fill="url(#{f})"/>'
