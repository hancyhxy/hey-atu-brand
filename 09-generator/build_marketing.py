import os, sys, shutil, glob
sys.path.insert(0, os.path.dirname(__file__))
from common import *
from PIL import Image

B = os.path.join(ROOT, 'build')
M = os.path.join(KIT, '04-marketing')
SC = '../build/screens'
LG = '../HeyAtu-Brand-Kit/01-logo/svg'
ST = '../HeyAtu-Brand-Kit/05-states/svg'
IC = '../HeyAtu-Brand-Kit/02-app-icon/png'
PLUSH = '../site/assets-web/dog-wave-vest.webp'
HEAD = '<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="brand.css"><body>'


def wrap(w, h, bg, inner, dots='dots fade-b'):
    return HEAD + f'<div style="position:relative;width:{w}px;height:{h}px;background:{bg};overflow:hidden"><div class="{dots}"></div>{inner}</div>'


def glow(x, y, r, a=.22):
    return f'<div style="position:absolute;left:{x-r}px;top:{y-r}px;width:{2*r}px;height:{2*r}px;border-radius:50%;background:radial-gradient(rgba(217,128,58,{a}),transparent 65%)"></div>'


def notif(w=820, title='Atu', text='Your agent needs you. The draft is ready for review.', when='now', dark=True):
    bg = 'rgba(38,38,44,.92)' if dark else 'rgba(255,255,255,.95)'
    fg = '#F7F7F8' if dark else '#18181B'
    sub = '#A1A1AA' if dark else '#4F4F58'
    return (f'<div style="width:{w}px;padding:30px 34px;border-radius:44px;background:{bg};display:flex;gap:26px;align-items:center;'
            f'box-shadow:0 30px 80px rgba(0,0,0,.45),0 0 0 1.5px rgba(255,255,255,.08);font-family:-apple-system,system-ui,sans-serif">'
            f'<img src="{IC}/app-icon-dark-1024.png" style="width:92px;height:92px;border-radius:22px">'
            f'<div style="flex:1"><div style="display:flex;justify-content:space-between;font-size:30px;font-weight:600;color:{fg}"><span>{title}</span>'
            f'<span style="font-weight:400;color:{sub};font-size:26px">{when}</span></div>'
            f'<div style="font-size:29px;color:{fg};opacity:.9;margin-top:6px;line-height:1.3">{text}</div></div></div>')


T = {}
T['og-share-1200x630'] = (1200, 630, wrap(1200, 630, 'var(--ink)', glow(80, 40, 420) + f'''
  <img src="{LG}/atu-lockup-horizontal-on-dark.svg" style="position:absolute;left:80px;top:72px;height:56px">
  <div class="disp" style="position:absolute;left:78px;top:210px;font-size:64px;color:var(--paper)">Keep your AI<br>working from<br>your <span class="acc">phone</span>.</div>
  <div style="position:absolute;left:82px;top:500px;font-size:22px;color:var(--dim)">Your own AI, on your own computer.</div>
  <div class="card" style="left:800px;top:70px;width:330px;border-radius:44px"><img src="{SC}/light-todo-06.png"></div>'''))

T['og-share-light-1200x630'] = (1200, 630, wrap(1200, 630, 'var(--paper)', f'''
  <img src="{LG}/atu-lockup-horizontal-on-light.svg" style="position:absolute;left:80px;top:72px;height:56px">
  <div class="disp" style="position:absolute;left:78px;top:210px;font-size:64px;color:var(--ink2)">Keep your AI<br>working from<br>your <span class="acc">phone</span>.</div>
  <div style="position:absolute;left:82px;top:500px;font-size:22px;color:#4F4F58">Your own AI, on your own computer.</div>
  <div class="card" style="left:800px;top:70px;width:330px;border-radius:44px;box-shadow:0 30px 80px rgba(0,0,0,.18),0 0 0 1.5px rgba(0,0,0,.06)"><img src="{SC}/dark-updates-03.png"></div>''', 'dots dk fade-b'))

T['x-header-1500x500'] = (1500, 500, wrap(1500, 500, 'var(--ink)', glow(1500, 0, 520, .18) + f'''
  <div class="disp" style="position:absolute;left:480px;top:160px;font-size:50px;color:var(--paper)">Keep your AI working<br>from your <span class="acc">phone</span>.</div>
  <div class="label" style="position:absolute;left:484px;top:310px;font-size:18px;color:var(--dim)">heyatu.com · Mac · Linux</div>
  <div style="position:absolute;left:1260px;top:110px;display:flex;flex-direction:column;gap:18px">
    {''.join(f'<div style="display:flex;align-items:center;gap:14px"><img src="{ST}/atu-state-{s}.svg" style="height:40px"><span class="label" style="font-size:16px;color:{c}">{s}</span></div>' for s, c in [('idle', '#A1A1AA'), ('working', '#E8954F'), ('done', '#3FB950'), ('offline', '#71717A')])}
  </div>''', 'dots fade-r'))

T['linkedin-banner-1584x396'] = (1584, 396, wrap(1584, 396, 'var(--ink)', glow(1584, 0, 480, .18) + f'''
  <img src="{LG}/atu-lockup-horizontal-on-dark.svg" style="position:absolute;left:560px;top:96px;height:60px">
  <div class="disp" style="position:absolute;left:558px;top:196px;font-size:46px;color:var(--paper)">Your own AI, on your own <span class="acc">computer</span>.</div>
  <div class="label" style="position:absolute;left:562px;top:286px;font-size:16px;color:var(--dim)">Check in on your agent from your phone</div>''', 'dots fade-r'))

