"""Hey Atu glyph geometry. Single source for every logo, icon and state file.

Units: master units (the 03 v2 build).
v2.0 (2026-10-13): the glyph is the product-approved hand-drawn dog, smoothed (version A).
Head, ears, eye patch and eyes are smooth closed curves stored in glyph_shapes.json.
Each part is still a separate shape layered as before (head, patch clipped to head,
right ear, left ear, eyes); no fillets at the joins; strokes and gaps grow outward.
HEAD / LEAR / REAR / PATCH / EYES remain tuples (cx, cy, w, h, angle_deg) fitted to each
shape for layout and guides; the drawing functions use the exact curve via `.poly`.
Plain tuples (e.g. derived state eyes) are still drawn as ellipses.
"""
import math
from shapely.geometry import Point, Polygon, MultiPolygon, LineString
from shapely import affinity
from shapely.ops import unary_union

import json as _json, os as _os


class Shape(tuple):
    """(cx, cy, w, h, angle) fitted ellipse + exact smooth polygon in .poly"""
    def __new__(cls, pts):
        poly = Polygon(pts).buffer(0)
        import numpy as _np
        a = _np.array(poly.exterior.coords)[:-1]
        c = a.mean(0); cov = _np.cov((a - c).T); w_, v_ = _np.linalg.eigh(cov)
        ang = math.degrees(math.atan2(v_[1, 0], v_[0, 0]))
        u = (a - c) @ v_[:, 0]; t = (a - c) @ v_[:, 1]
        cx, cy = poly.centroid.x, poly.centroid.y
        obj = super().__new__(cls, (cx, cy, float(u.max() - u.min()), float(t.max() - t.min()), ang))
        obj.poly = poly
        return obj


_G = _json.load(open(_os.path.join(_os.path.dirname(__file__), 'glyph_shapes.json')))
HEAD = Shape(_G['head'])
LEAR = Shape(_G['lear'])
REAR = Shape(_G['rear'])
PATCH = Shape(_G['patch'])
EYES = [Shape(e) for e in _G['eyes']]
COLOR_SIL = Polygon(_G['color_silhouette']).buffer(0)     # version A colour mark: caramel silhouette
COLOR_WHITE = Polygon(_G['color_white']).buffer(0)     # version A colour mark: white face

CARAMEL = "#D9803A"
INK = "#0E0E10"
WHITE = "#FFFFFF"
STROKE = 14.5          # sticker silhouette outline (outside), master units  (= version A)
EAR_LINE = 8.7         # ear line, grows outward, master units  (= version A)


def ellipse_d(e, grow=0.0):
    if hasattr(e, 'poly'):
        return poly_d(ellipse_poly(e, grow))
    cx, cy, w, h, a = e
    rx, ry = w / 2 + grow, h / 2 + grow
    t = math.radians(a)
    dx, dy = rx * math.cos(t), rx * math.sin(t)
    p1 = (cx + dx, cy + dy)
    p2 = (cx - dx, cy - dy)
    f = lambda v: f"{v:.2f}"
    return (f"M{f(p1[0])} {f(p1[1])}A{f(rx)} {f(ry)} {f(a)} 1 1 {f(p2[0])} {f(p2[1])}"
            f"A{f(rx)} {f(ry)} {f(a)} 1 1 {f(p1[0])} {f(p1[1])}Z")


def ellipse_poly(e, grow=0.0, n=256):
    if hasattr(e, 'poly'):
        return e.poly.buffer(grow, quad_segs=32, join_style='round') if grow else e.poly
    cx, cy, w, h, a = e
    c = Point(0, 0).buffer(1, quad_segs=n)
    c = affinity.scale(c, w / 2 + grow, h / 2 + grow)
    c = affinity.rotate(c, a, origin=(0, 0))
    return affinity.translate(c, cx, cy)


def ellipse_bbox(e, grow=0.0):
    if hasattr(e, 'poly'):
        return ellipse_poly(e, grow).bounds
    cx, cy, w, h, a = e
    rx, ry, t = w / 2 + grow, h / 2 + grow, math.radians(a)
    ex = math.sqrt((rx * math.cos(t)) ** 2 + (ry * math.sin(t)) ** 2)
    ey = math.sqrt((rx * math.sin(t)) ** 2 + (ry * math.cos(t)) ** 2)
    return cx - ex, cy - ey, cx + ex, cy + ey


