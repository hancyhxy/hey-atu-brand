import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from common import *

T = json.load(open(f'{KIT}/07-fonts-and-tokens/tokens.json'))
L = '01-logo'; A = '02-app-icon'; P = '03-stores/google-play'; M = '04-marketing'; S = '05-states'; X = '06-app-samples'; F = '07-fonts-and-tokens/fonts'; SRC = '08-source'


def sw(name, hexv, use, dark=False):
    r, g, b = (int(hexv[i:i + 2], 16) for i in (1, 3, 5))
    fg = '#fff' if dark else '#18181B'
    return (f'<div class="sw"><div class="chip" style="background:{hexv};color:{fg}"><b>{name}</b></div>'
            f'<div class="meta"><code>{hexv}</code><br><span>RGB {r} {g} {b}</span><p>{use}</p></div></div>')


def tile(src, cap, bg='#F7F7F8', h=180, cls=''):
    return f'<figure class="tile {cls}"><div class="box" style="background:{bg}"><img src="{src}" style="max-height:{h}px"></div><figcaption>{cap}</figcaption></figure>'


def dont(inner, cap, bg='#F7F7F8'):
    return f'<figure class="tile dont"><div class="box" style="background:{bg}">{inner}</div><figcaption>✕ {cap}</figcaption></figure>'


def sec(n, title, lede, body):
    return f'<section id="s{n}"><div class="num">{n:02d}</div><h2>{title}</h2><p class="lede">{lede}</p>{body}</section>'


