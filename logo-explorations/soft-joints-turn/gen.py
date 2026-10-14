"""Exploration (branch explore/soft-joints-turn): softer Atu line work.
v2: joins are drawn as one stroke of constant width (rounded centre line, concentric edges).

Does not touch geom.py or any guideline asset. Two ideas, tried alone and together:
  1. Soft joins: where the ears meet the head, the line turns through a very small arc,
     like a pen bending round, instead of a hard intersection (morphological closing).
  2. Slight turn: the face turns a little to the viewer's left. Eyes and patch follow a
     sphere, the ears follow their roots, and the leading cheek gets a Shin-chan-style arc.
Run: pyx logo-explorations/soft-joints-turn/gen.py
"""
import math, os, sys, json
import numpy as np
from shapely.geometry import Polygon, MultiPolygon
from shapely import affinity
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '09-generator'))
import geom as G
from geom import INK, CARAMEL, WHITE, STROKE, EAR_LINE, poly_d

J = dict(quad_segs=32, join_style='round')
CX, CY = 455.0, 330.0          # head centre, master units
RX = 304.0                     # head half width


def closing(g, r):
    return g.buffer(r, **J).buffer(-r, **J) if r else g


def opening(g, r):
    return g.buffer(-r, **J).buffer(r, **J) if r else g


# ---------- slight turn ----------
def sphere_x(x, phi):
    """x on a sphere of radius RX turned by phi (negative = towards viewer's left)."""
    u = (x - CX) / RX
    if abs(u) <= 1:
        return CX + RX * math.sin(math.asin(u) + phi)
    edge = math.copysign(1, u)
    return x + RX * (math.sin(math.asin(edge) + phi) - edge)


def map_poly(p, f):
    import shapely
    p = shapely.segmentize(p, 3.0)
    polys = p.geoms if isinstance(p, MultiPolygon) else [p]
    out = [Polygon([f(x, y) for x, y in q.exterior.coords]) for q in polys]
    return unary_union([o.buffer(0) for o in out])


def head_turned(head, phi, cheek, waist):
    """Cheek arc on the leading (lower-left) side, a small waist above it, and a fuller
    back of the head on the trailing side. Displacement along the radius from the centre."""
    s = abs(phi) / math.radians(10)          # effects scale with the turn
    g = lambda a, c, w: math.exp(-((math.atan2(math.sin(a - c), math.cos(a - c))) / w) ** 2)
    pts = []
    for x, y in head.exterior.coords:
        dx, dy = x - CX, y - CY
        a = math.atan2(dy, dx)                # image coords: +y down; pi*0.75 = lower-left
        r = math.hypot(dx, dy)
        d = (cheek * g(a, math.radians(142), math.radians(22))
             - waist * g(a, math.radians(176), math.radians(14))
             + 0.018 * g(a, math.radians(-25), math.radians(45))) * s * RX
        k = (r + d) / r
        pts.append((CX + dx * k, CY + dy * k))
    sh = sphere_x(CX, phi) - CX               # whole head drifts a touch with the turn
    return affinity.translate(Polygon(pts).buffer(0), sh * 0.25, 0)


# Pinned to the glyph as it was when this exploration ran (v2.0, front face), so the
# page stays reproducible after S1 became the guideline glyph (v2.1).
_V20 = json.load(open(os.path.join(HERE, 'glyph_shapes_v2.0.json')))
_P = lambda k: Polygon(_V20[k]).buffer(0)