def bbox(grow=0.0):
    bs = [ellipse_bbox(e, grow) for e in (HEAD, LEAR, REAR)]
    return min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs)


def poly_d(geom):
    """Shapely (Multi)Polygon -> SVG path data, evenodd."""
    polys = geom.geoms if isinstance(geom, MultiPolygon) else [geom]
    out = []
    for p in polys:
        for ring in [p.exterior, *p.interiors]:
            cs = list(ring.coords)
            out.append("M" + "L".join(f"{x:.2f} {y:.2f}" for x, y in cs[:-1]) + "Z")
    return "".join(out)


# ---------- shapes built with booleans (mono / line / notification) ----------
def mono_shape(gap=17.4, eyes=True):
    head, lear, rear = ellipse_poly(HEAD), ellipse_poly(LEAR), ellipse_poly(REAR)
    head2 = head.difference(lear.buffer(gap)).difference(rear.buffer(gap))
    g = unary_union([head2, lear, rear])
    if eyes:
        g = g.difference(unary_union([ellipse_poly(e) for e in EYES]))
    return g


def line_shape(width=18.0):
    """Version A line art: outward rings (width*0.8) for head, ears and patch edge."""
    lw = width * 0.8
    J = dict(quad_segs=32, join_style='round')
    head, lear, rear = ellipse_poly(HEAD), ellipse_poly(LEAR), ellipse_poly(REAR)
    patch = ellipse_poly(PATCH).intersection(head)
    ring = lambda q: q.buffer(lw, **J).difference(q)
    parts = [ring(lear),
             ring(rear).difference(lear),
             ring(head).difference(lear.buffer(lw, **J)).difference(rear.buffer(lw, **J)),
             ring(patch).intersection(head).difference(rear.buffer(lw, **J)).difference(lear.buffer(lw, **J))]
    eyes = unary_union([ellipse_poly(e) for e in EYES])
    return unary_union(parts + [eyes])


# ---------- analytic SVG bodies ----------
def color_body(head=WHITE, car=CARAMEL, ink=INK, eyes=True, pid="h"):
    """Version A colour mark: caramel silhouette + white face + eyes (exact approved artwork)."""
    s = [f'<path fill="{car}" d="{poly_d(COLOR_SIL)}"/>',
         f'<path fill="{head}" d="{poly_d(COLOR_WHITE)}"/>']
    if eyes:
        s += [f'<path fill="{ink}" d="{ellipse_d(e)}"/>' for e in EYES]
    return "\n".join(s)


def outline_body(head=WHITE, car=CARAMEL, ink=INK, pid="h", eyes=True):
    s = [f'<defs><clipPath id="{pid}"><path d="{ellipse_d(HEAD)}"/></clipPath></defs>',
         # silhouette outline: every shape grown by STROKE, filled ink
         f'<path fill="{ink}" d="{poly_d(unary_union([ellipse_poly(e) for e in (HEAD, LEAR, REAR)]).buffer(STROKE, quad_segs=32, join_style="round"))}"/>',
         f'<path fill="{head}" d="{ellipse_d(HEAD)}"/>',
         f'<path fill="{car}" clip-path="url(#{pid})" d="{ellipse_d(PATCH)}"/>',
         # right ear: outer line, then patch repainted so the ear meets the patch without a line
         f'<path fill="{ink}" d="{ellipse_d(REAR, EAR_LINE)}"/>',
         f'<path fill="{car}" d="{ellipse_d(REAR)}"/>',
         f'<path fill="{ink}" d="{ellipse_d(LEAR, EAR_LINE)}"/>',
         f'<path fill="{car}" d="{ellipse_d(LEAR)}"/>']
    if eyes:
        s += [f'<path fill="{ink}" d="{ellipse_d(e)}"/>' for e in EYES]
    return "\n".join(s)


def svg_doc(body, vb, w=None, h=None, bg=None):
    x, y, W, H = vb
    size = f' width="{w}" height="{h}"' if w else ""
    rect = f'<rect x="{x}" y="{y}" width="{W}" height="{H}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x:.2f} {y:.2f} {W:.2f} {H:.2f}"{size}>\n'
            f'{rect}{body}\n</svg>\n')


def tight_vb(grow=0.0, pad=0.0):
    x0, y0, x1, y1 = bbox(grow)
    return (x0 - pad, y0 - pad, x1 - x0 + 2 * pad, y1 - y0 + 2 * pad)
