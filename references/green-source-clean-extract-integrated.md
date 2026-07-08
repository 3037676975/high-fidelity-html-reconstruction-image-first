# Green Source Clean Extract Integrated

This skill includes a bundled clean extractor at:

```text
scripts/extract_green_source_assets.py
```

Use it to extract transparent PNG assets from generated green-source sheets.

## Required source image

The extractor must read a generated green-source image, normally:

```text
green_source.png
```

The source sheet must have a pure `#00FF00` background and separated assets.

Do not use the original screenshot as the extraction source. The original screenshot is only a visual reference.

## Standard command

```bash
python scripts/extract_green_source_assets.py \
  --source green_source.png \
  --out-dir assets \
  --manifest asset_manifest.json \
  --preview asset_preview.png
```

## Strong cleanup command

Use this when pale UI cards, white buttons, soft shadows, or low-contrast edges retain green spill:

```bash
python scripts/extract_green_source_assets.py \
  --source green_source.png \
  --out-dir assets \
  --manifest asset_manifest.json \
  --preview asset_preview.png \
  --edge-mode strong
```

## What the extractor does

The extractor should:

1. open the generated green-source PNG;
2. identify external connected green background from the canvas edges;
3. find non-background connected components;
4. crop each component with padding;
5. remove external green and green spill;
6. preserve legitimate green or teal content inside assets when possible;
7. re-crop each output to its alpha bounds;
8. export transparent PNG files into `assets/`;
9. write `asset_manifest.json`;
10. write `asset_preview.png`.

## Acceptance gate

After every extraction, inspect `asset_preview.png`.

Reject the output and regenerate `green_source.png` if:

- required assets are missing;
- two assets are merged;
- an asset is clipped;
- green rim remains;
- white/pale UI edges are damaged;
- rounded corners or shadows are cut off;
- output resolution is too small for the final HTML placement.

For this image-first skill, the extractor is especially important because cards, tables, charts, calendars, buttons, badges, and other visual UI blocks may be image assets rather than CSS redraws.
