import os, sys, json, math, re
sys.path.insert(0, os.path.dirname(__file__))
from geom import *
from common import *
from shapely.ops import unary_union
from PIL import Image

A = os.path.join(KIT, '02-app-icon')
BG_DARK = '#0E0E10'

x0, y0, x1, y1 = bbox()
GW, GH = x1 - x0, y1 - y0
GCX, GCY = (x0 + x1) / 2, (y0 + y1) / 2
SIL = unary_union([ellipse_poly(HEAD), ellipse_poly(LEAR), ellipse_poly(REAR)])
MAXR = max(math.hypot(x - GCX, y - GCY) for x, y in SIL.exterior.coords)


def placed(body, size, width_frac=None, radius=None, dy=0.0):
    """Transform group that centres the glyph in a size x size box."""
    s = (width_frac * size / GW) if width_frac else (radius / MAXR)
    tx = size / 2 - GCX * s
    ty = size / 2 - GCY * s + dy * size
    return f'<g transform="translate({tx:.3f} {ty:.3f}) scale({s:.5f})">{body}</g>', s, tx, ty


def square_icon(size=1024, bg=BG_DARK, frac=0.70, body=None, round_r=None):
    g, *_ = placed(body or color_body(pid='i'), size, frac, dy=0.01)
    rect = (f'<rect width="{size}" height="{size}" rx="{round_r}" fill="{bg}"/>' if round_r is not None
            else (f'<rect width="{size}" height="{size}" fill="{bg}"/>' if bg else ''))
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">{rect}{g}</svg>'


def circle_icon(size, bg=BG_DARK, frac=0.62):
    g, *_ = placed(color_body(pid='c'), size, frac, dy=0.01)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}"><circle cx="{size/2}" cy="{size/2}" r="{size/2}" fill="{bg}"/>{g}</svg>'


# ---------------- Android VectorDrawable ----------------
def vd_color_group(s, tx, ty, outline=False):
    c = lambda h: '#FF' + h.lstrip('#').upper()
    P = lambda d, fill: f'    <path android:fillColor="{c(fill)}" android:pathData="{d}"/>\n'
    out = f'  <group android:translateX="{tx:.3f}" android:translateY="{ty:.3f}" android:scaleX="{s:.5f}" android:scaleY="{s:.5f}">\n'
    if not outline:   # version A colour mark
        out += P(poly_d(COLOR_SIL), CARAMEL) + P(poly_d(COLOR_WHITE), WHITE)
        for e in EYES:
            out += P(ellipse_d(e), INK)
        return out + '  </group>\n'
    if outline:
        out += P(poly_d(unary_union([ellipse_poly(e) for e in (HEAD, LEAR, REAR)]).buffer(STROKE, quad_segs=32, join_style='round')), INK)
    out += P(ellipse_d(HEAD), WHITE)
    out += f'    <group>\n      <clip-path android:pathData="{ellipse_d(HEAD)}"/>\n  ' + P(ellipse_d(PATCH), CARAMEL) + '    </group>\n'
    if outline:
        out += P(ellipse_d(REAR, EAR_LINE), INK)
    out += P(ellipse_d(REAR), CARAMEL)
    if outline:
        out += P(ellipse_d(LEAR, EAR_LINE), INK)
    out += P(ellipse_d(LEAR), CARAMEL)
    for e in EYES:
        out += P(ellipse_d(e), INK)
    return out + '  </group>\n'


def vd(size_dp, inner, comment=''):
    return (f'<?xml version="1.0" encoding="utf-8"?>\n<!-- Hey Atu · {comment} · generated from the brand kit geometry -->\n'
            f'<vector xmlns:android="http://schemas.android.com/apk/res/android"\n    android:width="{size_dp}dp" android:height="{size_dp}dp"\n'
            f'    android:viewportWidth="{size_dp}" android:viewportHeight="{size_dp}">\n{inner}</vector>\n')


def vd_mono(size_dp, radius_dp, color='#FFFFFFFF', comment='', gap=14):
    s = radius_dp / MAXR
    tx, ty = size_dp / 2 - GCX * s, size_dp / 2 - GCY * s
    d = poly_d(mono_shape(gap=gap))
    inner = (f'  <group android:translateX="{tx:.3f}" android:translateY="{ty:.3f}" android:scaleX="{s:.5f}" android:scaleY="{s:.5f}">\n'
             f'    <path android:fillColor="{color}" android:fillType="evenOdd" android:pathData="{d}"/>\n  </group>\n')
    return vd(size_dp, inner, comment), d, s, tx, ty


