"""Atu Flat stickers: the current Mark plus one accessory each, drawn in vector.

Every sticker is built from geom.py, so a change to the Mark updates the stickers.
Dark tiles use the colour mark (with the face/ear gap); light tiles use the outline
mark and outline the accessories in ink. Output: 10-character/flat-stickers/
  svg/<name>-{dark,light}.svg, tiles/<name>-{dark,light}.png (1254 px),
  remix-{dark,light}.png (3 x 3 sheet with labels), and the same set in
  04-marketing/stickers/.
"""
import os, sys, shutil
sys.path.insert(0, os.path.dirname(__file__))
from geom import *
from common import KIT
from playwright.sync_api import sync_playwright

OUT = os.path.join(KIT, '10-character', 'flat-stickers')
MK = os.path.join(KIT, '04-marketing', 'stickers')
NAVY, NAVY2, ORANGE, CREAM, RED, CAR_L = '#1F2D4F', '#26407F', '#F08A2E', '#FBEBD3', '#D14343', '#E8954F'
NAMES = ['atu', 'focus', 'work', 'coffee', 'online', 'idle', 'party', 'cool', 'cozy']
VB = (-150, -250, 1170, 1170)          # square canvas around the mark, master units
J = dict(quad_segs=32, join_style='round')


class Pen:
    """Accessory painter: light theme outlines every shape in ink."""
    def __init__(self, light):
        self.light = light
        self.sw = 11 if light else 0

    def s(self, extra=''):
        return f' stroke="{INK}" stroke-width="{self.sw}" stroke-linejoin="round" stroke-linecap="round"{extra}' if self.light else extra

    def path(self, d, fill):
        return f'<path d="{d}" fill="{fill}"{self.s()}/>'

    def line(self, d, color, w):
        # open strokes (steam, zipper): ink on light, colour on dark
        col = INK if self.light and color == INK else color
        out = ''
        if self.light and color != INK:
            out += f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + 2 * self.sw}" stroke-linecap="round" stroke-linejoin="round"/>'
        return out + f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'

    def ell(self, cx, cy, rx, ry, fill, rot=0):
        return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" transform="rotate({rot} {cx} {cy})"{self.s()}/>'

    def rect(self, x, y, w, h, r, fill, rot=0, cx=None, cy=None):
        t = f' transform="rotate({rot} {cx if cx is not None else x + w / 2} {cy if cy is not None else y + h / 2})"' if rot else ''
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{t}{self.s()}/>'


def ears(light):
    """Ears drawn again on top of an accessory (beanie, headphone cups)."""
    out = ''
    for e in (REAR, LEAR):
        if light:
            out += f'<path fill="{INK}" d="{ellipse_d(e, EAR_LINE)}"/>'
        out += f'<path fill="{CARAMEL}" d="{ellipse_d(e)}"/>'
    return out


def accessory(name, p):
    """Returns (behind, front, ears_on_top)."""
    L = p.light
    if name == 'atu':        # fleece collar of the vest, zip in the middle
        ys = lambda x: 600 + 52 * (1 - ((x - 440) / 260) ** 2)
        scal = ''.join(p.ell(x, ys(x), 50, 44, CREAM) for x in list(range(220, 420, 62)) + list(range(660, 470, -62)))
        front = (p.path('M200 600 Q440 760 690 600 L700 660 Q440 800 190 660Z', NAVY) + scal +
                 p.rect(424, 640, 34, 92, 10, RED) + p.line('M441 600 L441 650', INK, 8))
        return '', front, False
    if name == 'focus':      # headphones
        band = p.line('M150 300 C110 -170 800 -170 800 280', CAR_L, 46)
        cups = p.rect(90, 240, 130, 250, 60, NAVY2) + p.rect(730, 230, 130, 250, 60, NAVY2)
        return band, cups, True
    if name == 'work':       # laptop in front of the chin
        front = (p.path('M600 470 L800 470 Q812 470 810 482 L784 640 L560 640 L586 482 Q588 470 600 470Z', NAVY) +
                 p.ell(690, 552, 13, 13, CAR_L) +
                 p.rect(520, 636, 330, 26, 12, NAVY))
        return '', front, False
    if name == 'coffee':     # mug with steam
        front = (p.line('M598 490 q-18 -22 0 -44 q18 -22 0 -44', INK if L else '#ECECF1', 9) +
                 p.line('M640 494 q-14 -18 0 -36 q14 -18 0 -36', INK if L else '#ECECF1', 9) +
                 p.line('M708 596 a36 32 0 1 1 -4 64', ORANGE, 22) +
                 p.path('M560 560 L720 560 L708 700 Q706 720 686 720 L594 720 Q574 720 572 700Z', ORANGE) +
                 p.ell(640, 562, 80, 14, '#C9661E'))
        return '', front, False
    if name == 'online':     # phone held by a white paw
        front = (p.rect(600, 470, 120, 210, 22, ORANGE, rot=14) +
                 p.rect(618, 496, 84, 150, 10, NAVY, rot=14, cx=660, cy=575) +
                 p.ell(728, 646, 50, 44, '#FFFFFF'))
        return '', front, False
    if name == 'idle':       # z z Z
        def z(x, y, s):
            d = f'M{x} {y} h{s} l{-s} {s} h{s}'
            return p.line(d, ORANGE, s * .32)
        return '', z(700, -10, 54) + z(790, -80, 72) + z(900, -175, 96), False
    if name == 'party':      # cone hat with a star and a pompom
        star = 'M450 -40 l12 26 28 3 -21 19 6 28 -25 -14 -25 14 6 -28 -21 -19 28 -3Z'
        front = (p.path('M360 60 L450 -170 L560 50 Q460 90 360 60Z', ORANGE) +
                 p.path(star, NAVY) + p.ell(450, -186, 30, 30, NAVY))
        return '', front, False
    if name == 'cool':       # sunglasses over both eyes
        lens = lambda cx: (f'M{cx - 102} 246 Q{cx} 232 {cx + 102} 246 C{cx + 108} 350 {cx + 64} 404 {cx} 404 '
                           f'C{cx - 64} 404 {cx - 108} 350 {cx - 102} 246Z')
        front = (p.line('M165 262 L290 258', INK, 22) + p.line('M630 258 L748 254', INK, 22) +
                 p.line('M474 262 Q459 244 444 262', INK, 22) +
                 p.path(lens(376), INK) + p.path(lens(542), INK))
        return '', front, False
    if name == 'cozy':       # beanie with a ribbed cuff and a pompom
        rib = ''.join(p.line(f'M{x} {150 - 40 * (1 - ((x - 455) / 330) ** 2) + 10} l-4 78', INK if L else '#B24E10', 8) for x in range(180, 740, 50))
        front = (p.ell(455, -150, 70, 66, ORANGE) +
                 p.path('M160 160 C150 -190 760 -190 750 160Z', NAVY) +
                 p.path('M130 150 Q455 50 780 150 L790 250 Q455 150 120 250Z', ORANGE) + rib)
        return '', front, True
    raise KeyError(name)


