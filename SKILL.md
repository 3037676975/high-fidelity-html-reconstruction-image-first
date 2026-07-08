---
name: high-fidelity-html-reconstruction
description: High-fidelity screenshot/design-to-HTML reconstruction with an integrated clean green-source extraction engine, rewritten for a hybrid image-first workflow. Use when converting screenshots, UI mockups, landing pages, app screens, or web page screenshots into visually faithful HTML where major visual components are preserved as extracted image assets and HTML is used mainly for page structure, positioning, and limited editable text.
---

# High Fidelity HTML Reconstruction

## Image-First Hybrid Version

This version is intentionally **not** extreme editable-first and **not** extreme all-image. It follows a **hybrid image-first** strategy:

- Use **image assets first** for visual components that usually lose fidelity when redrawn by HTML/CSS/SVG.
- Use **HTML/CSS** mainly for overall layout, containers, section positioning, page columns, spacing control, and a small amount of optional editable text.
- Use the bundled `green-source-clean-extract` engine to extract clean transparent assets from generated green-source sheets.

The goal is:

`reference screenshot only -> coverage inventory -> decide image-first asset roster -> generate green_source.png -> extract clean PNG assets -> assemble HTML layout with extracted image assets -> browser verification`

## Core Rule

Treat the uploaded screenshot/design as the only visual reference.

This skill prioritizes **visual fidelity** over deep DOM editability. If a component is likely to look noticeably worse when manually redrawn, preserve it as an image asset instead of forcing it into CSS/SVG.

Do not skip, reorder, or fake any step when the user requests this workflow. A reconstruction is incomplete if visible cards, table sections, charts, calendar blocks, task/activity rows, icons, badges, or image-like modules are omitted or over-simplified.

## Required References

Before acting, read:

- `references/strict-green-source-workflow.md`
- `references/asset-coverage-and-editability.md`
- `references/green-source-clean-extract-integrated.md`
- `scripts/extract_green_source_assets.py`

If other screenshot-to-HTML guidance is available, use it only as secondary support. Do not let it override this skill's image-first asset strategy.

## Representation Policy

### Prefer image assets for

- cards and grouped UI blocks
- tables and table-like blocks
- chart cards, chart surfaces, and chart widgets
- calendars and schedule widgets
- search boxes and search bars when their exact visual treatment matters
- buttons when exact visual fidelity matters
- complex icons and icon groups
- avatars and photos
- activity items and task items when their internal visual treatment is dense
- status badges, pills, and decorative marks
- any composite component whose rounded corners, shadows, borders, internal spacing, or ornamentation are hard to match precisely with CSS/SVG

### Prefer HTML/CSS for

- overall page layout
- container positioning
- page columns and section framing
- spatial composition and stacking order
- a small amount of title text or simple labels when helpful

### Use SVG sparingly

Inline SVG is optional and should be used only when it clearly improves fidelity or simplicity. Do not force ordinary icons, charts, or pills to be SVG if using extracted image assets is more faithful.

## Workflow

1. **Create the coverage inventory**
   - Enumerate every visible region and small element before generating assets.
   - Group by screen region: sidebar, header, main content, cards, right rail, footer, overlays, etc.
   - Assign each item one representation:
     - `layout-html`
     - `native-text`
     - `green-source-image`
     - `complete-card-image`
     - `optional-inline-svg`
   - Default toward `green-source-image` or `complete-card-image` for fidelity-sensitive UI pieces.
   - Write `coverage_inventory.md` or `coverage_inventory.json` for non-trivial screens.

2. **Choose the image-first asset roster**
   - Decide which components should be preserved as complete image blocks.
   - In this skill version, the default preferred image roster includes:
     - cards
     - tables
     - charts
     - calendar blocks
     - search bars
     - buttons
     - complex icons
     - avatars
     - activity rows
     - task rows
     - status badges
   - Keep HTML responsibilities narrow: structure, placement, section wrappers, and optionally a small amount of text.
   - If a component is not extracted as an image asset, it must still be represented explicitly in HTML/CSS and must not be silently dropped.

3. **Generate `green_source.png`**
   - Use GPT/img2img or the best available image generation tool with the screenshot as the visual reference.
   - Generate one high-resolution green-background sprite sheet named exactly `green_source.png`.
   - The background must be uniform pure `#00FF00`.
   - Place every required asset on the green background with generous spacing.
   - Use the coverage inventory as the exact roster; do not let the model summarize, omit, or merge assets.
   - Generate assets large enough for clean downscaling in HTML.
   - If the sheet would become crowded, generate additional sheets such as `green_source_02.png`.
   - Do not create local substitutes with Python, Canvas, SVG, screenshot crops, or manual drawing.

4. **Extract assets with the bundled clean extractor**
   - Use this skill's bundled `scripts/extract_green_source_assets.py` as the required extraction implementation.
   - Canonical command:

     ```bash
     python scripts/extract_green_source_assets.py --source green_source.png --out-dir assets --manifest asset_manifest.json --preview asset_preview.png
     ```

   - If pale cards, soft shadows, white controls, or low-contrast UI edges show green contamination, rerun with `--edge-mode strong`.
   - Compare `asset_preview.png` against the coverage inventory.
   - If assets are missing, clipped, merged, too small, or contaminated, regenerate the green-source sheet. Do not silently continue.

5. **Build the page**
   - Create `index.html`.
   - Use extracted assets as the primary visual surfaces for fidelity-sensitive UI.
   - Use HTML/CSS for page skeleton, wrappers, positioning, columns, section blocks, and optional title text.
   - Do not over-redraw image-first components as CSS/SVG unless the user explicitly prefers editability over fidelity.
   - Use CSS to place and size image assets accurately.
   - Preserve module count, hierarchy, alignment, spacing, and overall screen composition.
   - Do not add components that are absent from the screenshot.

6. **Verify**
   - Open `index.html` in a browser-like environment at the target viewport.
   - Save a verification screenshot.
   - Compare it against the reference screenshot and the coverage inventory.
   - Check for omitted modules, wrong proportions, missing badges/icons, stretched assets, green artifacts, and poor visual alignment.
   - If the page is visually weak because too many elements were redrawn in CSS/SVG, move those components into the next green-source asset pass.

## Output Checklist

Deliver:

- `green_source.png`
- additional `green_source_*.png` files when needed
- `assets/*.png`
- `asset_manifest.json`
- `asset_preview.png`
- `coverage_inventory.md` or `coverage_inventory.json`
- `index.html`
- any needed CSS/JS files
- verification screenshot when possible

## Decision Principle

When uncertain, ask:

**Will redrawing this component reduce fidelity?**

- If **yes**, preserve it as an image asset.
- If **no**, keep it in HTML/CSS.

This hybrid image-first rule is the default behavior for this rewritten skill.
