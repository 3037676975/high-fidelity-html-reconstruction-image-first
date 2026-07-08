# 案例1：高端企业官网复刻示例

这个案例使用本仓库的 **hybrid image-first** 思路，复刻上方生成的高端企业官网视觉。

## 案例目标

- 做一个高端大气的企业官网首页
- 视觉风格：蓝白科技商务、国际化、咨询 / SaaS / 数字化转型企业
- HTML 负责整体布局、容器定位、页面分栏
- 视觉资产负责 hero 城市图、logo、案例缩略图等复杂视觉内容

## 文件说明

```text
案例1/
  index.html
  style.css
  coverage_inventory.json
  green_source_prompt.md
  assets/
    logo.svg
    hero-city.svg
    case-fintech.svg
    case-manufacturing.svg
    case-healthcare.svg
```

## 打开方法

直接用浏览器打开：

```text
案例1/index.html
```

## 复刻策略

本案例不是把整张生成图作为背景贴进去，而是拆成：

- 顶部导航
- Hero 首屏
- 服务卡片区
- 优势区
- 数据统计条
- 案例区
- 客户 logo 区
- 评价区
- 团队区
- Footer

其中复杂视觉用 `assets/*.svg` 模拟 image-first 资产；结构、布局、分栏、按钮摆放用 HTML/CSS 完成。

真正执行完整 skill 时，可以把 `green_source_prompt.md` 里的资产清单拿去生成 `green_source.png`，再用 `scripts/extract_green_source_assets.py` 抠出透明 PNG 资产。
