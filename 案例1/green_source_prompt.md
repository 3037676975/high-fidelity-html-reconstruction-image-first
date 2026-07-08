# 案例1 green_source.png 生成提示词

这个文件用于完整执行 image-first skill 时生成绿底素材图。

## 目标

基于案例1的企业官网参考图，生成一个纯绿色背景的素材 sheet，用于 `extract_green_source_assets.py` 抠出透明 PNG。

## Prompt

Create a high-resolution green-source asset sheet for a premium corporate website homepage. Use a pure uniform #00FF00 background, no gradients, no labels, no crop marks, no border, no shadows on the background, and at least 100 px spacing between every asset. Every asset must be isolated and not touching the canvas edge.

Include the following image-first assets:

1. NEXORA corporate logo mark and wordmark.
2. Hero city skyline / futuristic business district visual with blue glass buildings and data network overlay.
3. Business Impact floating metric card.
4. Client Satisfaction circular progress floating card.
5. Six service cards as complete card images:
   - Digital Transformation
   - Cloud & Infrastructure
   - Data & AI
   - Cybersecurity
   - Enterprise Applications
   - Consulting & Advisory
6. Five advantage items as visual row blocks:
   - Business-First Approach
   - Domain Expertise
   - Agile Delivery
   - Quality & Security
   - Global Presence
7. Dark navy statistics strip as one complete image block.
8. Three case study card thumbnails:
   - Global FinTech Modernization
   - Smart Manufacturing with AI
   - Healthcare Data Platform
9. Testimonial card visual block.
10. Leadership portrait cards.
11. Footer visual block if high-fidelity footer details cannot be redrawn accurately.

Keep each component large enough for clean downscaling in HTML. Preserve rounded corners, shadows, blue/white corporate style, premium spacing, and polished enterprise look.

## Extractor command

```bash
python scripts/extract_green_source_assets.py \
  --source green_source.png \
  --out-dir assets \
  --manifest asset_manifest.json \
  --preview asset_preview.png
```

If white cards or pale UI blocks have green edge artifacts:

```bash
python scripts/extract_green_source_assets.py \
  --source green_source.png \
  --out-dir assets \
  --manifest asset_manifest.json \
  --preview asset_preview.png \
  --edge-mode strong
```
