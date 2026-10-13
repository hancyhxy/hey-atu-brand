import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import *
from PIL import Image

B = os.path.join(ROOT, 'build')
O = os.path.join(KIT, '06-app-samples')
IC = '../HeyAtu-Brand-Kit/02-app-icon'
LG = '../HeyAtu-Brand-Kit/01-logo/svg'
SC = '../build/screens'
HEAD = '<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="brand.css"><style>.sys{font-family:Roboto,-apple-system,system-ui,sans-serif}</style><body>'

SB = ('<div class="sys" style="display:flex;justify-content:space-between;align-items:center;padding:18px 30px 0;font-size:22px;color:{c};font-weight:500">'
      '<span>9:41</span><span style="display:flex;gap:10px;align-items:center">'
      '<svg width="22" height="18" viewBox="0 0 22 18"><path d="M1 17L21 1V17Z" fill="{c}"/></svg>'
      '<svg width="24" height="18" viewBox="0 0 24 18"><path d="M12 17L1 5A16 16 0 0 1 23 5Z" fill="{c}"/></svg>'
      '<svg width="14" height="22" viewBox="0 0 14 22"><rect x="1" y="3" width="12" height="18" rx="2" fill="{c}"/><rect x="4" y="0" width="6" height="3" fill="{c}"/></svg></span></div>')

GENERIC = ['#4C8BF5', '#34A853', '#F4B400', '#EA4335', '#7E57C2', '#00ACC1', '#FF7043', '#5C6BC0', '#26A69A', '#8D6E63', '#EC407A', '#78909C']
MARKS = ['<circle cx="50" cy="50" r="18" fill="#fff"/>', '<rect x="32" y="32" width="36" height="36" rx="6" fill="#fff"/>', '<path d="M50 30L70 68H30Z" fill="#fff"/>',
         '<rect x="30" y="44" width="40" height="12" rx="6" fill="#fff"/>', '<path d="M30 50h40M50 30v40" stroke="#fff" stroke-width="10" stroke-linecap="round"/>', '<circle cx="50" cy="50" r="20" fill="none" stroke="#fff" stroke-width="9"/>']


def gicon(i, size, shape='circle', themed=False):
    r = '50%' if shape == 'circle' else '26%'
    bg = '#3B3A4A' if themed else GENERIC[i % len(GENERIC)]
    mark = MARKS[i % len(MARKS)].replace('#fff', '#C9C2FF' if themed else '#fff')
    return f'<div style="width:{size}px;height:{size}px;border-radius:{r};background:{bg};overflow:hidden"><svg viewBox="0 0 100 100" width="{size}" height="{size}">{mark}</svg></div>'


def atu_icon(size, shape='circle', themed=False):
    r = {'circle': '50%', 'squircle': '34%', 'rounded': '22%', 'teardrop': '50% 50% 50% 18%'}[shape]
    if themed:
        inner = f'<img src="{IC}/svg/android-adaptive-monochrome-432.svg" style="width:150%;height:150%;margin:-25%;filter:invert(83%) sepia(20%) saturate(800%) hue-rotate(205deg)">'
        bg = '#3B3A4A'
    else:
        inner = f'<img src="{IC}/svg/android-adaptive-foreground-432.svg" style="width:150%;height:150%;margin:-25%">'
        bg = '#0E0E10'
    return f'<div style="width:{size}px;height:{size}px;border-radius:{r};background:{bg};overflow:hidden">{inner}</div>'


def phone(inner, w=480, h=1040, bg='#000', radius=64, frame='#1B1B1F'):
    return (f'<div style="width:{w+28}px;height:{h+28}px;border-radius:{radius+14}px;background:{frame};padding:14px;box-shadow:0 40px 100px rgba(0,0,0,.35)">'
            f'<div style="position:relative;width:{w}px;height:{h}px;border-radius:{radius}px;overflow:hidden;background:{bg}">{inner}</div></div>')