def sticker(name, theme):
    light = theme == 'light'
    p = Pen(light)
    behind, front, top = accessory(name, p)
    dog = outline_body(pid=f'{name}{theme}') if light else color_body(pid=f'{name}{theme}')
    return svg_doc(behind + dog + front + (ears(light) if top else ''), VB, 1254, 1254)


def show(page, html):
    tmp = os.path.join(OUT, '.render.html')
    open(tmp, 'w').write(html)
    page.goto('file://' + tmp)
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(200)
    os.remove(tmp)


def png(page, svg_path, out, bg, size=1254):
    page.set_viewport_size({'width': size, 'height': size})
    show(page, f'<body style="margin:0;background:{bg}"><img src="file://{svg_path}" width="{size}" height="{size}" style="display:block"></body>')
    page.screenshot(path=out)


def sheet(page, theme, out):
    bg, fg = ('#0E0E10', '#ECECF1') if theme == 'dark' else ('#F7F7F8', '#18181B')
    font = os.path.join(KIT, '07-fonts-and-tokens', 'fonts', 'JetBrainsMono-500.ttf')
    cells = ''.join(f'<figure><img src="file://{OUT}/svg/{n}-{theme}.svg"><figcaption>{n}</figcaption></figure>' for n in NAMES)
    page.set_viewport_size({'width': 1020, 'height': 1140})
    show(page, f'''<style>@font-face{{font-family:J;src:url("file://{font}")}}
body{{margin:0;background:{bg};width:1020px;height:1140px;display:grid;grid-template-columns:repeat(3,340px);grid-auto-rows:380px}}
figure{{margin:0;display:flex;flex-direction:column;align-items:center}}img{{width:330px;height:330px}}
figcaption{{font:500 26px J;color:{fg};margin-top:-6px}}</style>{cells}''')
    page.screenshot(path=out)


def main():
    for d in ('svg', 'tiles'):
        os.makedirs(os.path.join(OUT, d), exist_ok=True)
    with sync_playwright() as pw:
        page = pw.chromium.launch().new_page()
        for n in NAMES:
            for t in ('dark', 'light'):
                sp = os.path.join(OUT, 'svg', f'{n}-{t}.svg')
                open(sp, 'w').write(sticker(n, t))
                png(page, sp, os.path.join(OUT, 'tiles', f'{n}-{t}.png'), '#0E0E10' if t == 'dark' else '#F7F7F8')
        for t in ('dark', 'light'):
            sheet(page, t, os.path.join(OUT, f'remix-{t}.png'))
    if os.path.isdir(MK):
        for d in ('svg', 'tiles'):
            shutil.copytree(os.path.join(OUT, d), os.path.join(MK, d), dirs_exist_ok=True)
        for t in ('dark', 'light'):
            shutil.copy(os.path.join(OUT, f'remix-{t}.png'), MK)
    print('flat stickers done')


if __name__ == '__main__':
    main()
