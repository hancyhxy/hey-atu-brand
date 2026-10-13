"""Character system section for the brand guidelines (our own rules only)."""
C = '10-character'
L = '01-logo'
S = '05-states'


def fig(src, cap, h=200, bg='#F7F7F8', fit='contain'):
    return (f'<figure class="cf"><div class="cbox" style="background:{bg}"><img src="{src}" style="height:{h}px;object-fit:{fit}"></div>'
            f'<figcaption>{cap}</figcaption></figure>')


def table(head, rows, cls='t'):
    return (f'<table class="{cls}"><tr>' + ''.join(f'<th>{h}</th>' for h in head) + '</tr>' +
            ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '</table>')


def html():
    forms = f'''<div class="forms">
  <div class="form ink"><div class="label" style="color:#E8954F">形态 1 · Atu Mark</div><img src="{L}/svg/atu-glyph-color.svg" style="height:150px;margin:26px 0">
    <p><b>数字符号</b>：6 个椭圆组成的扁平狗头。它是品牌的签名，<b>永远不换装</b>，只有 4 个状态。</p></div>
  <div class="form ink"><div class="label" style="color:#E8954F">形态 2 · Atu Flat</div><img src="{C}/flat-stickers/tiles/focus-dark.png" style="height:150px;margin:26px 0;border-radius:18px">
    <p><b>扁平角色</b>：由 Mark 派生，可以加小配件。只用于贴纸、表情和插画，<b>不能当 logo 用</b>。</p></div>
  <div class="form ink"><div class="label" style="color:#E8954F">形态 3 · Atu Plush</div><img src="{C}/plush-outfits/dog-wave-vest.webp" style="height:150px;margin:26px 0">
    <p><b>玩偶角色</b>：有毛绒质感，有鼻子和嘴，会做动作，可以换衣服。用在 App 内、官网、视频和周边。</p></div></div>'''

    dna = table(['', '固定不变（三种形态共用）', 'Mark / Flat', 'Plush'], [
        ['耳朵', '两只焦糖色耳朵', '左耳上扬、右耳下垂（经过符号化）', '两只都自然下垂，毛绒质感'],
        ['眼斑', '<b>画面右侧那只眼睛</b>被焦糖色斑块包住', '一条连续的椭圆弧', '毛绒斑块，边缘柔和'],
        ['眼睛', '两只黑眼睛', '竖椭圆，没有高光', '圆形，有高光'],
        ['脸', '白色头部', '<b>没有鼻子、嘴巴、腮红</b>', '有棕色鼻子、微笑的嘴、粉色腮红'],
        ['颜色', '焦糖 · 白 · 黑', '用品牌色值：#D9803A / #FFFFFF / #0E0E10', '真实材质颜色，接近焦糖色就可以，不要求精确色值'],
        ['名字', 'Atu', 'App 里的标签写作 ATU（等宽字体，全大写）', '同左']])

    wardrobe = f'''<div class="wd">
  <div class="tier"><div class="label">T1 · 默认装（Signature）</div><div class="row">{fig(f"{C}/plush-outfits/dog-wave-vest.webp", "抓绒马甲：奶油色羊羔绒、藏青色包边、红色拉链头", 190)}{fig(f"{C}/plush-outfits/atu-face.webp", "头像裁切", 120)}</div>
    <p>App 内<b>只用这一套</b>。每个新渠道第一次出场、应用商店、官方头像，也都用这一套。</p><p class="note">⚠ 现在这张标准照里，玩偶手上的手机背面露出了苹果标志。下一版要修掉，或换成没有标志的手机。</p></div>
  <div class="tier"><div class="label">T2 · 场景装（Scene）</div><div class="row">{fig(f"{C}/plush-outfits/scene-commute.webp", "通勤：黑色羽绒马甲 + 工牌", 170)}{fig(f"{C}/plush-outfits/scene-garden.webp", "周末：粉色帽子 + 浇水壶", 170)}{fig(f"{C}/plush-outfits/dog-switch.webp", "游戏：灰色马甲（手里的游戏机是第三方产品，宣发里不要用）", 170)}</div>
    <p>只用在官网的场景段落、社媒和视频里，用来说明“Atu 陪你在哪儿”。<b>不进 App，不进应用商店。</b></p></div>
  <div class="tier"><div class="label">T3 · 限定装（Limited）</div><div class="row"><div class="ph">节日、发布会、联名</div></div>
    <p>有时间范围，过期就下线，例如 “Launch week 卫衣”“圣诞围巾”。每次发布前都要登记进衣橱表。</p></div></div>'''

    wardrobe_rules = table(['换装规则', '为什么'], [
        ['衣服和配件<b>不能挡住</b>耳朵、右眼斑和眼睛', '这三处是认出 Atu 的关键'],
        ['一次最多 <b>1 件头部配件 + 1 件上衣 + 1 件手持物</b>', '保持轮廓干净，缩小后也能看清'],
        ['服装颜色从品牌色里选：奶油、藏青、焦糖、Ink，点缀色限一个', '和 Mark 放在一起时颜色不打架'],
        ['衣服上只能出现 Atu Mark，<b>不能出现第三方 logo 或商标</b>（手机背面、游戏机、饮料杯）', '避免侵权，也避免在应用商店被拒'],
        ['新的宣发物料不再用食物、饮料道具（拿铁、泡面）', '整体是科技工具的气质，不往生活方式方向走'],
        ['不改物种特征：体型比例、耳朵形状、斑块位置都不动', '换的是衣服，不是换一只狗'],
        ['命名：<code>atu-plush-&lt;tier&gt;-&lt;outfit&gt;-&lt;action&gt;</code>，例如 <code>atu-plush-t1-vest-wave</code>', '方便统一管理和检索']])

    acts = ''.join(f'''<div class="act"><img src="{C}/plush-motion/mascot-{g}.gif" class="ag"><img src="{S}/svg/atu-state-{s}.svg" class="am">
      <div class="label" style="color:{c}">{t}</div><p>{d}</p></div>''' for g, s, c, t, d in [
        ('idle', 'idle', '#71717A', 'idle · 待命', '轻微呼吸、眨眼'),
        ('working', 'working', '#D9803A', 'working · 工作中', '对着笔记本打字'),
        ('done-laugh', 'done', '#218739', 'done · 完成', '大笑；另外三个变体是挥手、眨眼、撒彩带，随机播放'),
        ('offline', 'offline', '#74747E', 'offline · 离线', '闭眼睡觉')])
    act_extra = ''.join(f'<img src="{C}/plush-motion/mascot-done-{v}.gif" title="done-{v}">' for v in ['wave', 'wink', 'confetti'])

    motion_spec = table(['项目', 'App 内（现行规格，来自 NativeMascot.swift）', '官网 / 视频'], [
        ['格式', 'GIF，透明底，216×216', '透明 WebM + HEVC .mov；静帧用 WebP'],
        ['节奏', '36 帧 · 12 fps · 3 秒循环', '每段 4 秒左右，结尾停在第一帧，可以无缝循环'],
        ['构图', '胸像居中，头部占画面约 45%；在 64pt 圆形头像和 36pt 列表图标里裁切显示', '全身，脚底留 6% 空白'],
        ['动作和状态', '动作只表达 4 个状态，不加和状态无关的动作', '可以加挥手、拿手机这类营销动作'],
        ['无障碍', '开启“减弱动态效果”时只显示第一帧', '同左']])

    usage = table(['触点', 'Mark', 'Flat', 'Plush T1', 'Plush T2/T3'], [
        ['App 图标 · 系统通知 · 商店图标 · favicon', '✓', '', '', ''],
        ['App 内：Agent 头像、列表图标、离线页', '', '', '✓', ''],
        ['应用商店截图', '✓（状态标签）', '', '界面里自然出现', ''],
        ['官网首屏 / 导航', '✓ 导航', '', '✓ 首屏', '✓ 场景段落'],
        ['社媒头像', '✓', '', '', ''],
        ['社媒内容 / 视频', '', '✓', '✓', '✓'],
        ['贴纸 / 表情包', '', '✓', '', ''],
        ['周边：毛绒玩具、钥匙扣', '刺绣用线条版', '', '✓ 实物', '✓ 限定款'],
        ['T 恤、贴纸等印刷品', '✓', '✓', '', '']], cls='t usage')

    flat_rules = f'''<div class="cols2"><img class="wide" src="{C}/flat-stickers/remix-dark.png" style="max-width:520px"><div>
  {table(['Flat 规则', ''], [
      ['底子', '必须是完整的 Mark 几何，配件叠在上面'],
      ['配件', '扁平填色，用品牌色加藏青；浅色底版本加 Ink 描边'],
      ['可以遮挡什么', '只有墨镜可以遮住眼睛；耳朵和眼斑任何时候都不能遮'],
      ['尺寸', '512×512 透明 PNG，留 8% 边距；表情包另出 128 和 96 两档'],
      ['数量', '先做 9 个；之后每季度最多加 6 个，保持整套风格一致']])}</div></div>'''

    roadmap = table(['阶段', '做什么', '交付物'], [
        ['现在', 'Mark + 4 个状态；Plush T1 + 4 组状态动画；Flat 9 个配件版', '本规范和交付包'],
        ['下一步（上架后 1–3 个月）', '把状态 Mark 接到通知、Live Activity 和小组件；Flat 做成 iMessage / Telegram 贴纸包；T2 场景装统一重拍到 T1 的灯光和机位', '贴纸包；Plush T2 图库'],
        ['之后（3–12 个月）', '季节性 T3；评估是否让用户给自己的 Atu 选衣服（产品功能，需要单独决策）；实体毛绒玩具和刺绣周边', '衣橱表 v2；周边打样'],
        ['长期', '每年检查一次角色：动作库是否覆盖了新的产品状态；不同渠道的视觉是否已经走偏', '角色年检报告']])

    governance = '''<div class="cols3"><div class="card"><h4>新增服装或动作前，过一遍 6 项检查</h4><ol style="padding-left:18px;margin:6px 0;font-size:14px">
  <li>耳朵、右眼斑、眼睛都看得见吗？</li><li>体型和比例没改吧？</li><li>颜色都在品牌色里吗？</li><li>画面里有第三方 logo 吗？</li><li>缩到 64px 还能认出来吗？</li><li>这个动作对应哪个产品状态，或者哪个营销场景？</li></ol></div>
  <div class="card"><h4>AI 生成 Plush 的要求</h4><p style="font-size:14px">参考图只用 T1 正面标准照（<code>10-character/plush-outfits/dog-wave-vest.webp</code>）。提示词里写明“同一只玩偶，只换衣服”。出图后过 6 项检查，并<b>人工核对右眼斑的位置</b>，AI 经常把它画到另一只眼睛上。</p></div>
  <div class="card"><h4>谁来批</h4><p style="font-size:14px">Mark 和 Flat 的规则由品牌负责人维护。Plush 的新服装和新动作由品牌负责人审批；如果要进 App，还要通知 App 团队，由他们替换 <code>ios/native/Resources/</code> 里的文件。</p></div></div>'''

    return f'''
<p class="lede">Atu 是同一只狗，分三种形态出现。三种形态共用同一组<b>“认出它”的特征</b>（下文称 DNA），但各自管自己的场景，不能互相替代。</p>
{forms}
<h3>A · 角色 DNA：哪些固定、哪些可以变</h3>{dna}
<h3>B · Plush 衣橱：三档服装</h3>{wardrobe}{wardrobe_rules}
<h3>C · 动作库：每个动作都对应一个产品状态</h3><p class="note">App 里玩偶的 4 个状态，和 Mark 的 4 个状态一一对应。同一时刻，App 内外讲的是同一件事。</p>
<div class="acts">{acts}</div><div class="actx"><span class="label">done 的其他变体</span>{act_extra}</div>{motion_spec}
<h3>D · Flat：贴纸和表情的延展</h3>{flat_rules}
<h3>E · 场景矩阵：哪种形态用在哪里</h3>{usage}
<h3>F · 延展路线</h3>{roadmap}
<h3>G · 管理</h3>{governance}'''


