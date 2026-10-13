# App Store 上架信息 · Hey Atu（iOS / iPadOS）

状态：Apple Developer Program 还在审批。审批通过之前，下面这些都可以先准备好；通过后在 App Store Connect 建 App 记录，把名字 "Hey Atu" 占住。

## 1. 图片素材（对照 App Store Connect 现行规格，2026-10 查证）

| 位置 | 文件 | 规格要求 | 本包 |
|---|---|---|---|
| App icon | 随构建包上传：`02-app-icon/ios/AppIcon.appiconset/` | 1024×1024、不透明、不加圆角（系统自动加遮罩）；可额外提供 Dark 和 Tinted 外观 | ✅ 默认、Dark、Tinted 三种外观；另有备份 `01-app-icon/app-store-icon-1024.png` |
| iPhone 截图（必需） | `03-iphone-6.3in-1206x2622/` | 必需档位是「带灵动岛的中尺寸屏」：1206×2622 或 1179×2556；1–10 张；PNG/JPG，不能有 alpha | ✅ 7 张 1206×2622 |
| iPhone 大屏截图（建议） | `02-iphone-6.9in-1320x2868/` | 1320×2868；不传的话，系统会把其他档位缩放后补上 | ✅ 7 张 |
| iPad 截图（App 支持 iPad 时必需） | `04-ipad-13in-2752x2064/` | 13 寸：2752×2064 横屏，或 2064×2752 竖屏 | ✅ 4 张横屏 |
| App Preview 视频 | — | 可选；每个尺寸最多 3 段 | 暂不提供 |

截图上的界面都是 iOS 的真实界面，取自 heyatu.com 线上演示，演示按当前 App 还原。**App Store 的截图和元数据里不能出现 Android、Google Play 等其他移动平台的名称或图像**（审核指南 2.3.10）。截图必须展示 App 的使用状态，不能只放标题图、登录页或启动页（2.3.3）。

## 2. 文案

| 字段 | 上限 | 建议 |
|---|---|---|
| Name | 30 | `Hey Atu` |
| Subtitle | 30 | `Keep your AI working`（20），备选 `Your AI agent, from anywhere`（28） |
| Promotional text | 170 | `Your own AI runs on your own computer. Hey Atu lets you check progress, answer questions and pick up where you left off, right from your phone.`（143） |
| Keywords | 100 字节，逗号分隔 | `ai agent,remote,mac,linux,assistant,coding,terminal,automation,todo,updates,llm,agentic,workflow`（96 字节）。**规则禁止写其他公司或 App 的名字**，所以 Claude、ChatGPT 都不要放进关键词；App 名字本身已经能被搜到，也不用再写 |
| Description | 4000 | 和 Google Play 的 Full description 用同一份（见 `../google-play/listing.md`）。描述里列模型厂商名属于功能说明，可以写，但不要堆砌 |
| Category | — | 主类别 Developer Tools，副类别 Productivity |
| Support URL | 必填 | 必须能找到联系方式，例如 `https://heyatu.com/support` 或 support@ 的页面 |
| Marketing URL | 选填 | `https://heyatu.com` |
| Privacy Policy URL | 必填 | `https://heyatu.com/privacy` |
| Copyright | 必填 | `2026 Sui Qian`（和官网法律页的运营者名称保持一致） |

## 3. 非视觉项（负责人：产品）

- [ ] App Privacy（隐私标签）：和 Google Play 的 Data safety 用同一份数据清单来填。
- [ ] 年龄分级问卷。
- [ ] App Review 信息：审核员手上没有 Mac，也没有你们的手机。需要提供**审核演示环境**（发布计划里的 reviewer demo），否则会被 2.1 卡住。
- [ ] 如果 App 里有付费：需要签 Paid Apps 协议、配置 StoreKit（发布计划 E 节）。
- [ ] 截图里的账号和数据都是虚构的示例（2.3.9）：现在的演示内容都是示例数据，满足要求。
