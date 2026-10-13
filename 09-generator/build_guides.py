import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from geom import *
from common import *
G = os.path.join(KIT, '01-logo/guides')
x0, y0, x1, y1 = bbox()
X = EYES[0][3]  # clear-space unit = eye height
def construction():
    body = color_body(pid='c')
    lines = ''.join(f'<path d="{ellipse_d(e)}" fill="none" stroke="#6EA3E0" stroke-width="3" stroke-dasharray="10 8"/>'
                    f'<path d="M{e[0]-14} {e[1]}H{e[0]+14}M{e[0]} {e[1]-14}V{e[1]+14}" stroke="#6EA3E0" stroke-width="3"/>' for e in (HEAD, LEAR, REAR, PATCH, *EYES))
    return svg_doc(body + lines, (x0 - 140, y0 - 120, x1 - x0 + 280, y1 - y0 + 300))
def clearspace():
    body = color_body(pid='k')
    box = f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="none" stroke="#D9803A" stroke-width="3" stroke-dasharray="10 8"/>'
    outer = f'<rect x="{x0-X}" y="{y0-X}" width="{x1-x0+2*X}" height="{y1-y0+2*X}" fill="none" stroke="#D9803A" stroke-width="4"/>'
    unit = ''.join(f'<rect x="{x}" y="{y}" width="{X}" height="{X}" fill="#D9803A" fill-opacity=".18"/>' for x, y in [(x0 - X, y0 - X), (x1, y0 - X), (x0 - X, y1), (x1, y1)])
    eye = f'<rect x="{EYES[0][0]-EYES[0][2]/2-4}" y="{EYES[0][1]-X/2}" width="{EYES[0][2]+8}" height="{X}" fill="none" stroke="#6EA3E0" stroke-width="3"/>'
    return svg_doc(unit + box + outer + body + eye, (x0 - X - 30, y0 - X - 30, x1 - x0 + 2 * X + 60, y1 - y0 + 2 * X + 60))
def misuse():
    m = {}
    m['recolor'] = svg_doc(color_body(car='#6EA3E0', pid='m1'), tight_vb())
    nose = '<ellipse cx="472" cy="430" rx="46" ry="32" fill="#3B2A22"/><path d="M420 480Q472 530 524 480" fill="none" stroke="#0E0E10" stroke-width="16" stroke-linecap="round"/>'
    m['face'] = svg_doc(color_body(pid='m2') + nose, tight_vb())
    m['outline-dark'] = svg_doc(outline_body(ink='#FFFFFF', pid='m3'), tight_vb(STROKE))
    m['gradient'] = svg_doc('<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FF7A00"/><stop offset="1" stop-color="#C2185B"/></linearGradient></defs>' + color_body(car='url(#g)', pid='m4'), tight_vb())
    return m
write(f'{G}/atu-construction.svg', construction())
write(f'{G}/atu-clearspace.svg', clearspace())
for k, v in misuse().items(): write(f'{G}/misuse/atu-dont-{k}.svg', v)
with Renderer() as r:
    r.svg(construction(), f'{G}/atu-construction.png', 1600)
    r.svg(clearspace(), f'{G}/atu-clearspace.png', 1600)
print('guides ok')
