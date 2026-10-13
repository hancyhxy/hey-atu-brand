import base64, os, math
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from playwright.sync_api import sync_playwright

ROOT = os.path.expanduser('~/.pi/tmp/2026-10-12/brand-spec')
KIT = os.environ.get('ATU_KIT') or os.path.join(ROOT, 'HeyAtu-Brand-Kit')
FONTS = os.path.join(ROOT, 'fonts/ttf')

_fonts = {}


def font(name):
    if name not in _fonts:
        _fonts[name] = TTFont(os.path.join(FONTS, name))
    return _fonts[name]


def text_path(text, fname='JetBrainsMono-500.ttf', size=100, x=0, baseline=0, tracking=0.0):
    """Outline text. Returns (path_d, width, cap_height_px)."""
    f = font(fname)
    gs = f.getGlyphSet()
    cmap = f.getBestCmap()
    upm = f['head'].unitsPerEm
    s = size / upm
    pen = SVGPathPen(gs)
    cx = x
    for ch in text:
        g = cmap[ord(ch)]
        tp = TransformPen(pen, (s, 0, 0, -s, cx, baseline))
        gs[g].draw(tp)
        cx += gs[g].width * s + tracking * size
    width = cx - x - tracking * size
    cap = getattr(f['OS/2'], 'sCapHeight', 730) * s
    return pen.getCommands(), width, cap


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as fh:
        fh.write(text)


class Renderer:
    def __enter__(self):
        self.p = sync_playwright().start()
        self.b = self.p.chromium.launch()
        self.pg = self.b.new_page(viewport={'width': 800, 'height': 800})
        return self

    def __exit__(self, *a):
        self.b.close(); self.p.stop()

    def svg(self, svg_text, out, w, h=None, bg=None):
        """Rasterise SVG text to PNG of exact size. bg=None keeps alpha."""
        if h is None:
            import re
            vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', svg_text).group(1).split()]
            h = round(w * vb[3] / vb[2])
        b64 = base64.b64encode(svg_text.encode()).decode()
        self.pg.set_viewport_size({'width': w, 'height': h})
        bgc = bg or 'transparent'
        self.pg.set_content(f'<html><body style="margin:0;background:{bgc}"><img src="data:image/svg+xml;base64,{b64}" '
                            f'style="display:block;width:{w}px;height:{h}px"></body></html>')
        self.pg.wait_for_function('document.images[0].complete')
        os.makedirs(os.path.dirname(out), exist_ok=True)
        self.pg.screenshot(path=out, omit_background=bg is None, clip={'x': 0, 'y': 0, 'width': w, 'height': h})
        return out

    def html(self, html, out, w, h, scale=1, wait=300, alpha=False):
        self.pg.set_viewport_size({'width': w, 'height': h})
        if scale != 1:
            ctx = self.b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=scale)
            pg = ctx.new_page()
        else:
            ctx, pg = None, self.pg
        pg.set_content(html, wait_until='load')
        pg.evaluate('document.fonts.ready')
        pg.wait_for_timeout(wait)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        pg.screenshot(path=out, omit_background=alpha, clip={'x': 0, 'y': 0, 'width': w, 'height': h})
        if ctx: ctx.close()
        return out


def render_file(r, html_path, out, w, h, alpha=False, wait=400):
    r.pg.set_viewport_size({'width': w, 'height': h})
    r.pg.goto('file://' + html_path, wait_until='load')
    r.pg.evaluate('document.fonts.ready.then(()=>1)')
    r.pg.wait_for_timeout(wait)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    r.pg.screenshot(path=out, omit_background=alpha, clip={'x': 0, 'y': 0, 'width': w, 'height': h})
    return out
