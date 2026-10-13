"""Hey Atu glyph geometry. Single source for every logo, icon and state file.

Units: master units (the 03 v2 build). All shapes are ellipses (cx, cy, w, h, angle_deg),
angle = clockwise rotation in y-down coordinates (same in OpenCV and SVG).
"""
import math
from shapely.geometry import Point, Polygon, MultiPolygon, LineString
from shapely import affinity
from shapely.ops import unary_union

HEAD = (468.709, 330.383, 607.013, 669.647, 33.593)
LEAR = (164.581, 163.570, 204.356, 417.941, 45.425)
REAR = (778.803, 379.151, 160.164, 415.904, 171.239)
PATCH = (664.385, 215.614, 371.923, 489.340, 19.683)
EYES = [(388.14, 321.45, 70.5, 121.2, 0.0), (556.62, 321.34, 70.5, 121.2, 0.0)]

CARAMEL = "#D9803A"
INK = "#0E0E10"
WHITE = "#FFFFFF"
STROKE = 11.0          # sticker silhouette outline (outside), master units
EAR_LINE = 6.0         # ear-over-head line (outside half), master units


def ellipse_d(e, grow=0.0):
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
    cx, cy, w, h, a = e
    c = Point(0, 0).buffer(1, quad_segs=n)
    c = affinity.scale(c, w / 2 + grow, h / 2 + grow)
    c = affinity.rotate(c, a, origin=(0, 0))
    return affinity.translate(c, cx, cy)


def ellipse_bbox(e, grow=0.0):
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
def mono_shape(gap=14.0, eyes=True):
    head, lear, rear = ellipse_poly(HEAD), ellipse_poly(LEAR), ellipse_poly(REAR)
    head2 = head.difference(lear.buffer(gap)).difference(rear.buffer(gap))
    g = unary_union([head2, lear, rear])
    if eyes:
        g = g.difference(unary_union([ellipse_poly(e) for e in EYES]))
    return g


def line_shape(width=18.0):
    head, lear, rear = ellipse_poly(HEAD), ellipse_poly(LEAR), ellipse_poly(REAR)
    patch = ellipse_poly(PATCH).intersection(head)
    sil = unary_union([head, lear, rear])
    lines = [sil.exterior if hasattr(sil, 'exterior') else sil.boundary,
             lear.exterior.intersection(head),
             rear.exterior.intersection(head.difference(patch.buffer(-2))),
             patch.boundary.intersection(head.buffer(-1)).difference(lear).difference(rear)]
    strokes = unary_union([l.buffer(width / 2, cap_style='round', join_style='round') for l in lines])
    eyes = unary_union([ellipse_poly(e) for e in EYES])
    return unary_union([strokes, eyes])


# ---------- analytic SVG bodies ----------
def color_body(head=WHITE, car=CARAMEL, ink=INK, eyes=True, pid="h"):
    s = [f'<defs><clipPath id="{pid}"><path d="{ellipse_d(HEAD)}"/></clipPath></defs>',
         f'<path fill="{head}" d="{ellipse_d(HEAD)}"/>',
         f'<path fill="{car}" clip-path="url(#{pid})" d="{ellipse_d(PATCH)}"/>',
         f'<path fill="{car}" d="{ellipse_d(REAR)}"/>',
         f'<path fill="{car}" d="{ellipse_d(LEAR)}"/>']
    if eyes:
        s += [f'<path fill="{ink}" d="{ellipse_d(e)}"/>' for e in EYES]
    return "\n".join(s)


def outline_body(head=WHITE, car=CARAMEL, ink=INK, pid="h", eyes=True):
    s = [f'<defs><clipPath id="{pid}"><path d="{ellipse_d(HEAD)}"/></clipPath></defs>',
         # silhouette outline: every shape grown by STROKE, filled ink
         *[f'<path fill="{ink}" d="{ellipse_d(e, STROKE)}"/>' for e in (HEAD, LEAR, REAR)],
         f'<path fill="{head}" d="{ellipse_d(HEAD)}"/>',
         f'<path fill="{car}" clip-path="url(#{pid})" d="{ellipse_d(PATCH)}"/>',
         # right ear: outer line, then patch repainted so the ear meets the patch without a line
         f'<path fill="{ink}" d="{ellipse_d(REAR, EAR_LINE)}"/>',
         f'<path fill="{car}" clip-path="url(#{pid})" d="{ellipse_d(PATCH)}"/>',
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