def build():
    b = T['brand']
    colors = ''.join([
        sw('Ink', '#0E0E10', b['ink']['use'], True), sw('Paper', '#F7F7F8', b['paper']['use']),
        sw('Caramel', '#D9803A', b['caramel']['use'], True), sw('Caramel Light', '#E8954F', b['caramel-light']['use'], True),
        sw('Navy', '#1F2D4F', b['navy']['use'], True), sw('White', '#FFFFFF', b['white']['use']),
        sw('Ink 2', '#18181B', b['ink-2']['use'], True), sw('Cream', '#FFFDF9', b['cream']['use'])])
    ui = ''.join(f'<tr><td>{k}</td><td><i style="background:{T["app-ui-light"][k]}"></i><code>{T["app-ui-light"][k]}</code></td><td><i style="background:{T["app-ui-dark"][k]}"></i><code>{T["app-ui-dark"][k]}</code></td></tr>' for k in T['app-ui-light'])
    states = ''.join(f'''<div class="state"><div class="pair"><img src="{S}/svg/atu-state-{s}.svg" class="g"><span>↔</span><img src="{SRC}/mascot-{gif}.gif" class="m"></div>
      <div class="label" style="color:{c}">{s}</div><p>{t}</p></div>''' for s, gif, c, t in [
        ('idle', 'idle', '#71717A', '默认状态，等你发下一条消息。'), ('working', 'working', '#D9803A', 'Agent 正在干活：眼睛往下看，面前放一台电脑。'),
        ('done', 'done-laugh', '#218739', '任务完成：笑眼，加一颗焦糖色星星。'), ('offline', 'offline', '#74747E', '电脑休眠或断开：闭眼、整体变灰，加 z z。')])
    shots = ''.join(f'<img src="{P}/03-phone-screenshots/hey-atu-phone-{n}.png">' for n in ['01-agent', '02-updates', '03-follow-up', '04-todo', '05-pair', '06-your-computer', '07-dark'])
    mk = lambda f, cap: f'<figure class="mk"><img src="{M}/{f}"><figcaption>{cap}</figcaption></figure>'

    S_ = []
    S_.append(sec(1, '品牌概述', 'Hey Atu 让你在手机上照看自己电脑上的 AI agent。Atu 是那只 Jack Russell 玩偶：它替你盯着 agent，有事就叫你。',
        '''<div class="cols3"><div class="card"><h4>一句话</h4><p class="big">Your own AI, on your own computer.</p><p>沿用官网的 slogan。产品利益点就三件事：<b>数据在自己电脑上、在手机上随时接上、有一只狗替你看着</b>。</p></div>
        <div class="card"><h4>性格</h4><ul><li><b>冷静可靠</b>：像一个靠谱的工程工具，不浮夸。</li><li><b>温暖陪伴</b>：狗的存在让等待变得不焦虑。</li><li><b>工程师审美</b>：等宽字体、真实界面、克制的配色。</li></ul></div>
        <div class="card"><h4>说话方式</h4><ul><li>短句、平实、具体：<i>“One scan. You're in.”</i></li><li>说结果，不说形容词：<i>“Know the moment it's done.”</i></li><li>不用 Best、#1、Revolutionary 这类词，不用 emoji 堆砌。</li></ul></div></div>'''))
    S_.append(sec(2, 'Logo 系统', '同一个狗头轮廓，配 4 种表现。默认用彩色版；遇到浅底、小尺寸或只能用单色的场景，就换到对应版本。',
        '<div class="grid4">' + tile(f'{L}/svg/atu-glyph-color.svg', '<b>彩色主标</b>：深色底的默认版本', '#0E0E10') +
        tile(f'{L}/svg/atu-glyph-outline.svg', '<b>描边版</b>：浅色底、白色底、16–32px') +
        tile(f'{L}/svg/atu-glyph-mono-ink.svg', '<b>单色版</b>：单色印刷、压印、系统图标') +
        tile(f'{L}/svg/atu-glyph-line-ink.svg', '<b>线条版</b>：刺绣、线稿、周边') + '</div>' +
        '''<table class="t"><tr><th>场景</th><th>用哪个</th></tr><tr><td>深色底（#0E0E10、Navy、照片暗部）</td><td>彩色主标</td></tr><tr><td>浅色底（#F7F7F8、白、奶油）</td><td>描边版（白头必须有黑描边托住）</td></tr>
        <tr><td>焦糖底</td><td>单色白（不要用彩色版，焦糖耳会和底色融在一起）</td></tr><tr><td>只能用 1 种颜色（系统通知、压印、传真）</td><td>单色版</td></tr><tr><td>≤16px（favicon、状态栏）</td><td>单色版或描边版</td></tr></table>'''))
    S_.append(sec(3, '构成、安全区与最小尺寸', '整个狗头由 6 个椭圆组成：头、两只耳朵、眼斑、两只眼睛。眼斑是头内的一条连续椭圆弧。不要重新手绘，所有文件都由同一份几何参数生成（<code>src/geom.py</code>）。',
        '<div class="cols2">' + tile(f'{L}/guides/atu-construction.svg', '构成：6 个椭圆，眼斑被裁切在头部范围内', '#0E0E10', 300) +
        tile(f'{L}/guides/atu-clearspace.svg', '安全区：四周至少留 <b>X = 1 个眼睛的高度</b>', '#0E0E10', 300) + '</div>' +
        '''<table class="t"><tr><th>版本</th><th>屏幕最小</th><th>印刷最小</th></tr><tr><td>彩色主标</td><td>24 px 高</td><td>8 mm</td></tr><tr><td>描边版 / 单色版</td><td>16 px 高</td><td>5 mm</td></tr><tr><td>横版组合标</td><td>96 px 宽</td><td>25 mm</td></tr></table>'''))
    S_.append(sec(4, '组合标志与字标', '字标 “Hey Atu” 用 <b>JetBrains Mono Medium（500）</b>，和 App 内的字体一致。文件里的字已经转成路径，打开时不需要装字体。',
        '<div class="cols2">' + tile(f'{L}/svg/atu-lockup-horizontal-on-dark.svg', '横版 · 深色底', '#0E0E10', 110) + tile(f'{L}/svg/atu-lockup-horizontal-on-light.svg', '横版 · 浅色底（描边狗头）', '#F7F7F8', 110) +
        tile(f'{L}/svg/atu-lockup-stacked-on-dark.svg', '竖版 · 深色底', '#0E0E10', 220) + tile(f'{L}/svg/atu-lockup-stacked-on-light.svg', '竖版 · 浅色底', '#F7F7F8', 220) + '</div>' +
        '<p class="note">比例关系：大写字母高度 = 狗头高度 × 0.40；狗头和字之间的间距 = 狗头高度 × 0.26；字的竖向中心对齐头部椭圆的圆心。字间距 −1%。品牌名一律写成 <b>Hey Atu</b>，不用全大写 “HEY ATU”，也不用官网页脚的 Instrument Serif 斜体，这一处需要官网同步更新。</p>'))
    img = lambda f, st='': f'<img src="{L}/svg/{f}" style="height:110px;{st}">'
    S_.append(sec(5, '错误用法', '下面这些都会让 Atu 不再是同一只狗。',
        '<div class="grid4">' + dont(f'<img src="{L}/guides/misuse/atu-dont-recolor.svg" style="height:110px">', '改耳朵颜色', '#0E0E10') +
        dont(f'<img src="{L}/guides/misuse/atu-dont-face.svg" style="height:110px">', '加鼻子、嘴巴、腮红', '#0E0E10') +
        dont(img('atu-glyph-color.svg', 'transform:scaleX(1.35)'), '拉伸或压扁', '#0E0E10') +
        dont(img('atu-glyph-color.svg', 'transform:rotate(-18deg)'), '旋转、歪头', '#0E0E10') +
        dont(img('atu-glyph-color.svg'), '彩色版放在焦糖底上', '#D9803A') +
        dont(img('atu-glyph-color.svg'), '彩色白头直接放在浅底上，不加描边', '#F7F7F8') +
        dont(f'<img src="{L}/guides/misuse/atu-dont-gradient.svg" style="height:110px">', '加渐变、加阴影、加 3D', '#0E0E10') +
        dont(f'<div style="width:150px;height:150px;border-radius:34px;background:#0E0E10;overflow:hidden;position:relative"><img src="{L}/svg/atu-glyph-color.svg" style="position:absolute;height:170px;left:30px;top:40px"></div>', '把狗头裁切成“从角落探头”（旧版 E）') + '</div>'))
    S_.append(sec(6, 'Logo 和玩偶怎么分工', 'Logo 是数字符号，只出现在 App 外面；玩偶 Atu（穿抓绒马甲的那只）是角色，只出现在 App 里面和视频里。两者靠同样的焦糖耳、右眼斑和黑眼睛，让人认出是同一只狗。',
        f'<img class="wide" src="{X}/hey-atu-logo-vs-mascot.png">' +
        '''<table class="t"><tr><th></th><th>Logo（狗头符号）</th><th>玩偶 Atu</th></tr><tr><td>出现位置</td><td>App 图标、系统通知、应用商店、官网导航、分享卡片、社媒头像</td><td>Agent 页顶部 80pt 动画、抽屉里的 Agents 行、离线睡觉页、视频、宣发里的角色客串</td></tr>
        <tr><td>不要放在</td><td>App 内的界面里（Chats 页、会话列表都不放 logo）</td><td>App 图标、系统通知、单色场景</td></tr></table>'''))
    S_.append(sec(7, '四个状态', 'Logo 的 4 个状态和 App 里玩偶的 4 个状态一一对应，用在通知、Live Activity、社媒和状态面板里。不设 “needs-you” 状态；离线用闭眼，不用 X 眼。',
        f'<div class="states">{states}</div>'))
    S_.append(sec(8, '色彩', '用色比例大约是 Ink 60%、Paper 25%、Caramel 10%、Navy 5%。焦糖色是唯一的强调色，一个画面里只强调一处。',
        f'<div class="ratio"><i style="flex:60;background:#0E0E10"></i><i style="flex:25;background:#F7F7F8"></i><i style="flex:10;background:#D9803A"></i><i style="flex:5;background:#1F2D4F"></i></div><div class="sws">{colors}</div>'
        f'<h3>App 界面颜色（来自 <code>NativeAppearance.swift</code>，App 团队维护，这里只做对照）</h3><table class="t ui"><tr><th>token</th><th>Light</th><th>Dark</th></tr>{ui}</table>'
        '<p class="note">App 里 tab 选中色是 <code>#D97757</code>（偏珊瑚色），品牌焦糖色是 <code>#D9803A</code>。两个都保留，但宣发物料只用品牌焦糖色。</p>'))
    S_.append(sec(9, '字体', '三种字体，各管一件事。全部是 SIL OFL 开源授权，文件在 <code>07-fonts-and-tokens/fonts/</code>。',
        f'''<div class="type"><div><div class="label">Display · Departure Mono</div><div class="disp" style="font-size:56px">Keep your AI working</div><p>只用在宣发大标题。像素风等宽字体，和官网首屏一致。每段 ≤ 2 行，强调词用焦糖色。</p></div>
        <div><div class="label">Brand / UI · JetBrains Mono</div><div style="font-family:JBM;font-weight:500;font-size:44px">Hey Atu · 9:41 · working</div><p>字标、小标签（全大写，字间距 +16%）、数字、产品界面。字重 400 / 500 / 600。</p></div>
        <div><div class="label">Body · System sans</div><div style="font-family:-apple-system,Roboto,sans-serif;font-size:30px">Your own AI, on your own computer.</div><p>宣发里较长的正文。iOS 用 SF Pro，Android 用 Roboto，网页用系统字体。</p></div></div>
        <table class="t"><tr><th>层级</th><th>字体</th><th>@1080 宽</th><th>@1200 宽（OG 图）</th></tr><tr><td>H1</td><td>Departure Mono</td><td>84–92</td><td>64</td></tr><tr><td>Label</td><td>JetBrains Mono 600，全大写，字间距 +16%</td><td>24–26</td><td>18</td></tr><tr><td>Body</td><td>System / JetBrains Mono 400</td><td>28–32</td><td>22</td></tr></table>'''))
    S_.append(sec(10, '图形元素', '只用 4 种元素，所有宣发都由它们组合出来。',
        '''<div class="cols4"><div class="card ink"><div class="dots-demo"></div><h4>点阵</h4><p>28px 网格、1.6px 圆点，透明度 13%，往一侧渐隐，带一点终端质感。</p></div>
        <div class="card ink"><div class="glow-demo"></div><h4>焦糖光晕</h4><p>放在一个角上，透明度 16–22%。每张图只放一处。</p></div>
        <div class="card ink"><div class="label" style="color:#D9803A;display:flex;gap:10px;align-items:center"><img src="05-states/svg/atu-state-working.svg" style="height:28px">AGENT</div><h4>状态标签</h4><p>状态狗头配一个全大写的 JetBrains Mono 词，放在标题上面。</p></div>
        <div class="card ink"><div style="height:70px;border-radius:18px;background:#F7F7F8;box-shadow:0 0 0 1.5px rgba(255,255,255,.1)"></div><h4>产品卡片</h4><p>真实 App 界面，圆角 64px（以 1080 宽为基准），1.5px 白色描边加深色阴影，不加手机外框。</p></div></div>'''))
    S_.append(sec(11, '图像风格', '以产品界面为主角，Atu 偶尔客串。整体是科技工具的气质，不做咖啡馆、生活方式那一类摆拍。',
        f'''<div class="cols2"><div class="card"><h4>✓ 这样用</h4><ul><li>真实 App 界面（本包 <code>08-source/app-screens/</code>，浅色和深色都有）。</li><li>玩偶只用穿抓绒马甲的那只，抠图，放在纯色或点阵底上。</li><li>一张图只讲一件事，大标题加一张界面。</li></ul><div class="row"><img src="{SRC}/website/dog-wave-vest.webp" style="height:180px"><img src="{SRC}/app-screens/light-updates-03.png" style="height:180px;border-radius:20px"></div></div>
        <div class="card"><h4>✕ 不要这样</h4><ul><li>咖啡、拿铁、面条、绿植这类生活道具，以及暖色滤镜。</li><li>图库照片、人物手持手机、手指点击。</li><li>同一画面里塞多套服装的玩偶，或者 AI 生成的伪界面。</li></ul><div class="row" style="opacity:.55;filter:grayscale(.3)"><img src="{SRC}/website/dog-latte.webp" style="height:180px"><img src="{SRC}/website/dog-noodles.webp" style="height:180px"></div><p class="note">官网上这些素材可以继续用，但新的宣发物料不再采用。</p></div></div>'''))
    S_.append(sec(12, 'App 图标与系统触点', '图标统一是 Ink 底加彩色狗头。Android 用 adaptive icon，并且提供 monochrome 层，所以支持 Android 13 起的主题图标。',
        f'<img class="wide" src="{X}/hey-atu-android-touchpoints.png"><img class="wide" src="{X}/hey-atu-android-icon-masks.png"><div class="cols2"><img class="wide" src="{X}/hey-atu-ios-touchpoints.png"><div>' +
        '''<table class="t"><tr><th>交付物</th><th>文件</th></tr><tr><td>Android adaptive（矢量）</td><td><code>android/res/drawable/ic_launcher_foreground.xml</code> + <code>ic_launcher_monochrome.xml</code> + <code>values/ic_launcher_background.xml</code></td></tr>
        <tr><td>Android 旧版启动图标</td><td><code>mipmap-mdpi…xxxhdpi/ic_launcher(.png|_round.png)</code> 48–192px</td></tr><tr><td>通知小图标</td><td><code>drawable/ic_stat_atu.xml</code> + <code>drawable-*/ic_stat_atu.png</code> 24–96px，纯白透明底</td></tr>
        <tr><td>启动页（Android 12+）</td><td><code>drawable/splash_icon.xml</code>（288dp，落在 192dp 的圆内）+ <code>values/splash_theme_snippet.xml</code></td></tr><tr><td>iOS</td><td><code>ios/AppIcon.appiconset/</code>：1024 默认版（不透明）、Dark、Tinted 三种外观</td></tr>
        <tr><td>其他配色</td><td><code>png/app-icon-light|caramel-1024.png</code>，用于活动和测试版</td></tr></table><p class="note">Adaptive 图标的狗头控制在 66dp 安全区以内，用圆形、方圆形、圆角方形、水滴形任何一种遮罩都不会被裁到。</p></div></div>'''))
    asx = ''.join(f'<img src="03-stores/app-store/02-iphone-6.9in-1320x2868/hey-atu-iphone-{n}.png">' for n in ['01-agent', '02-updates', '03-follow-up', '04-todo', '05-pair', '06-your-computer', '07-dark'])
    pads = ''.join(f'<img src="03-stores/app-store/04-ipad-13in-2752x2064/hey-atu-ipad-{n}.png">' for n in ['01-updates', '02-follow-up', '03-todo', '04-dark'])
    S_.append(sec(13, '应用商店：Google Play 和 App Store', '两个商店共用同一套图标、同一条截图故事线和同一套模板，按各自规格导出。<b>每个商店的截图都只放该平台自己的界面。</b>文案和检查清单见各自文件夹里的 <code>listing.md</code>。',
        f'''<table class="t"><tr><th></th><th>Google Play（今天）</th><th>App Store（等 Apple 审批）</th></tr>
        <tr><td>图标</td><td>512×512 · 32-bit PNG · 满版正方形，Play 自动加 30% 圆角</td><td>1024×1024 · 不透明 · 随构建包上传（默认 / Dark / Tinted）</td></tr>
        <tr><td>横幅</td><td>Feature graphic 1024×500</td><td>—</td></tr>
        <tr><td>手机截图</td><td>7 张 · 1080×1920</td><td>7 张 · 1206×2622（必需）+ 1320×2868</td></tr>
        <tr><td>平板截图</td><td>选填</td><td>4 张 · iPad 13 寸 2752×2064（支持 iPad 时必需）</td></tr>
        <tr><td>文字</td><td>名称 30 · 短描述 80 · 完整描述 4000</td><td>名称 30 · 副标题 30 · 推广文本 170 · 关键词 100 字节 · 描述 4000</td></tr>
        <tr><td>门槛</td><td>.aab 安装包 target API 36；新个人账号要 12 人 × 14 天封闭测试</td><td>开发者账号审批；审核演示环境；隐私标签</td></tr></table>
        <h3>Google Play</h3><div class="cols2"><div><img class="wide" src="{P}/02-feature-graphic/feature-graphic-1024x500.png"></div><div><img src="{P}/01-app-icon/play-icon-512.png" style="height:150px;border-radius:45px"><p class="note">Feature graphic 用焦糖底：Play 不建议纯白、纯黑、深灰底，也不要放大号 logo。<b>这组截图现在是 iOS 界面，Android 版出来后要替换。</b></p></div></div><div class="shots">{shots}</div>
        <h3>App Store · iPhone 6.9 寸（6.3 寸为同图缩放导出）</h3><div class="shots">{asx}</div>
        <h3>App Store · iPad 13 寸</h3><div class="pads">{pads}</div>'''))
    S_.append(sec(14, '宣发物料', '模板都是 HTML 渲染出来的，改文案后重新生成即可（<code>src/build_marketing.py</code>）。',
        '<div class="mkgrid">' + mk('web/hey-atu-og-share-1200x630.png', 'OG 分享图 · 深色 1200×630') + mk('web/hey-atu-og-share-light-1200x630.png', 'OG 分享图 · 浅色') +
        mk('social/hey-atu-x-header-1500x500.png', 'X 头图 1500×500') + mk('social/hey-atu-linkedin-banner-1584x396.png', 'LinkedIn 横幅 1584×396') +
        mk('templates/hey-atu-release-card-1200x675.png', '更新日志卡片 1200×675') + mk('web/hey-atu-email-header-1200x400.png', '邮件头图 1200×400') +
        mk('social/hey-atu-social-post-1080x1350.png', '社媒帖子 1080×1350（玩偶客串）') + mk('social/hey-atu-story-1080x1920.png', 'Story 1080×1920 · 状态面板') +
        mk('social/hey-atu-avatar-1024.png', '社媒头像 1024') + mk('stickers/remix-dark.png', '表情贴纸 · 深色') + '</div>'))
    S_.append(sec(15, '文件索引', '所有 PNG 都由 SVG 或 HTML 渲染得到。SVG 是唯一的源文件，要改就改 <code>src/</code> 里的生成脚本，不要手改 PNG。',
        '''<table class="t"><tr><th>文件夹</th><th>内容</th><th>格式</th></tr>
        <tr><td>01-logo/svg, png</td><td>彩色、描边、单色（ink / white / caramel）、线条；横版 / 竖版组合标；字标</td><td>SVG；PNG 512 / 1024 / 2048（组合标 1200 / 2400）透明底</td></tr>
        <tr><td>01-logo/guides</td><td>构成图、安全区、错误用法</td><td>SVG / PNG</td></tr><tr><td>02-app-icon</td><td>iOS appiconset、Android res（adaptive / 旧版 / 圆形 / 通知 / 启动页）、其他配色</td><td>XML VectorDrawable、PNG、SVG、JSON</td></tr>
        <tr><td>03-stores</td><td>google-play：图标、Feature graphic、7 张截图、listing.md；app-store：图标、iPhone 6.9 / 6.3 寸各 7 张、iPad 13 寸 4 张、listing.md；ai-directories：目录和 Google 登录用的图标</td><td>PNG / JPG / MD</td></tr><tr><td>04-marketing</td><td>OG、X、LinkedIn、帖子、Story、头像、更新日志卡、邮件头图、贴纸、favicon</td><td>PNG</td></tr>
        <tr><td>05-states</td><td>idle / working / done / offline</td><td>SVG；PNG 256 / 512 / 1024</td></tr><tr><td>06-app-samples</td><td>Android、iOS 系统触点示意；Logo 和玩偶分工</td><td>PNG</td></tr>
        <tr><td>07-fonts-and-tokens</td><td>字体（OFL 授权）、tokens.json / tokens.css</td><td>TTF / JSON / CSS</td></tr><tr><td>08-source</td><td>真实 App 界面截图（浅色 / 深色）、官网素材、玩偶状态 GIF</td><td>PNG / WebP / GIF</td></tr></table>'''))

    toc = ''.join(f'<a href="#s{i}">{i:02d} {t}</a>' for i, t in enumerate(['品牌概述', 'Logo 系统', '构成与安全区', '组合标志', '错误用法', 'Logo 和玩偶', '四个状态', '色彩', '字体', '图形元素', '图像风格', '图标与系统', '应用商店', '宣发物料', '文件索引'], 1))
    html = f'''<!doctype html><html lang="zh"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Hey Atu · 品牌视觉规范 v1.0</title>
<style>
@font-face{{font-family:"Departure Mono";src:url("{F}/DepartureMono-Regular.ttf")}}
@font-face{{font-family:JBM;src:url("{F}/JetBrainsMono-400.ttf");font-weight:400}}@font-face{{font-family:JBM;src:url("{F}/JetBrainsMono-500.ttf");font-weight:500}}@font-face{{font-family:JBM;src:url("{F}/JetBrainsMono-600.ttf");font-weight:600}}
*{{box-sizing:border-box}}body{{margin:0;background:#F7F7F8;color:#18181B;font:16px/1.65 -apple-system,"PingFang SC",system-ui,sans-serif}}
.cover{{background:#0E0E10;color:#F7F7F8;padding:110px 8vw 90px;position:relative;overflow:hidden}}
.cover:before{{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.12) 1.4px,transparent 1.6px);background-size:26px 26px;-webkit-mask-image:linear-gradient(90deg,transparent 30%,#000)}}
.cover:after{{content:"";position:absolute;left:-200px;top:-260px;width:800px;height:800px;border-radius:50%;background:radial-gradient(rgba(217,128,58,.22),transparent 65%)}}
.cover>*{{position:relative;z-index:1}}.cover h1{{font:400 64px/1.08 "Departure Mono";margin:56px 0 16px}}.cover .acc{{color:#D9803A}}
.toc{{display:flex;flex-wrap:wrap;gap:8px 18px;margin-top:46px;font:500 13px JBM}}.toc a{{color:#A1A1AA;text-decoration:none}}
section{{padding:84px 8vw;border-top:1px solid #DEDEE3;max-width:1500px;margin:0 auto}}
.num{{font:600 13px JBM;letter-spacing:.16em;color:#D9803A}}h2{{font:400 40px/1.15 "Departure Mono";margin:10px 0 12px}}h3{{font:600 15px JBM;margin:40px 0 12px}}
.lede{{font-size:18px;color:#4F4F58;max-width:900px;margin:0 0 34px}}.note{{font-size:14px;color:#74747E;max-width:1000px}}
code{{font:500 .88em JBM;background:#EEEEF0;padding:1px 6px;border-radius:5px}}
.label{{font:600 13px JBM;letter-spacing:.16em;text-transform:uppercase}}.disp{{font-family:"Departure Mono"}}
.grid4{{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}}.cols2{{display:grid;grid-template-columns:1fr 1fr;gap:24px;align-items:start}}.cols3{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}}.cols4{{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}}
.tile{{margin:0}}.tile .box{{border-radius:20px;height:230px;display:flex;align-items:center;justify-content:center;box-shadow:inset 0 0 0 1px rgba(0,0,0,.06);overflow:hidden;padding:20px}}.tile img{{max-width:100%}}
.tile figcaption{{font-size:14px;margin-top:10px;color:#4F4F58}}.cols2 .tile .box{{height:auto;min-height:230px}}
.dont .box{{position:relative}}.dont figcaption{{color:#D14343}}
.card{{background:#fff;border-radius:20px;padding:24px 26px;box-shadow:0 0 0 1px #DEDEE3}}.card h4{{margin:0 0 8px;font:600 15px JBM}}.card ul{{padding-left:18px;margin:6px 0}}.card .big{{font:400 24px/1.25 "Departure Mono";margin:4px 0 10px}}
.card.ink{{background:#0E0E10;color:#ECECF1;box-shadow:none}}.card.ink p{{color:#ADADB8;font-size:14px}}
.dots-demo{{height:70px;border-radius:14px;background-image:radial-gradient(rgba(255,255,255,.25) 1.6px,transparent 1.8px);background-size:14px 14px;-webkit-mask-image:linear-gradient(90deg,transparent,#000)}}
.glow-demo{{height:70px;border-radius:14px;background:radial-gradient(circle at 0 0,rgba(217,128,58,.5),transparent 70%)}}
.row{{display:flex;gap:14px;margin-top:14px;align-items:end}}
.t{{border-collapse:collapse;width:100%;margin:22px 0;font-size:14px;background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 0 0 1px #DEDEE3}}.t th,.t td{{text-align:left;padding:10px 14px;border-bottom:1px solid #EEEEF0;vertical-align:top}}.t th{{font:600 12px JBM;letter-spacing:.08em;text-transform:uppercase;color:#74747E;background:#FAFAFB}}
.t.ui i{{display:inline-block;width:14px;height:14px;border-radius:4px;vertical-align:-2px;margin-right:8px;box-shadow:0 0 0 1px rgba(0,0,0,.12)}}
.ratio{{display:flex;height:34px;border-radius:10px;overflow:hidden;box-shadow:0 0 0 1px #DEDEE3;margin-bottom:22px}}
.sws{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}}.sw{{background:#fff;border-radius:18px;overflow:hidden;box-shadow:0 0 0 1px #DEDEE3}}.sw .chip{{height:110px;padding:14px 16px;font:600 15px JBM;display:flex;align-items:flex-end;box-shadow:inset 0 -1px 0 rgba(0,0,0,.06)}}.sw .meta{{padding:12px 16px;font-size:13px}}.sw .meta span{{color:#74747E}}.sw p{{margin:6px 0 0;color:#4F4F58}}
.states{{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}}.state{{background:#0E0E10;color:#ECECF1;border-radius:20px;padding:22px}}.state .pair{{display:flex;align-items:center;gap:12px;justify-content:space-between}}.state .g{{height:84px}}.state .m{{height:96px;border-radius:16px;background:#F7F7F8}}.state p{{color:#ADADB8;font-size:14px;margin:6px 0 0}}.state span{{color:#555}}
.type>div{{background:#fff;border-radius:20px;padding:26px;margin-bottom:16px;box-shadow:0 0 0 1px #DEDEE3}}.type p{{color:#4F4F58;margin:8px 0 0}}
img.wide{{width:100%;border-radius:20px;display:block;margin:0 0 18px;box-shadow:0 0 0 1px #DEDEE3}}
.shots{{display:grid;grid-template-columns:repeat(7,1fr);gap:12px;margin-top:12px}}.shots img{{width:100%;border-radius:14px}}.pads{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}}.pads img{{width:100%;border-radius:12px}}
.mkgrid{{display:grid;grid-template-columns:repeat(2,1fr);gap:22px}}.mk{{margin:0}}.mk img{{width:100%;border-radius:16px;box-shadow:0 0 0 1px #DEDEE3;display:block;max-height:640px;object-fit:contain;background:#E9E9EC}}.mk figcaption{{font-size:14px;color:#4F4F58;margin-top:8px}}
footer{{padding:50px 8vw 80px;color:#74747E;font-size:13px}}
@media print{{section{{break-inside:auto;padding:46px 6vw}}.cover{{padding:80px 6vw}}}}
@media(max-width:900px){{.grid4,.cols4,.sws,.states{{grid-template-columns:1fr 1fr}}.cols2,.cols3,.mkgrid{{grid-template-columns:1fr}}.shots{{grid-template-columns:repeat(3,1fr)}}h2{{font-size:30px}}.cover h1{{font-size:40px}}}}
</style><body>
<header class="cover"><img src="{L}/svg/atu-lockup-horizontal-on-dark.svg" style="height:64px"><h1>品牌视觉规范<br><span class="acc">v1.0</span></h1>
<div style="color:#A1A1AA;font:500 15px JBM">Brand guidelines · 2026-10 · 交付产品团队 · Google Play / App Store 上架</div><nav class="toc">{toc}</nav></header>
{''.join(S_)}
<footer>Hey Atu · 品牌视觉规范 v1.0 · 所有 PNG 都由 SVG 或 HTML 渲染，源文件见 src/。界面截图取自 heyatu.com 线上演示（按当前 App 还原，示例内容）。</footer></body></html>'''
    write(f'{KIT}/Hey-Atu-Brand-Guidelines.html', html)
    with Renderer() as r:
        r.pg.set_viewport_size({'width': 1440, 'height': 900})
        r.pg.goto('file://' + f'{KIT}/Hey-Atu-Brand-Guidelines.html', wait_until='load')
        r.pg.evaluate('document.fonts.ready.then(()=>1)'); r.pg.wait_for_timeout(1500)
        r.pg.screenshot(path=f'{ROOT}/build/guide-full.png', full_page=True)
        r.pg.emulate_media(media='print')
        r.pg.pdf(path=f'{KIT}/Hey-Atu-Brand-Guidelines.pdf', width='1440px', height='1800px', print_background=True, margin={'top': '0', 'bottom': '0', 'left': '0', 'right': '0'})
    print('guide ok')


if __name__ == '__main__':
    build()