def main():
    files = {}
    # ---- iOS ----
    ios = f'{A}/ios/AppIcon.appiconset'
    # ---- Android res ----
    res = f'{A}/android/res'
    # adaptive foreground: glyph fits a 66dp safe circle (radius 31dp, 2dp margin)
    R_SAFE = 31.0
    s = R_SAFE / MAXR
    tx, ty = 54 - GCX * s, 54 - GCY * s
    files[f'{res}/drawable/ic_launcher_foreground.xml'] = vd(108, vd_color_group(s, tx, ty), 'adaptive icon foreground, 108dp, logo inside the 66dp safe zone')
    mono_xml, *_ = vd_mono(108, R_SAFE, '#FF000000', 'adaptive icon monochrome layer (Android 13+ themed icons)')
    files[f'{res}/drawable/ic_launcher_monochrome.xml'] = mono_xml
    files[f'{res}/values/ic_launcher_background.xml'] = '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#0E0E10</color>\n    <color name="atu_caramel">#D9803A</color>\n    <color name="atu_ink">#0E0E10</color>\n    <color name="atu_paper">#F7F7F8</color>\n</resources>\n'
    adaptive = ('<?xml version="1.0" encoding="utf-8"?>\n<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n'
                '    <background android:drawable="@color/ic_launcher_background"/>\n    <foreground android:drawable="@drawable/ic_launcher_foreground"/>\n'
                '    <monochrome android:drawable="@drawable/ic_launcher_monochrome"/>\n</adaptive-icon>\n')
    files[f'{res}/mipmap-anydpi-v26/ic_launcher.xml'] = adaptive
    files[f'{res}/mipmap-anydpi-v26/ic_launcher_round.xml'] = adaptive
    # notification small icon: white silhouette, 24dp, live area 20dp
    ntf_xml, ntf_d, ns, ntx, nty = vd_mono(24, 10.6, '#FFFFFFFF', 'notification small icon (status bar), white on transparent', gap=22)
    files[f'{res}/drawable/ic_stat_atu.xml'] = ntf_xml
    # splash (Android 12+): icon without background, 288dp, fits a 192dp circle
    s2 = 90 / MAXR
    files[f'{res}/drawable/splash_icon.xml'] = vd(288, vd_color_group(s2, 144 - GCX * s2, 144 - GCY * s2), 'Android 12+ splash icon on #0E0E10, 288dp, inside the 192dp circle')
    s3 = 88 / MAXR
    files[f'{res}/drawable/splash_icon_light.xml'] = vd(288, vd_color_group(s3, 144 - GCX * s3, 144 - GCY * s3, outline=True), 'Android 12+ splash icon on #F7F7F8 (outlined glyph)')
    files[f'{res}/values/splash_theme_snippet.xml'] = ('<?xml version="1.0" encoding="utf-8"?>\n<!-- Merge into themes.xml. Needs androidx.core:core-splashscreen. -->\n<resources>\n'
        '    <style name="Theme.HeyAtu.Starting" parent="Theme.SplashScreen">\n        <item name="windowSplashScreenBackground">#0E0E10</item>\n'
        '        <item name="windowSplashScreenAnimatedIcon">@drawable/splash_icon</item>\n        <item name="postSplashScreenTheme">@style/Theme.HeyAtu</item>\n    </style>\n</resources>\n')

    # SVG sources for icons
    svgs = {
        f'{A}/svg/app-icon-dark-1024.svg': square_icon(1024),
        f'{A}/svg/app-icon-light-1024.svg': square_icon(1024, '#F7F7F8', 0.70, outline_body(pid='o')),
        f'{A}/svg/app-icon-caramel-1024.svg': square_icon(1024, CARAMEL, 0.70, f'<path fill="#FFFFFF" fill-rule="evenodd" d="{poly_d(mono_shape())}"/>'),
        f'{A}/svg/android-adaptive-foreground-432.svg': f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 108 108"><g transform="translate({tx:.3f} {ty:.3f}) scale({s:.5f})">{color_body(pid="f")}</g></svg>',
        f'{A}/svg/android-adaptive-monochrome-432.svg': f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 108 108"><g transform="translate({tx:.3f} {ty:.3f}) scale({s:.5f})"><path fill="#000" fill-rule="evenodd" d="{poly_d(mono_shape())}"/></g></svg>',
        f'{A}/svg/android-notification-24.svg': f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><g transform="translate({ntx:.3f} {nty:.3f}) scale({ns:.5f})"><path fill="#fff" fill-rule="evenodd" d="{ntf_d}"/></g></svg>',
        f'{A}/svg/ios-dark-1024.svg': square_icon(1024, None),
        f'{A}/svg/ios-tinted-1024.svg': square_icon(1024, '#000000', 0.70, color_body(head='#FFFFFF', car='#8A8A8A', ink='#000000', pid='t')),
    }
    for p, t in {**files, **svgs}.items():
        write(p, t)

    with Renderer() as r:
        # iOS
        r.svg(svgs[f'{A}/svg/app-icon-dark-1024.svg'], f'{ios}/AppIcon-1024.png', 1024, 1024)
        r.svg(svgs[f'{A}/svg/ios-dark-1024.svg'], f'{ios}/AppIcon-1024-dark.png', 1024, 1024)
        r.svg(svgs[f'{A}/svg/ios-tinted-1024.svg'], f'{ios}/AppIcon-1024-tinted.png', 1024, 1024)
        # alt colourways
        for k in ['dark', 'light', 'caramel']:
            r.svg(svgs[f'{A}/svg/app-icon-{k}-1024.svg'], f'{A}/png/app-icon-{k}-1024.png', 1024, 1024)
        # Play store icon: full square, no rounding, no shadow
        r.svg(square_icon(512, BG_DARK, 0.68), f'{KIT}/03-stores/google-play/01-app-icon/play-icon-512.png', 512, 512)
        # Android legacy launcher + round + adaptive layers as PNG
        dens = {'mdpi': 1, 'hdpi': 1.5, 'xhdpi': 2, 'xxhdpi': 3, 'xxxhdpi': 4}
        for dname, m in dens.items():
            L = round(48 * m)
            r.svg(square_icon(L, BG_DARK, 0.66, round_r=L * 0.18), f'{res}/mipmap-{dname}/ic_launcher.png', L, L)
            r.svg(circle_icon(L), f'{res}/mipmap-{dname}/ic_launcher_round.png', L, L)
            F = round(108 * m)
            r.svg(svgs[f'{A}/svg/android-adaptive-foreground-432.svg'], f'{res}/mipmap-{dname}/ic_launcher_foreground.png', F, F)
            r.svg(svgs[f'{A}/svg/android-adaptive-monochrome-432.svg'], f'{res}/mipmap-{dname}/ic_launcher_monochrome.png', F, F)
            N = round(24 * m)
            r.svg(svgs[f'{A}/svg/android-notification-24.svg'], f'{res}/drawable-{dname}/ic_stat_atu.png', N, N)
    # iOS: drop alpha on the primary icon (App Store requirement)
    im = Image.open(f'{ios}/AppIcon-1024.png').convert('RGB'); im.save(f'{ios}/AppIcon-1024.png')
    im = Image.open(f'{ios}/AppIcon-1024-tinted.png').convert('L'); im.save(f'{ios}/AppIcon-1024-tinted.png')
    p = f'{KIT}/03-stores/google-play/01-app-icon/play-icon-512.png'
    Image.open(p).convert('RGBA').save(p)  # 32-bit PNG as Play requires
    write(f'{ios}/Contents.json', json.dumps({
        "images": [
            {"filename": "AppIcon-1024.png", "idiom": "universal", "platform": "ios", "size": "1024x1024"},
            {"appearances": [{"appearance": "luminosity", "value": "dark"}], "filename": "AppIcon-1024-dark.png", "idiom": "universal", "platform": "ios", "size": "1024x1024"},
            {"appearances": [{"appearance": "luminosity", "value": "tinted"}], "filename": "AppIcon-1024-tinted.png", "idiom": "universal", "platform": "ios", "size": "1024x1024"}],
        "info": {"author": "xcode", "version": 1}}, indent=2))
    print('icons done', round(MAXR, 1), 'safe radius scale', round(s, 4))


if __name__ == '__main__':
    main()
