import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import *
from build_play import SHOTS, hl, HEAD, SC, ST
from PIL import Image

B = os.path.join(ROOT, 'build')
AS = os.path.join(KIT, '03-stores/app-store')


def iphone_html(label, state, lines, screens, W=1320, H=2868):
    k = W / 1080
    if len(screens) == 1:
        cards = f'<div class="card" style="left:{130}px;top:{640}px;width:{1060}px;border-radius:{84}px"><img src="{SC}/{screens[0]}.png"></div>'
    else:
        cards = (f'<div class="card" style="left:80px;top:760px;width:700px;border-radius:64px;opacity:.96"><img src="{SC}/{screens[0]}.png"></div>'
                 f'<div class="card" style="left:540px;top:640px;width:700px;border-radius:64px"><img src="{SC}/{screens[1]}.png"></div>')
    return HEAD + f'''
<div style="position:relative;width:{W}px;height:{H}px;background:var(--ink);overflow:hidden">
  <div class="dots fade-b" style="background-size:{28*k:.0f}px {28*k:.0f}px"></div>
  <div style="position:absolute;left:-320px;top:-360px;width:1100px;height:1100px;border-radius:50%;background:radial-gradient(rgba(217,128,58,.22),transparent 65%)"></div>
  <div style="position:absolute;left:112px;top:170px;display:flex;align-items:center;gap:22px">
    <img src="{ST}/atu-state-{state}.svg" style="height:56px"><span class="label acc" style="font-size:32px">{label}</span></div>
  <div class="disp" style="position:absolute;left:108px;top:262px;font-size:104px;color:var(--paper)">{hl(lines)}</div>
  {cards}
</div>'''


IPAD = [
    ('01-updates', 'Updates', 'done', ["Know the moment it's *done*."], 'pad-light-07'),
    ('02-follow-up', 'Follow up', 'idle', ['Ask about *any* update.'], 'pad-light-08'),
    ('03-todo', 'Todo', 'done', ['Plan the day with *Atu*.'], 'pad-dark-09'),
    ('04-dark', 'Light or dark', 'offline', ['Same *Atu*, after dark.'], 'pad-dark-07'),
]


def ipad_html(label, state, lines, screen, W=2752, H=2064):
    return HEAD + f'''
<div style="position:relative;width:{W}px;height:{H}px;background:var(--ink);overflow:hidden">
  <div class="dots fade-b" style="background-size:40px 40px"></div>
  <div style="position:absolute;left:-400px;top:-500px;width:1500px;height:1500px;border-radius:50%;background:radial-gradient(rgba(217,128,58,.2),transparent 65%)"></div>
  <div style="position:absolute;left:226px;top:150px;display:flex;align-items:center;gap:26px">
    <img src="{ST}/atu-state-{state}.svg" style="height:64px"><span class="label acc" style="font-size:38px">{label}</span></div>
  <div class="disp" style="position:absolute;left:222px;top:250px;font-size:120px;color:var(--paper)">{hl(lines)}</div>
  <div class="card" style="left:226px;top:520px;width:2300px;border-radius:70px"><img src="{SC}/{screen}.png"></div>
</div>'''


def main():
    with Renderer() as r:
        for name, label, state, lines, screens, sub in SHOTS:
            hp = f'{B}/as-iphone-{name}.html'; write(hp, iphone_html(label, state, lines, screens))
            big = f'{AS}/02-iphone-6.9in-1320x2868/hey-atu-iphone-{name}.png'
            render_file(r, hp, big, 1320, 2868)
            im = Image.open(big).convert('RGB'); im.save(big)
            med = f'{AS}/03-iphone-6.3in-1206x2622/hey-atu-iphone-{name}.png'
            os.makedirs(os.path.dirname(med), exist_ok=True)
            im.resize((1206, 2622), Image.LANCZOS).save(med)
        for name, label, state, lines, screen in IPAD:
            hp = f'{B}/as-ipad-{name}.html'; write(hp, ipad_html(label, state, lines, screen))
            out = f'{AS}/04-ipad-13in-2752x2064/hey-atu-ipad-{name}.png'
            render_file(r, hp, out, 2752, 2064)
            Image.open(out).convert('RGB').save(out)
    # App Store icon: 1024, opaque, square (Apple applies the mask)
    os.makedirs(f'{AS}/01-app-icon', exist_ok=True)
    Image.open(f'{KIT}/02-app-icon/ios/AppIcon.appiconset/AppIcon-1024.png').convert('RGB').save(f'{AS}/01-app-icon/app-store-icon-1024.png')
    print('app store done')


if __name__ == '__main__':
    main()
