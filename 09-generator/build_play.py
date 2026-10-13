import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import *
from PIL import Image

B = os.path.join(ROOT, 'build')
P = os.path.join(KIT, '03-stores/google-play')
SC = '../build/screens'   # relative to build/
ST = '../HeyAtu-Brand-Kit/05-states/svg'

HEAD = '<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="brand.css"><body>'

SHOTS = [
    # file, label, state, headline lines (accent wrapped in *), screen(s), sub
    ('01-agent', 'Agent', 'working', ['Your agent,', 'in your *pocket*.'], ['light-todo-06'], ''),
    ('02-updates', 'Updates', 'done', ['Know the moment', "it's *done*."], ['light-updates-03'], ''),
    ('03-follow-up', 'Follow up', 'idle', ['Ask about', '*any* update.'], ['light-updates-11'], ''),
    ('04-todo', 'Todo', 'done', ['Plan the day', 'with *Atu*.'], ['light-todo-00'], ''),
    ('05-pair', 'Pair', 'idle', ['One scan.', "You're *in*."], ['light-pair-03'], ''),
    ('06-your-computer', 'Your computer', 'working', ['Your AI, on your', '*own* computer.'], ['light-pair-07'], ''),
    ('07-dark', 'Light or dark', 'offline', ['Light or dark.', 'Same *Atu*.'], ['light-todo-12', 'dark-todo-06'], ''),
]


def hl(lines):
    out = []
    for l in lines:
        parts = l.split('*')
        out.append(''.join(f'<span class="acc">{p}</span>' if i % 2 else p for i, p in enumerate(parts)))
    return '<br>'.join(out)


def shot_html(label, state, lines, screens):
    cards = ''
    if len(screens) == 1:
        cards = f'<div class="card" style="left:110px;top:520px;width:860px"><img src="{SC}/{screens[0]}.png"></div>'
    else:
        cards = (f'<div class="card" style="left:70px;top:600px;width:560px;opacity:.96"><img src="{SC}/{screens[0]}.png"></div>'
                 f'<div class="card" style="left:450px;top:520px;width:560px"><img src="{SC}/{screens[1]}.png"></div>')
    return HEAD + f'''
<div style="position:relative;width:1080px;height:1920px;background:var(--ink);overflow:hidden">
  <div class="dots fade-b"></div>
  <div style="position:absolute;left:-260px;top:-300px;width:900px;height:900px;border-radius:50%;background:radial-gradient(rgba(217,128,58,.22),transparent 65%)"></div>
  <div style="position:absolute;left:90px;top:118px;display:flex;align-items:center;gap:18px">
    <img src="{ST}/atu-state-{state}.svg" style="height:46px">
    <span class="label acc" style="font-size:26px">{label}</span>
  </div>
  <div class="disp" style="position:absolute;left:88px;top:196px;font-size:84px;color:var(--paper)">{hl(lines)}</div>
  {cards}
</div>'''


def feature_html():
    return HEAD + f'''
<div style="position:relative;width:1024px;height:500px;background:var(--caramel);overflow:hidden">
  <div class="dots dk fade-r"></div>
  <div style="position:absolute;left:96px;top:118px;width:470px">
    <div class="label" style="font-size:15px;color:rgba(14,14,16,.7);margin-bottom:22px">Hey Atu</div>
    <div class="disp" style="font-size:46px;color:var(--ink)">Keep your AI<br>working from<br>your phone.</div>
    <div style="font-size:16px;color:rgba(14,14,16,.78);margin-top:22px;line-height:1.5">Your own AI, on your own computer.</div>
  </div>
  <div class="card" style="left:560px;top:84px;width:200px;border-radius:30px;box-shadow:0 24px 60px rgba(60,30,0,.35)"><img src="{SC}/light-updates-03.png"></div>
  <div class="card" style="left:722px;top:44px;width:220px;border-radius:32px;box-shadow:0 24px 60px rgba(60,30,0,.45)"><img src="{SC}/dark-todo-06.png"></div>
</div>'''


def main():
    with Renderer() as r:
        for name, label, state, lines, screens, sub in SHOTS:
            hp = f'{B}/play-{name}.html'
            write(hp, shot_html(label, state, lines, screens))
            out = f'{P}/03-phone-screenshots/hey-atu-phone-{name}.png'
            render_file(r, hp, out, 1080, 1920)
            Image.open(out).convert('RGB').save(out)
        hp = f'{B}/play-feature.html'
        write(hp, feature_html())
        out = f'{P}/02-feature-graphic/feature-graphic-1024x500.png'
        render_file(r, hp, out, 1024, 500)
        im = Image.open(out).convert('RGB'); im.save(out); im.save(out.replace('.png', '.jpg'), quality=95)
    print('play done')


if __name__ == '__main__':
    main()