def home(themed=False):
    wall = 'linear-gradient(160deg,#2A3557 0%,#1F2D4F 45%,#3A2A2A 100%)'
    cells = []
    for i in range(16):
        if i == 9:
            cells.append(f'<div style="display:flex;flex-direction:column;align-items:center;gap:10px">{atu_icon(92, "circle", themed)}<span class="sys" style="font-size:19px;color:#fff">Hey Atu</span></div>')
        else:
            cells.append(f'<div style="display:flex;flex-direction:column;align-items:center;gap:10px">{gicon(i, 92, "circle", themed)}<span class="sys" style="font-size:19px;color:#fff;opacity:.85">App</span></div>')
    grid = f'<div style="position:absolute;left:34px;right:34px;top:420px;display:grid;grid-template-columns:repeat(4,1fr);row-gap:40px">{"".join(cells)}</div>'
    clock = '<div class="sys" style="position:absolute;left:44px;top:120px;color:#fff;font-size:120px;font-weight:300;line-height:1">9:41</div><div class="sys" style="position:absolute;left:48px;top:250px;color:#fff;opacity:.8;font-size:24px">Tue, Oct 13</div>'
    search = '<div style="position:absolute;left:40px;right:40px;bottom:46px;height:84px;border-radius:42px;background:rgba(255,255,255,.18)"></div>'
    return phone(SB.format(c='#fff') + clock + grid + search, bg=wall)


def shade():
    n = ('<div class="sys" style="margin:0 22px;border-radius:34px;background:#2B2B33;padding:24px 26px;color:#ECECF1">'
         '<div style="display:flex;align-items:center;gap:12px;font-size:19px;color:#ADADB8">'
         f'<img src="{IC}/svg/android-notification-24.svg" style="width:26px;height:26px;filter:invert(62%) sepia(60%) saturate(500%) hue-rotate(345deg)"> Hey Atu · now</div>'
         '<div style="display:flex;gap:18px;margin-top:14px;align-items:center"><div style="flex:1"><div style="font-size:24px;font-weight:600">Atu</div>'
         '<div style="font-size:22px;color:#C9C9D1;margin-top:4px;line-height:1.35">Your agent needs you. The draft is ready for review.</div></div>'
         f'<img src="{IC}/png/app-icon-dark-1024.png" style="width:72px;height:72px;border-radius:50%"></div>'
         '<div style="display:flex;gap:30px;margin-top:20px;font-size:20px;color:#E8954F;font-weight:600"><span>Open</span><span>Reply</span></div></div>')
    sb = SB.format(c='#ECECF1').replace('<span>9:41</span>', f'<span style="display:flex;gap:12px;align-items:center">9:41 <img src="{IC}/svg/android-notification-24.svg" style="width:24px;height:24px"></span>')
    qs = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:30px 22px 26px">' + ''.join('<div style="height:84px;border-radius:42px;background:#34343C"></div>' for _ in range(4)) + '</div>'
    return phone(sb + qs + n, bg='#16161A')


