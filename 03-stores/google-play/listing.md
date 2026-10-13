# Google Play 商店信息 · Hey Atu

Play Console 路径：**Grow users › Store presence › Main store listing**。

## 1. 图片素材（逐项对照 Play 规格）

| 位置 | 文件 | 规格要求 | 本包 |
|---|---|---|---|
| App icon | `01-app-icon/play-icon-512.png` | 512×512，32-bit PNG（含 alpha），≤1024 KB，满版正方形，不要自己加圆角和阴影 | ✅ 512×512 RGBA，满版 #0E0E10，Play 自己加 30% 圆角 |
| Feature graphic | `02-feature-graphic/feature-graphic-1024x500.png`（也有 `.jpg`） | 1024×500，JPEG 或 24-bit PNG，不能有 alpha；不要用纯白、纯黑或深灰底；重点放在画面中间 | ✅ 焦糖底，不放大号 logo，不放设备外框 |
| Phone screenshots | `03-phone-screenshots/hey-atu-phone-01…07.png` | 2–8 张，PNG/JPEG，不能有 alpha，9:16；想进推荐位需要至少 4 张、每张 ≥1080×1920 | ✅ 7 张，1080×1920，24-bit PNG |
| Tablet screenshots | — | 可选 | 暂不提供（见文末） |
| Preview video | — | 可选，填 YouTube 链接 | 暂不提供 |

上传顺序就是文件编号顺序。前 3 张都是 App 内的真实界面，符合 Play「前三张优先展示 UI」的建议。

## 2. 文案

**App name**（≤30 字符）
```
Hey Atu
```

**Short description**（≤80 字符，现在 70 个字符；不能写 CTA，也不能写 Best、#1、Free 这类词）
```
Check on the AI agent running on your computer, right from your phone.
```

**Full description**（≤4000 字符，草稿，发布前请产品确认）
```
Hey Atu keeps your AI working while you are away from your desk.

Your own AI assistant runs on your own computer, not in someone else's cloud. Hey Atu connects your phone to it, so you can check progress, answer questions and pick up where you left off.

CHATS
Continue any session from your phone. Read the plan, choose an option, and send the next step.

UPDATES
See what finished while you were away: morning briefs, price watches, inbox digests and more, in one feed. Ask a follow-up about any update.

TODO
Plan the day with Atu. Add to-dos, follow up on several at once, and let Atu work through them.

PAIR IN ONE SCAN
Install on your computer, then scan the code with your phone. No VPN and no ports to open.

BRING YOUR OWN MODELS
Use Claude, ChatGPT, Gemini, Grok, DeepSeek, Kimi, Qwen and more. Sign in with the subscriptions you already have.

YOUR DATA STAYS ON YOUR COMPUTER
Your chats, to-dos and files stay on your own disk.

Works with Mac and Linux. Windows is coming.
```

> 「Mac / Linux / Windows soon」「30+ 模型」「数据留在你的电脑上」都直接取自 heyatu.com 线上文案。如果 Android 版的功能和 iOS 不一样，提交前要逐条核对。

## 3. 每张图的 Alt text（≤140 字符）

| 文件 | Alt text |
|---|---|
| feature-graphic | Hey Atu: keep your AI working from your phone. Two app screens on a caramel background. |
| phone-01-agent | The Agent chat: Atu shares a plan and asks which dentist time to book. |
| phone-02-updates | The Updates feed with cards for a morning brief, a price watch and home energy use. |
| phone-03-follow-up | A price-watch update about Tokyo flights, with a follow-up question and Atu's answer. |
| phone-04-todo | The Todo tab: one task done today and four recent to-dos. |
| phone-05-pair | Pairing: the phone camera scans the QR code shown on the computer. |
| phone-06-your-computer | A new chat connected to Studio Mac, ready for the first message. |
| phone-07-dark | The same Agent chat in light and dark appearance. |

## 4. 提交前检查

- [ ] 截图必须是 **Android 版**的真实界面。本包里的截图来自 heyatu.com 线上演示，演示按当前 iOS App 一比一还原。如果 Android 版界面不同（状态栏、导航条、字体），要用 Android 真机截图替换中间的手机画面。外层模板 `build/play-*.html` 可以直接复用。
- [ ] 截图里没有通知、运营商名称，电池和信号都是满格。
- [ ] Feature graphic 和截图都没有写 Best、#1、New、Free、Download now 这类词。
- [ ] Short description 不超过 80 字符，没有 emoji 或特殊符号。
- [ ] 每张图都填了 Alt text。

## 5. 非视觉项（2026-10 查证，负责人：产品 / Android 开发）

- [ ] **Android 安装包**：上传 `.aab`。2026-08-31 起，新 App 必须 target **API 36（Android 16）**。仓库里目前没有 Android 工程。
- [ ] **新个人账号的测试门槛**：2023-11-13 以后注册的个人账号，必须先跑封闭测试，至少 **12 名测试者连续参与 14 天**，才能申请正式发布；申请审核一般 7 天以内。组织账号不受这条限制，但需要 D-U-N-S 编号。
- [ ] **App content 声明**：隐私政策 URL、广告、App access（审核员登录方式，需要演示环境，同 App Store）、内容分级、目标受众、Data safety。
- [ ] **账号删除**：只要 App 里能创建账号，就必须提供 App 内和网页两个删除入口。
- [ ] **开发者身份验证**：2026-09-30 起在巴西、印尼、新加坡、泰国生效，2027 年推广到全球。从 Play 发布时，在 Play Console 完成验证即可。
- [ ] Play 的元数据和截图同样不要出现 iPhone、App Store 字样。现在的截图界面是 iOS 样式，Android 版出来后要替换。

## 6. 可选（这次没做）

- 平板截图：需要至少 4 张，边长在 1080–7680 px 之间，比例 16:9 或 9:16，内容必须是平板界面。
- 预览视频：YouTube 链接，前 10 秒要出现真实 App 界面。
