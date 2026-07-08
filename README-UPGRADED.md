# Upgrade Notes

This repository contains the image-first rewrite of `high-fidelity-html-reconstruction`.

## What changed

The original rule set favored editable HTML/CSS/SVG. This version changes the default to a **hybrid image-first workflow**:

- Fidelity-sensitive components should become green-source image assets.
- HTML/CSS should primarily assemble layout and positioning.
- SVG is optional and should not be forced when image extraction gives a closer match.

## Image-first defaults

Prefer image assets for:

- cards
- tables
- charts
- calendars
- search bars
- buttons
- complex icons
- avatars
- activity items
- task items
- status badges

Prefer HTML/CSS for:

- overall page layout
- container positioning
- page columns
- module placement
- limited title text

## Extractor

The clean extractor lives at:

```text
scripts/extract_green_source_assets.py
```

Standard use:

```bash
python scripts/extract_green_source_assets.py --source green_source.png --out-dir assets --manifest asset_manifest.json --preview asset_preview.png
```

Use `--edge-mode strong` for white cards, pale controls, and soft UI shadows.