CSS = '''
.forms{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-bottom:10px}}.form{{border-radius:22px;padding:26px;text-align:center;background:#0E0E10;color:#ECECF1}}.form p{{font-size:14px;color:#C9C9D1;text-align:left;margin:0}}.form img{{display:block;margin-left:auto!important;margin-right:auto!important}}
.cf{{margin:0}}.cbox{{border-radius:18px;padding:14px;display:flex;align-items:center;justify-content:center;box-shadow:inset 0 0 0 1px rgba(0,0,0,.06)}}.cf figcaption{{font-size:13px;color:#4F4F58;margin-top:8px;max-width:220px}}
.wd{{display:grid;grid-template-columns:1.1fr 1.5fr .8fr;gap:18px;margin:14px 0}}.tier{{background:#fff;border-radius:20px;padding:20px;box-shadow:0 0 0 1px #DEDEE3}}.tier .label{{color:#D9803A;margin-bottom:12px}}.tier p{{font-size:14px;color:#4F4F58;margin:12px 0 0}}.tier .row{{display:flex;gap:10px;align-items:flex-end;flex-wrap:wrap;margin:0}}
.ph{{height:190px;width:100%;border-radius:18px;border:2px dashed #DEDEE3;display:flex;align-items:center;justify-content:center;color:#74747E;font-size:14px}}
.acts{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}}.act{{background:#0E0E10;border-radius:20px;padding:20px;color:#ECECF1;position:relative}}.act .ag{{width:100%;max-width:200px;display:block;margin:0 auto;background:#F7F7F8;border-radius:16px}}.act .am{{position:absolute;right:16px;top:16px;height:46px}}.act .label{{margin-top:12px}}.act p{{color:#ADADB8;font-size:14px;margin:4px 0 0}}
.actx{{display:flex;gap:14px;align-items:center;margin:14px 0}}.actx img{{height:110px;border-radius:14px;background:#fff;box-shadow:0 0 0 1px #DEDEE3}}.actx .label{{color:#74747E}}
.usage td:not(:first-child),.usage th:not(:first-child){{text-align:center}}
'''

CSS = CSS.replace('{{', '{').replace('}}', '}')