def turned_shapes(phi=0.0, cheek=0.0, waist=0.0, as_is=False):
    """as_is: the current shapes untouched (reference 00). Otherwise the patch is also
    taken out to the head outline, so no white hairline shows between patch and line."""
    head, lear, rear, patch = (_P(k) for k in ('head', 'lear', 'rear', 'patch'))
    eyes = [Polygon(e).buffer(0) for e in _V20['eyes']]
    if as_is:
        return dict(head=head, lear=lear, rear=rear, patch=patch, eyes=eyes)
    f = lambda x, y: (sphere_x(x, phi), y)
    head2 = head_turned(head, phi, cheek, waist)
    eyes2 = [map_poly(e, f) for e in eyes]
    # the patch's leading edge follows the sphere; its back edge stays on the head outline
    # the patch's leading edge follows the sphere; the part that lies on the head outline
    # stays on the (new) outline: those points are projected radially onto it
    import shapely
    from shapely.geometry import LineString, Point
    ring = head2.exterior
    def to_outline(x, y, extra=12.0):
        dx, dy = x - CX, y - CY; r = math.hypot(dx, dy)
        hit = ring.intersection(LineString([(CX, CY), (CX + dx / r * 2000, CY + dy / r * 2000)]))
        R = max(math.hypot(qx - CX, qy - CY) for g in getattr(hit, 'geoms', [hit]) for qx, qy in g.coords)
        k = (R + extra) / r
        return CX + dx * k, CY + dy * k
    inner = head.buffer(-4, **J)
    pts = []
    for x, y in shapely.segmentize(patch, 3.0).exterior.coords:
        mx, my = sphere_x(x, phi), y
        pts.append(to_outline(mx, my) if not inner.contains(Point(x, y)) else (mx, my))
    patch2 = Polygon(pts).buffer(0)
    patch2 = opening(closing(patch2, 8), 5)
    # ears move with their roots on the sphere; the far ear also tips slightly back
    lroot, rroot = (300.0, 120.0), (740.0, 230.0)
    lear2 = affinity.translate(lear, sphere_x(lroot[0], phi) - lroot[0], 0)
    lear2 = affinity.rotate(lear2, math.degrees(phi) * 0.4, origin=lroot)
    rear2 = affinity.translate(rear, sphere_x(rroot[0], phi) - rroot[0], 0)
    return dict(head=head2, lear=lear2, rear=rear2, patch=patch2, eyes=eyes2)


# ---------- drawing ----------
def stroke_ring(sil, lw, rc):
    """One-stroke outline of `sil`, grown outward, width lw everywhere.
    The pen's centre line (sil grown by lw/2) is rounded at every inward corner with radius
    rc, then both edges are offset lw/2 from that centre line: inside and outside of each
    turn are concentric arcs (radii rc - lw/2 and rc + lw/2), so the width never changes.
    rc = 0 keeps the current hard join. Returns (ink ring, inner edge region)."""
    if not rc:
        return sil.buffer(lw, **J).difference(sil), sil
    centre = closing(sil.buffer(lw / 2, **J), rc)
    inner = centre.buffer(-lw / 2, **J)
    return centre.buffer(lw / 2, **J).difference(inner), inner


def outline_svg(S, rc, rf):
    """Outline mark: outward silhouette stroke + ear lines over the face.
    rc: centre-line radius of the turn where ear and head meet (0 = current hard join).
    rf: tip radius of the thin white wedge where an ear line meets the outline."""
    head, lear, rear = S['head'], S['lear'], S['rear']
    ears = unary_union([lear, rear])
    sil = unary_union([head, ears])
    ring, inner = stroke_ring(sil, STROKE, rc)
    ear_fill = ears.intersection(inner)
    face = inner.difference(ears.buffer(EAR_LINE, **J))
    face = opening(face, rf)                     # wedge tips end in a small round, not a needle
    outer = unary_union([ring, inner])
    ink = outer.difference(face).difference(ear_fill)
    if not rc:                                   # current construction, unchanged
        earlines = unary_union([e.buffer(EAR_LINE, **J).difference(e) for e in (lear, rear)]).intersection(sil)
        ink = unary_union([ring, earlines])
        face = sil
    patch = S['patch'].intersection(head).intersection(face).difference(ears)
    eyes = unary_union(S['eyes'])
    return [(WHITE, face), (CARAMEL, patch), (CARAMEL, ear_fill), (INK, ink.intersection(outer)), (INK, eyes)], inner


def line_svg(S, rc):
    sil = unary_union([S['head'], S['lear'], S['rear']])
    ring, inner = stroke_ring(sil, 18.0 * 0.8, rc)
    return [(INK, unary_union([ring, unary_union(S['eyes'])]))], inner


