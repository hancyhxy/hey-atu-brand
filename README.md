# Hey Atu 品牌交付包 v1.2（2026-10）

> v1.2（2026-10-13）：
> - 彩色主标：双耳和脸之间留一道透明缝隙（约 1.5 倍描边宽），深浅底一致；边缘取自同一套平滑曲线。
> - 线条版（刺绣、周边）：只保留外轮廓一条线加双眼，不再有内线。
> - Flat 贴纸：9 个配件 × 深 / 浅两版，改为由 `09-generator/build_flat.py` 用当前 Logo 矢量生成（SVG + PNG）。
> - 规范页适配手机；所有 Logo、图标、状态、商店图、宣发物料和下载包已按新几何重新生成。
>
> v1.1（2026-10-13）：狗头 Logo 换成产品团队认可的手绘版（流畅化 A）。头、耳、眼斑为平滑曲线，眼睛为椭圆；描边与缝隙向外生长。所有 Logo、App 图标、状态图、宣发物料和规范已按新几何重新生成。

先打开 **`Hey-Atu-Brand-Guidelines.html`**，PDF 版是同一份内容。规范共 16 节，只写我们自己的视觉系统：Logo、色彩、字体、图形、图像、图标、角色系统（Mark / Flat / Plush 三种形态、衣橱、动作库、延展路线）、应用商店和宣发物料。

外部调研单独放在 **`00-research/Hey-Atu-Research.html`**，包括科技 / Agent 公司的视觉调研、上架渠道调研和资料来源，仅供内部参考。

## 上架渠道

Android 和 Google Play 的关系、一共有哪几个渠道、行业通行做法，都写在 `00-research/`；现在还缺什么，见 `03-stores/README.md`。

| 商店 | 上传文件 | 文案和检查清单 |
|---|---|---|
| Google Play | `03-stores/google-play/`：图标 512、Feature graphic 1024×500、7 张 1080×1920 截图 | `google-play/listing.md` |
| App Store | `03-stores/app-store/`：iPhone 1206×2622（必需）和 1320×2868 各 7 张、iPad 2752×2064 共 4 张；图标随构建包上传 | `app-store/listing.md` |
| Claude / ChatGPT 目录、Google 登录同意页 | `03-stores/ai-directories/`：图标 120 / 512 / 1024 | — |

⚠️ Google Play 截图现在用的是 iOS 界面，Android 版出来后要替换。仓库里还没有 Android 工程。

## Android 工程（直接拷进 `app/src/main/res/`）

`02-app-icon/android/res/` 里包括：adaptive icon（矢量的 foreground 和 monochrome 层，加背景色）、旧版 mipmap 和圆形图标、通知小图标 `ic_stat_atu`、Android 12+ 启动页图标，以及主题片段。Manifest 里这样写：

```xml
android:icon="@mipmap/ic_launcher"
android:roundIcon="@mipmap/ic_launcher_round"
```

通知里用 `setSmallIcon(R.drawable.ic_stat_atu)`，强调色用 `@color/atu_caramel`。

## iOS

`02-app-icon/ios/AppIcon.appiconset/` 可以直接替换 `ios/native/Assets.xcassets/AppIcon.appiconset/`，里面有默认、Dark、Tinted 三种外观。

## 文件夹

| 文件夹 | 内容 |
|---|---|
| 00-research | 外部调研（不对外，不进规范） |
| 01-logo | SVG 源文件 + 透明底 PNG：彩色、描边、单色（ink/white/caramel）、线条、横版和竖版组合标、字标；guides/ 下是构成图、安全区和错误用法 |
| 02-app-icon | iOS、Android 图标，各种配色的 1024 PNG 和 SVG |
| 03-stores | 各商店的上架素材、listing.md 和渠道调研 |
| 04-marketing | web（OG 图、邮件头图、favicon）、social（X、LinkedIn、帖子、Story、头像）、templates（更新日志卡片）、stickers（贴纸） |
| 05-states | idle / working / done / offline 四个状态，SVG + PNG |
| 06-app-samples | Android 和 iOS 系统触点示意、Logo 与玩偶分工 |
| 07-fonts-and-tokens | Departure Mono、JetBrains Mono（OFL 授权）、tokens.json / tokens.css |
| 08-source | 真实 App 界面截图（浅色和深色，取自 heyatu.com 线上演示）、官网素材、玩偶状态 GIF |
| 10-character | 角色素材：Plush 状态动画 GIF（App 现行版本）、各档服装的抠图、Flat 贴纸（SVG + PNG，深 / 浅） |
| 09-generator | 生成脚本和 HTML 模板。改了几何参数或文案后运行 `09-generator/build_all.sh`，会重建全部素材、规范 HTML / PDF 和 `downloads/` 下载包 |

## 规则摘要

- 颜色：Ink `#0E0E10` · Paper `#F7F7F8` · Caramel `#D9803A` · Navy `#1F2D4F`
- 狗头在深色底上用彩色版；在浅色底上一定要用描边版；在焦糖底上用单色白。
- 字体：标题用 Departure Mono，字标和标签用 JetBrains Mono 500，正文用系统字体。
- Logo 只出现在 App 外面；App 里面只用穿马甲的玩偶 Atu（T1 默认装）。
- 换装只换 Plush，Logo 永远不换装；耳朵、右眼斑、眼睛任何时候都不能遮。