def splash():
    return phone(SB.format(c='#ECECF1') + f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center"><img src="{LG}/atu-glyph-color.svg" style="width:200px"></div>', bg='#0E0E10')


def board(title_items, w, h, bg='#F7F7F8', fg='#18181B'):
    cols = ''.join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:30px">{el}<div class="label" style="font-size:20px;color:{fg};opacity:.7">{t}</div></div>' for t, el in title_items)
    return HEAD + f'<div style="width:{w}px;height:{h}px;background:{bg};display:flex;align-items:center;justify-content:center;gap:70px">{cols}</div>'


def masks():
    items = [(s, atu_icon(220, s)) for s in ['circle', 'squircle', 'rounded', 'teardrop']] + [('themed', atu_icon(220, 'circle', True))]
    return board(items, 1900, 560)


def ios_pair():
    lock = (SB.format(c='#fff') + '<div class="sys" style="position:absolute;top:150px;width:100%;text-align:center;color:#fff;font-size:120px;font-weight:600">9:41</div>'
            '<div class="sys" style="position:absolute;left:20px;right:20px;top:420px;border-radius:30px;background:rgba(255,255,255,.72);backdrop-filter:blur(20px);padding:20px;display:flex;gap:16px;align-items:center">'
            f'<img src="{IC}/ios/AppIcon.appiconset/AppIcon-1024.png" style="width:70px;height:70px;border-radius:16px"><div style="flex:1"><div style="display:flex;justify-content:space-between;font-size:22px;font-weight:600;color:#111"><span>Atu</span><span style="font-weight:400;color:#555;font-size:19px">now</span></div>'
            '<div style="font-size:21px;color:#222;margin-top:3px">Your agent needs you. The draft is ready for review.</div></div></div>')
    wall = 'linear-gradient(170deg,#9FB3D9,#5E73A8 60%,#2A3557)'
    cells = []
    for i in range(16):
        if i == 6:
            cells.append(f'<div style="display:flex;flex-direction:column;align-items:center;gap:8px"><img src="{IC}/ios/AppIcon.appiconset/AppIcon-1024.png" style="width:92px;height:92px;border-radius:22px"><span class="sys" style="font-size:18px;color:#fff">Hey Atu</span></div>')
        else:
            cells.append(f'<div style="display:flex;flex-direction:column;align-items:center;gap:8px">{gicon(i, 92, "sq")}<span class="sys" style="font-size:18px;color:#fff;opacity:.85">App</span></div>')
    home_i = SB.format(c='#fff') + f'<div style="position:absolute;left:34px;right:34px;top:110px;display:grid;grid-template-columns:repeat(4,1fr);row-gap:36px">{"".join(cells)}</div>'
    return board([('iOS home', phone(home_i, bg=wall)), ('iOS lock screen', phone(lock, bg=wall))], 1400, 1300)


def logo_vs_mascot():
    def card(src, w=360):
        return f'<div style="width:{w}px;border-radius:46px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.18),0 0 0 1.5px rgba(0,0,0,.06)"><img src="{SC}/{src}.png" style="width:100%;display:block"></div>'
    left = (f'<div style="display:flex;gap:26px;align-items:center">{atu_icon(150, "squircle")}'
            f'<img src="{IC}/ios/AppIcon.appiconset/AppIcon-1024.png" style="width:150px;border-radius:34px"></div>')
    return HEAD + f'''<div style="width:1800px;height:1000px;background:#F7F7F8;display:grid;grid-template-columns:1fr 1fr">
  <div style="padding:80px;border-right:1.5px solid #DEDEE3"><div class="label" style="font-size:22px;color:#D9803A">Outside the app · Logo</div>
   <div class="disp" style="font-size:52px;color:#18181B;margin:22px 0 60px">Icon, notifications,<br>store, website.</div>{left}
   <div style="margin-top:60px;display:flex;gap:20px;align-items:center"><img src="{LG}/atu-lockup-horizontal-on-light.svg" style="height:70px"></div></div>
  <div style="padding:80px;position:relative;overflow:hidden"><div class="label" style="font-size:22px;color:#D9803A">Inside the app · Plush</div>
   <div class="disp" style="font-size:52px;color:#18181B;margin:22px 0 40px">Agent header,<br>states, sleep screen.</div>
   <div style="display:flex;gap:30px">{card('light-todo-06', 330)}{card('dark-todo-06', 330)}</div></div></div>'''


def main():
    pages = {
        'android-touchpoints': (board([('Home · circle mask', home()), ('Themed icons', home(True)), ('Notification', shade()), ('Splash', splash())], 2600, 1400), 2600, 1400),
        'android-icon-masks': (masks(), 1900, 560),
        'ios-touchpoints': (ios_pair(), 1400, 1300),
        'logo-vs-mascot': (logo_vs_mascot(), 1800, 1000),
    }
    with Renderer() as r:
        for n, (html, w, h) in pages.items():
            hp = f'{B}/sample-{n}.html'; write(hp, html)
            out = f'{O}/hey-atu-{n}.png'; render_file(r, hp, out, w, h, wait=700)
            Image.open(out).convert('RGB').save(out)
    print('samples done')


if __name__ == '__main__':
    main()
