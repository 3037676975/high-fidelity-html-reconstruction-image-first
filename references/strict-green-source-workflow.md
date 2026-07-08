# Strict Green-Source Workflow

Use this reference when the user requests screenshot/design-to-HTML conversion under the rewritten **hybrid image-first** workflow.

## Non-Negotiable Order

1. Original screenshot is the only visual reference.
2. Create a coverage inventory that accounts for every visible module, icon, badge, row, panel, and image-like region.
3. Decide the image-first roster: which components will remain image assets and which few items will remain HTML/CSS.
4. Generate `green_source.png` with GPT/img2img for all bitmap-preserved components.
5. Use the bundled clean extractor copied from `green-source-clean-extract` to extract assets from generated green-source sheets.
6. Output transparent PNG assets, `asset_manifest.json`, and `asset_preview.png`.
7. Build `index.html` using extracted bitmap assets as the primary visual surfaces and HTML/CSS as the layout shell.
8. Verify in browser against the reference screenshot and coverage inventory.

Never create a fake green source with Python, Canvas, SVG, CSS, screenshot crops, or manual drawing. Never crop final assets directly from the original screenshot.

## Coverage Inventory Gate

Before generating `green_source.png`, write a coverage inventory for non-trivial screens.

The inventory must include:

- layout containers and structural regions;
- cards, charts, tables, calendar blocks, task panels, activity panels;
- search bars, buttons, badges, pills, icons, avatars, and decorative marks;
- which items will be `layout-html`, `native-text`, `green-source-image`, `complete-card-image`, or `optional-inline-svg`.

Do not proceed until every visible element has a representation.

## Default Image-First Bias

In this rewritten workflow, the following should **normally** go into the image-preserved side unless there is a strong reason not to:

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

HTML/CSS should normally keep responsibility for:

- overall page layout
- container positioning
- page columns
- section structure
- optional title text or simple headings

Do not automatically decompose these image-first components into editable primitives.

## `green_source.png` Rules

- Name the file exactly `green_source.png`.
- Use the highest practical resolution available.
- Use one uniform pure `#00FF00` background.
- Place all reusable image assets directly on the green background.
- Keep generous empty green spacing between assets.
- Use the coverage inventory as the exact asset roster.
- Do not let the model summarize or merge repeated elements.
- Generate each asset large enough for clean extraction and later downscaling.
- If needed, generate additional sheets such as `green_source_02.png`.
- Do not include elements absent from the screenshot.
- Do not place labels, guides, borders, or extra annotations on the sheet.

## What Should Usually Stay As Image Assets

Preserve as image assets whenever fidelity matters:

- cards and grouped card surfaces;
- tables or table sections;
- chart blocks and chart cards;
- calendar widgets;
- search bars and buttons;
- task rows and activity rows;
- badges, pills, and visual chips;
- complex icons and icon clusters;
- avatars, photos, logos, and image-like artwork.

Use `complete-card-image` when the full component should remain intact as one visual block.
Use `green-source-image` when the component is an individual reusable asset or smaller image component.

## What Should Usually Stay As HTML

Keep as HTML/CSS when the element mainly provides structure rather than micro-visual fidelity:

- page shell
- main wrapper containers
- section placement
- columns and alignment scaffolding
- optional title text or simple headings

SVG may be used only if it clearly helps and does not reduce fidelity.

## Clean Extraction Rules

Use the bundled extractor as the required implementation:

```bash
python scripts/extract_green_source_assets.py --source green_source.png --out-dir assets --manifest asset_manifest.json --preview asset_preview.png
```

If white cards, pale controls, soft shadows, or low-contrast edges show green artifacts, rerun with:

```bash
python scripts/extract_green_source_assets.py --source green_source.png --out-dir assets --manifest asset_manifest.json --preview asset_preview.png --edge-mode strong
```

The preview is an acceptance gate:

- compare `asset_preview.png` against the coverage inventory;
- confirm no required image-first asset is missing;
- confirm no green rims, clipped shadows, clipped corners, or merged neighbors;
- confirm output sizes remain suitable for final HTML use.

If the result is weak, regenerate the green-source sheet with larger assets and more spacing. Do not patch missing assets by cropping the original screenshot.

## HTML Reconstruction Rules

- Final page file is `index.html`.
- Use extracted `assets/*.png` as the main visual surfaces for fidelity-sensitive components.
- HTML/CSS should mainly assemble the page and place assets correctly.
- Preserve overall screen composition, module count, hierarchy, spacing, and alignment.
- Do not overcomplicate the page with unnecessary DOM decomposition when image placement yields a better match.
- Do not reference the original screenshot directly in the final page.
- Do not stretch or distort extracted assets.
- If limited editable text is included, keep it small in scope and visually aligned with the screenshot.

## Verification

- Open the page in an independent browser session.
- Capture a verification screenshot at the target viewport.
- Compare against the original screenshot and the coverage inventory.
- Inspect for missing cards, wrong module sizes, poor spacing, bad image scaling, green remnants, and layout drift.
- If a component looks weak because it was redrawn in HTML/CSS, move it into the next green-source asset pass.

## Final Principle

This rewritten workflow is **image-first but not all-image**.

Use code for structure.
Use image assets for fidelity.

When in doubt, prefer the option that keeps the reconstruction visually closer to the original screenshot.
