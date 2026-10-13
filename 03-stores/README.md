# 应用商店素材

渠道调研和规格来源都在 `00-research/Hey-Atu-Research.html`。

| 渠道 | 文件夹 | 文案和检查清单 |
|---|---|---|
| Google Play（Android） | `google-play/`：图标 512、Feature graphic 1024×500、7 张 1080×1920 截图 | `google-play/listing.md` |
| App Store（iOS / iPadOS） | `app-store/`：iPhone 1206×2622（必需）和 1320×2868 各 7 张、iPad 2752×2064 4 张；图标随构建包上传 | `app-store/listing.md` |
| Claude / ChatGPT 目录、Google 登录同意页 | `ai-directories/`：图标 120 / 512 / 1024 | — |

## 现在的缺口

1. Google Play 截图里现在是 iOS 界面。Android 版能跑起来后，换成 Android 截图，模板不用改（`09-generator/build_play.py`）。
2. 仓库里还没有 Android 工程。Play 要求上传 `.aab`，并且 target API 36。
3. 两个商店都需要审核演示环境，因为审核员手上没有你们的 Mac。
