import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from geom import *
from common import *

L = os.path.join(KIT, '01-logo')
S = os.path.join(KIT, '05-states')
GREY_HEAD, GREY_CAR = '#A1A1AA', '#6E6E78'


# ---------------- glyph variants ----------------
def glyph_variants():
    vb0 = tight_vb()
    vbS = tight_vb(STROKE)
    v = {
        'atu-glyph-color': svg_doc(color_body(), vb0),
        'atu-glyph-outline': svg_doc(outline_body(), vbS),
        'atu-glyph-mono-ink': svg_doc(f'<path fill="{INK}" fill-rule="evenodd" d="{poly_d(mono_shape())}"/>', vb0),
        'atu-glyph-mono-white': svg_doc(f'<path fill="#FFFFFF" fill-rule="evenodd" d="{poly_d(mono_shape())}"/>', vb0),
        'atu-glyph-mono-caramel': svg_doc(f'<path fill="{CARAMEL}" fill-rule="evenodd" d="{poly_d(mono_shape())}"/>', vb0),
        'atu-glyph-line-ink': svg_doc(f'<path fill="{INK}" fill-rule="evenodd" d="{poly_d(line_shape())}"/>', tight_vb(9)),
        'atu-glyph-line-white': svg_doc(f'<path fill="#FFFFFF" fill-rule="evenodd" d="{poly_d(line_shape())}"/>', tight_vb(9)),
    }
    return v


# ---------------- lockups ----------------
def lockup(kind='h', on='dark', glyph='color'):
    gb = color_body(pid='lh') if glyph == 'color' else outline_body(pid='lh')
    grow = 0 if glyph == 'color' else STROKE
    x0, y0, x1, y1 = bbox(grow)
    gw, gh = x1 - x0, y1 - y0
    fg = '#F7F7F8' if on == 'dark' else '#18181B'
    cap = 0.40 * gh
    size = cap / 0.73
    if kind == 'h':
        gap = 0.26 * gh
        d, tw, capp = text_path('Hey Atu', 'JetBrainsMono-500.ttf', size, x1 + gap, 0, tracking=-0.01)
        base = HEAD[1] + capp / 2
        d, tw, capp = text_path('Hey Atu', 'JetBrainsMono-500.ttf', size, x1 + gap, base, tracking=-0.01)
        vb = (x0, y0, gw + gap + tw, gh)
    else:
        gap = 0.20 * gh
        size = size * 0.78
        d0, tw, capp = text_path('Hey Atu', 'JetBrainsMono-500.ttf', size, 0, 0, tracking=-0.01)
        tx = x0 + gw / 2 - tw / 2
        base = y1 + gap + capp
        d, tw, capp = text_path('Hey Atu', 'JetBrainsMono-500.ttf', size, tx, base, tracking=-0.01)
        left = min(x0, tx); right = max(x1, tx + tw)
        vb = (left, y0, right - left, base - y0 + size * 0.26)
    body = gb + f'\n<path fill="{fg}" d="{d}"/>'
    return svg_doc(body, vb)


def wordmark(color):
    d, tw, capp = text_path('Hey Atu', 'JetBrainsMono-500.ttf', 100, 0, 73.0, tracking=-0.01)
    return svg_doc(f'<path fill="{color}" d="{d}"/>', (0, 0, tw, 73.0 + 26))


# ---------------- states ----------------
def eye_arc(cx, cy, up=True, w=48, h=30):
    if up:   # ^  happy
        return f'M{cx-w} {cy+h*0.6} Q{cx} {cy-h*1.6} {cx+w} {cy+h*0.6}'
    return f'M{cx-w} {cy-h*0.2} Q{cx} {cy+h*1.4} {cx+w} {cy-h*0.2}'  # ‿ closed


def state(name):
    x0, y0, x1, y1 = bbox()
    extra = ''
    if name == 'idle':
        body = color_body(pid='s')
        vb = (x0, y0 - 90, x1 - x0 + 60, y1 - y0 + 90)
    elif name == 'working':
        eyes = [(e[0], e[1] + 38, e[2], e[3] * 0.82, 0) for e in EYES]
        body = color_body(pid='s', eyes=False) + ''.join(f'<path fill="{INK}" d="{ellipse_d(e)}"/>' for e in eyes)
        # back of an open laptop in front of the chin
        body += (f'<rect x="268" y="470" width="400" height="232" rx="26" fill="#8C8C96"/>'
                 f'<rect x="232" y="690" width="472" height="34" rx="17" fill="#5A5A64"/>'
                 f'<circle cx="468" cy="586" r="16" fill="{CARAMEL}"/>')
        vb = (x0, y0 - 90, x1 - x0 + 60, 724 - y0 + 90)
    elif name == 'done':
        body = color_body(pid='s', eyes=False)
        body += ''.join(f'<path d="{eye_arc(e[0], e[1] - 6, True)}" fill="none" stroke="{INK}" stroke-width="32" stroke-linecap="round"/>' for e in EYES)
        cx, cy, r = 900, 0, 86
        star = (f'M{cx} {cy-r}C{cx+8} {cy-12} {cx+12} {cy-8} {cx+r} {cy}C{cx+12} {cy+8} {cx+8} {cy+12} {cx} {cy+r}'
                f'C{cx-8} {cy+12} {cx-12} {cy+8} {cx-r} {cy}C{cx-12} {cy-8} {cx-8} {cy-12} {cx} {cy-r}Z')
        body += f'<path fill="{CARAMEL}" d="{star}"/>'
        vb = (x0, y0 - 150, x1 - x0 + 140, y1 - y0 + 150)
    elif name == 'offline':
        body = color_body(head=GREY_HEAD, car=GREY_CAR, pid='s', eyes=False)
        body += ''.join(f'<path d="{eye_arc(e[0], e[1], False)}" fill="none" stroke="{INK}" stroke-width="30" stroke-linecap="round"/>' for e in EYES)
        z1, *_ = text_path('z', 'JetBrainsMono-700.ttf', 190, 800, 60)
        z2, *_ = text_path('z', 'JetBrainsMono-700.ttf', 130, 920, -50)
        body += f'<path fill="{GREY_HEAD}" d="{z1}"/><path fill="{GREY_HEAD}" d="{z2}"/>'
        vb = (x0, y0 - 150, x1 - x0 + 140, y1 - y0 + 150)
    return svg_doc(body, vb)


if __name__ == '__main__':
    files = {}
    for k, v in glyph_variants().items():
        files[f'{L}/svg/{k}.svg'] = v
    for on in ['dark', 'light']:
        g = 'color' if on == 'dark' else 'outline'
        files[f'{L}/svg/atu-lockup-horizontal-on-{on}.svg'] = lockup('h', on, g)
        files[f'{L}/svg/atu-lockup-stacked-on-{on}.svg'] = lockup('v', on, g)
    files[f'{L}/svg/atu-wordmark-ink.svg'] = wordmark('#18181B')
    files[f'{L}/svg/atu-wordmark-white.svg'] = wordmark('#F7F7F8')
    for st in ['idle', 'working', 'done', 'offline']:
        files[f'{S}/svg/atu-state-{st}.svg'] = state(st)
    for p, t in files.items():
        write(p, t)
    with Renderer() as r:
        for p, t in files.items():
            name = os.path.basename(p)[:-4]
            base = os.path.dirname(os.path.dirname(p))
            widths = [512, 1024, 2048] if 'lockup' not in name and 'wordmark' not in name else [1200, 2400]
            if '05-states' in p: widths = [256, 512, 1024]
            for w in widths:
                r.svg(t, f'{base}/png/{name}@{w}w.png', w)
    print(len(files), 'svg written')