T['social-post-1080x1350'] = (1080, 1350, wrap(1080, 1350, 'var(--ink)', glow(1080, 1350, 700, .20) + f'''
  <div style="position:absolute;left:84px;top:96px;display:flex;align-items:center;gap:16px"><img src="{ST}/atu-state-done.svg" style="height:44px"><span class="label acc" style="font-size:24px">Done</span></div>
  <div class="disp" style="position:absolute;left:82px;top:172px;font-size:92px;color:var(--paper)">Hey, your<br>agent needs<br><span class="acc">you</span>.</div>
  <div style="position:absolute;left:84px;top:590px">{notif(912)}</div>
  <img src="{PLUSH}" style="position:absolute;right:20px;bottom:-60px;height:600px;filter:drop-shadow(0 30px 60px rgba(0,0,0,.5))">'''))

T['story-1080x1920'] = (1080, 1920, wrap(1080, 1920, 'var(--ink)', glow(0, 0, 700, .22) + f'''
  <img src="{LG}/atu-lockup-horizontal-on-dark.svg" style="position:absolute;left:90px;top:150px;height:64px">
  <div class="disp" style="position:absolute;left:88px;top:330px;font-size:88px;color:var(--paper)">Atu keeps<br>an eye on it.</div>
  <div style="position:absolute;left:90px;top:640px;width:900px;border-radius:40px;background:#16161A;box-shadow:0 0 0 1.5px var(--line);padding:24px 44px">
   {''.join(f'<div style="display:flex;align-items:center;gap:34px;padding:38px 0;border-bottom:{b}"><img src="{ST}/atu-state-{s}.svg" style="height:110px;width:150px;object-fit:contain"><div><div class="label" style="font-size:26px;color:{c}">{s}</div><div style="font-size:32px;color:#ECECF1;margin-top:10px">{t}</div></div></div>' for s, c, t, b in [('idle', '#A1A1AA', 'Waiting for you', '1.5px solid var(--line)'), ('working', '#E8954F', 'Editing 3 files on Studio Mac', '1.5px solid var(--line)'), ('done', '#3FB950', 'The draft is ready', '1.5px solid var(--line)'), ('offline', '#81818C', 'Your Mac is asleep', 'none')])}
  </div>
  <div class="label" style="position:absolute;left:90px;bottom:120px;font-size:24px;color:var(--dim)">heyatu.com</div>'''))

T['avatar-1024'] = (1024, 1024, HEAD + f'<div style="width:1024px;height:1024px;background:var(--ink);display:flex;align-items:center;justify-content:center"><img src="{LG}/atu-glyph-color.svg" style="width:600px"></div>')

T['release-card-1200x675'] = (1200, 675, wrap(1200, 675, 'var(--ink)', glow(1200, 675, 520, .16) + f'''
  <div style="position:absolute;left:80px;top:74px;display:flex;align-items:center;gap:16px"><img src="{LG}/atu-glyph-color.svg" style="height:40px"><span class="label" style="font-size:18px;color:var(--dim)">Changelog · v0.2 · Oct 2026</span></div>
  <div class="disp" style="position:absolute;left:78px;top:160px;font-size:62px;color:var(--paper)">Atu can now<br>message you <span class="acc">first</span>.</div>
  <div style="position:absolute;left:82px;top:350px;font-size:22px;line-height:1.9;color:#C9C9D1">
   <div>+ A note from Atu lands in the Agent chat</div><div>+ Send flight and keyboard close together</div><div>+ Sent images keep their 3:4 frame</div></div>
  <div class="card" style="left:820px;top:60px;width:300px;border-radius:40px"><img src="{SC}/dark-todo-06.png"></div>'''))

T['email-header-1200x400'] = (1200, 400, wrap(1200, 400, 'var(--paper)', f'''
  <img src="{LG}/atu-lockup-horizontal-on-light.svg" style="position:absolute;left:80px;top:80px;height:54px">
  <div class="disp" style="position:absolute;left:78px;top:200px;font-size:44px;color:var(--ink2)">Your agent kept working. <span class="acc">Here's what happened.</span></div>''', 'dots dk fade-r'))


def main():
    os.makedirs(os.path.join(ROOT, 'site/assets-web'), exist_ok=True)
    shutil.copy(os.path.expanduser('~/Documents/xinyihan/products/experiments/pi-remote-website/site/assets/img/dog-wave-vest.webp'),
                os.path.join(ROOT, 'site/assets-web/dog-wave-vest.webp'))
    with Renderer() as r:
        for name, (w, h, html) in T.items():
            hp = f'{B}/mk-{name}.html'
            write(hp, html)
            sub = 'social' if any(k in name for k in ['x-header', 'linkedin', 'social', 'story', 'avatar']) else ('web' if 'og' in name or 'email' in name else 'templates')
            out = f'{M}/{sub}/hey-atu-{name}.png'
            render_file(r, hp, out, w, h)
            Image.open(out).convert('RGB').save(out)
        r.svg(open(f'{KIT}/01-logo/svg/atu-glyph-color.svg').read(), f'{M}/web/favicon-512.png', 512, 512)
    # favicon set from the outline glyph (works on light and dark tabs)
    stickers = os.path.join(ROOT, '..', 'logo-directions/final/A7')
    for f in ['remix-light.png', 'remix-dark.png']:
        shutil.copy(os.path.join(stickers, f), f'{M}/stickers/' if os.path.isdir(f'{M}/stickers') else (os.makedirs(f'{M}/stickers') or f'{M}/stickers/'))
    for f in glob.glob(os.path.join(stickers, 'tiles/*.png')):
        os.makedirs(f'{M}/stickers/tiles', exist_ok=True); shutil.copy(f, f'{M}/stickers/tiles/')
    print('marketing done')


if __name__ == '__main__':
    main()