def color_svg(S, r_sil):
    """Colour mark with the transparent face/ear gap (same recipe as geom.color_body)."""
    ears = unary_union([S['lear'], S['rear']])
    face = S['head'].difference(ears.buffer(G.COLOR_GAP, **J))
    r = G.COLOR_ROUND
    face = face.buffer(-r, **J).buffer(2 * r, **J).buffer(-r, **J)
    patch = S['patch'].intersection(face)
    white = face.difference(patch).buffer(-4, **J).buffer(5.5, **J).intersection(face)
    return [(CARAMEL, ears), (CARAMEL, patch), (WHITE, white), (INK, unary_union(S['eyes']))], face


VB = (-40, -30, 950, 720)


def doc(layers, bg=None, vb=VB):
    x, y, w, h = vb
    rect = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    body = ''.join(f'<path fill="{c}" fill-rule="evenodd" d="{poly_d(g)}"/>' for c, g in layers if not g.is_empty)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}">{rect}{body}</svg>\n'


# id, title (zh), note, turn (deg, negative = viewer's left), cheek, waist, r_sil, r_ink
VARIANTS = [
    ('00', '现行规范（对照）', '硬拼接，正脸', 0, 0, 0, 0, 0),
    ('S1', '现行 + 微侧 6°', '线条和转角保持现行，只把脸微侧（同 T1 的侧法）', -6, 0.05, 0.0, 0, 0),
    ('S2', '现行 + 侧 10° + 小新式脸颊', '线条和转角保持现行，侧脸同 T3', -10, 0.07, 0.035, 0, 0),
    ('J1', '一笔转角 · 小', '线的中心线转弯半径 = 0.8 倍线宽；内外两条边同心，线宽不变', 0, 0, 0, 11.5, 4),
    ('J2', '一笔转角 · 中', '中心线转弯半径 = 1.3 倍线宽', 0, 0, 0, 19, 5),
    ('T1', 'J1 + 微侧 6°', '五官和耳朵跟着转，脸颊轻轻鼓一点', -6, 0.05, 0.0, 11.5, 4),
    ('T2', 'J1 + 侧 10° + 脸颊弧', '左下脸颊鼓出一道弧', -10, 0.06, 0.0, 11.5, 4),
    ('T3', 'J1 + 侧 10° + 小新式脸颊', '脸颊鼓出，上方轻收一点腰', -10, 0.07, 0.035, 11.5, 4),
    ('T4', 'J2 + 侧 14° + 小新式脸颊', '侧得更明显，作为上限参考', -14, 0.065, 0.03, 19, 5),
]


def build():
    os.makedirs(os.path.join(HERE, 'svg'), exist_ok=True)
    meta = []
    for vid, title, note, deg, cheek, waist, rs, ri in VARIANTS:
        S = turned_shapes(math.radians(deg), cheek, waist, as_is=(vid == '00'))
        files = {}
        for kind, (layers, _), bg in [
            ('outline', outline_svg(S, rs, ri), '#F7F7F8'),
            ('line', line_svg(S, rs), '#F7F7F8'),
            ('color', color_svg(S, rs), '#0E0E10'),
        ]:
            name = f'atu-{vid}-{kind}.svg'
            open(os.path.join(HERE, 'svg', name), 'w').write(doc(layers, bg))
            files[kind] = f'svg/{name}'
            if kind in ('outline', 'line'):
                for zid, zvb in (('zl', (77, 213, 180, 135)), ('zr', (647, 125, 180, 135))):
                    zname = f'atu-{vid}-{kind}-{zid}.svg'
                    open(os.path.join(HERE, 'svg', zname), 'w').write(doc(layers, bg, zvb))
                    files[f'{kind}-{zid}'] = f'svg/{zname}'
        meta.append(dict(id=vid, title=title, note=note, files=files))
    json.dump(meta, open(os.path.join(HERE, 'variants.json'), 'w'), ensure_ascii=False, indent=1)
    return meta


