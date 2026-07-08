# High Fidelity HTML Reconstruction — Image First

这是一个用于“截图 / 设计稿转 HTML”的 skill 规则包。

这个版本不是传统的“全部用 HTML/CSS/SVG 手工重画”，也不是“整张图贴进网页”。它采用更适合高保真还原的 **图像优先混合模式**：

- **图像负责高保真细节**：卡片、表格、图表、日历、搜索框、按钮、复杂图标、头像、活动项、任务项、状态徽章。
- **HTML/CSS 负责结构**：整体布局、容器定位、页面分栏、模块摆放、少量标题文字。

目标是让网页看起来更接近原图，同时保留一定的结构化能力。

## 核心流程

```text
原始截图 / 设计稿
  ↓
覆盖清单 coverage_inventory
  ↓
决定哪些元素用图像，哪些元素用 HTML
  ↓
生成纯绿色背景素材图 green_source.png
  ↓
使用 clean extractor 抠出透明 PNG
  ↓
用 HTML/CSS 进行页面拼装
  ↓
浏览器截图验证
  ↓
继续修正直到接近原图
```

## 推荐用图像资产的元素

- 卡片
- 表格
- 图表
- 日历
- 搜索框
- 按钮
- 复杂图标
- 头像
- 活动项
- 任务项
- 状态徽章

## 推荐用 HTML/CSS 的元素

- 整体布局
- 容器定位
- 页面分栏
- 模块位置关系
- 少量标题文字

## 目录说明

```text
SKILL.md
references/
  asset-coverage-and-editability.md
  strict-green-source-workflow.md
  green-source-clean-extract-integrated.md
scripts/
  extract_green_source_assets.py
agents/
  openai.yaml
examples/
  run-extractor.sh
  run-extractor.ps1
requirements.txt
```

## 抠图命令

```bash
python scripts/extract_green_source_assets.py \
  --source green_source.png \
  --out-dir assets \
  --manifest asset_manifest.json \
  --preview asset_preview.png
```

如果白色卡片、浅色按钮、柔和阴影、低对比度边缘还有绿色污染，可以使用：

```bash
python scripts/extract_green_source_assets.py \
  --source green_source.png \
  --out-dir assets \
  --manifest asset_manifest.json \
  --preview asset_preview.png \
  --edge-mode strong
```

## 输出产物

一个完整任务通常应该输出：

```text
index.html
style.css
assets/*.png
green_source.png
asset_manifest.json
asset_preview.png
coverage_inventory.json 或 coverage_inventory.md
verification_render.png
comparison_side_by_side.png
comparison_diff.png
```

## 设计原则

当不确定一个元素应该用代码还是图片时，问一句：

> 如果用 HTML/CSS/SVG 重画，会不会明显不像原图？

如果会，就优先做成图像资产。  
如果不会，再用 HTML/CSS/SVG。

这就是这个 image-first 版本的核心。