PAGE_HEAD = """<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>阿图 · 线条软化探索</title>
<style>
*,*::before,*::after{box-sizing:border-box}
body{margin:0;padding:12px;background:#ececec;font:14px/1.5 -apple-system,system-ui,sans-serif;color:#1c1a1b;overflow-wrap:anywhere}
main{max-width:60rem;margin:auto}
h1{font-size:20px;margin:4px 0 6px}
.lead{color:#555;margin:0 0 12px}
.lead li{margin:2px 0}
section{background:#fff;border-radius:12px;padding:10px;margin-bottom:10px;min-width:0}
h2{font-size:16px;margin:0}
.note{color:#777;margin:0 0 8px}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}
.zoom{margin-top:6px}
figure{margin:0;min-width:0}
figure img{display:block;width:100%;height:auto;border-radius:8px;outline:1px solid #0001}
figcaption{font-size:11px;color:#888;text-align:center}
@media (max-width:520px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}.grid figure:first-child{grid-column:1/-1}body{padding:8px}section{padding:8px}}
</style></head><body><main>
<h1>阿图 · 线条软化探索</h1>
<ul class="lead">
<li>分支 <code>explore/soft-joints-turn</code>，现行规范和所有物料都没动。</li>
<li><b>一笔转角</b>（第二版）：先把笔的中心线在耳朵和头的交点处转成小圆弧，再从中心线向两侧各让出半个线宽。转角的内外两条边是同心圆弧，线宽始终不变，不再有尖角或方形的痕迹。J1/J2 同时补上了眼斑和轮廓线之间的白缝。</li>
<li><b>微侧脸</b>：脸朝画面左边转一点。眼睛、眼斑、耳朵跟着转；左下脸颊鼓出一道弧，像蜡笔小新的脸，不再是正圆。</li>
<li>每组：描边版 · 线条版（刺绣）· 彩色深底；下面是两个连接处的放大。</li>
</ul>
"""


def render_png(meta):
    """Review-sized PNGs for the phone preview (it does not load SVG images)."""
    from playwright.sync_api import sync_playwright
    os.makedirs(os.path.join(HERE, 'png'), exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page()
        for m in meta:
            for k, rel in list(m['files'].items()):
                w, h = (360, 270) if '-z' in k else (760, 576)
                pg.set_viewport_size({'width': w, 'height': h})
                svg = open(os.path.join(HERE, rel)).read().replace('<svg ', f'<svg width="{w}" height="{h}" ', 1)
                pg.set_content(f'<body style="margin:0">{svg}</body>')
                out = rel.replace('svg/', 'png/').replace('.svg', '.png')
                pg.screenshot(path=os.path.join(HERE, out))
                m['files'][k + '.png'] = out
        b.close()
    # the four joint close-ups go into one 2 x 2 sheet per variant (fewer preview files)
    from PIL import Image
    for m in meta:
        ks = ['outline-zl', 'outline-zr', 'line-zl', 'line-zr']
        sheet = Image.new('RGB', (2 * 360 + 6, 2 * 270 + 6), (236, 236, 236))
        for i, k in enumerate(ks):
            fp = os.path.join(HERE, m['files'].pop(k + '.png'))
            sheet.paste(Image.open(fp).convert('RGB'), ((i % 2) * 366, (i // 2) * 276))
            os.remove(fp)
        out = f"png/atu-{m['id']}-zoom.png"
        sheet.save(os.path.join(HERE, out))
        m['files']['zoom.png'] = out


def build_page(meta):
    cards = []
    for m in meta:
        f = {k[:-4]: v for k, v in m['files'].items() if k.endswith('.png')}
        main = ''.join(f'<figure><img src="{f[k]}" alt="{m["id"]} {cap}" width="760" height="576"><figcaption>{cap}</figcaption></figure>'
                       for k, cap in (('outline', '描边版'), ('line', '线条版'), ('color', '彩色深底')))
        zoom = (f'<figure><img src="{f["zoom"]}" alt="{m["id"]} 转角放大" width="726" height="546">'
                '<figcaption>转角放大：上排描边版（左耳下 · 右耳上），下排线条版</figcaption></figure>')
        cards.append(f'<section id="v-{m["id"]}"><h2>{m["id"]} · {m["title"]}</h2><p class="note">{m["note"]}</p>'
                     f'<div class="grid">{main}</div><div class="zoom">{zoom}</div></section>')
    open(os.path.join(HERE, 'index.html'), 'w').write(PAGE_HEAD + '\n'.join(cards) + '\n</main></body></html>\n')


if __name__ == '__main__':
    meta = build()
    render_png(meta)
    build_page(meta)
    for m in meta:
        print(m['id'], m['title'])
