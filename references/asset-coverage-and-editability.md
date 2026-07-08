# Asset Coverage And Editability

Use this reference before generating green-source sheets or building HTML. This rewritten version prioritizes **visual fidelity first**, while still keeping a usable HTML layout shell.

## Goal

Do not aim for maximum editability at the cost of visual loss.

The target is a **hybrid image-first reconstruction**:

- major visual UI components are preserved as image assets;
- HTML/CSS handles the page framework, layout, and limited text;
- optional SVG is used only when it clearly helps.

## Why Fidelity Breaks In Editable-First Reconstructions

Visual loss usually happens for one of these reasons:

- cards are rebuilt in CSS but their exact border, radius, highlight, and shadow treatment no longer match;
- tables are redrawn structurally, but row density, separators, and badges feel off;
- charts are recreated in SVG/CSS but lose their exact visual style;
- calendars, tasks, and activity rows are decomposed too aggressively and stop looking like the original;
- small icon groups are approximated rather than preserved;
- the workflow assumes "simple UI should always be redrawn" even when redrawing noticeably hurts fidelity.

## Coverage Inventory

Before `green_source.png`, make a coverage inventory grouped by screen region. For each item, record:

- `id`: stable short name such as `sidebar-overview-card` or `tasks-row-01`
- `region`: sidebar, header, main content, right rail, footer, overlay, etc.
- `kind`: card, chart, table, calendar, search-bar, button, icon, avatar, task-row, activity-row, badge, text, container
- `representation`: `layout-html`, `native-text`, `green-source-image`, `complete-card-image`, or `optional-inline-svg`
- `visual notes`: radius, shadow, color, density, internal details, and placement
- `required`: true for every visible screenshot element unless the user explicitly allows simplification

Count repeated elements. Do not write vague inventory lines such as "some icons" or "several rows".

## New Default Representation Rules

### Use `complete-card-image` for

- dashboard cards
- table blocks
- chart panels
- calendar panels
- task panels when they are visually dense
- activity panels when they are visually dense
- composite widgets whose internal look matters more than editability

### Use `green-source-image` for

- buttons when their exact look matters
- search bars when their exact look matters
- badges, pills, and status chips
- complex icons and icon sets
- avatars, photos, and portraits
- task rows and activity rows when they should look exactly like the screenshot
- small grouped visual elements that are easy to miss or hard to redraw faithfully

### Use `layout-html` for

- page shell
- outer containers
- multi-column structure
- section placement
- spacing relationships
- wrapper boxes whose main purpose is layout, not precise micro-styling

### Use `native-text` for

- a small amount of title text or simple labels when useful
- optional headings that benefit from being editable

### Use `optional-inline-svg` only when

- it genuinely improves fidelity or simplicity;
- the component is simple enough that SVG recreation will not visibly weaken the result.

Do not force ordinary icons, charts, or badges to be SVG if preserving them as extracted images gives a closer match.

## Default Image-First Asset Roster

Unless the user explicitly asks for more editability, the following should normally be treated as image assets:

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

This is the preferred default for this rewritten skill.

## Green-Source Prompt Requirements

The prompt for the image model must include the exact asset roster assigned to `green-source-image` or `complete-card-image`.

Require:

- pure uniform `#00FF00` background;
- no labels, crop marks, grid lines, background shadows, or texture;
- generous spacing between assets;
- no asset touching another asset or canvas edge;
- no green rim or green reflected light;
- exact count from the coverage inventory;
- large enough asset size for clean extraction and later downscaling.

Recommended minimums:

- full cards/panels: at least 2x final display size when practical;
- buttons/search bars/badges: large enough to retain edge quality and shadows;
- complex icons: at least 160 x 160;
- avatars: at least 192 x 192, preferably larger;
- dense table or calendar modules: large enough that row separators and small text remain visually stable.

If crowded, split into multiple sheets. Do not shrink everything just to keep one sheet.

## Extraction Acceptance Rules

After extraction, inspect `asset_preview.png` and compare it with the coverage inventory.

Confirm:

- no required asset is missing;
- no green fringe remains;
- no cards or buttons are clipped;
- rounded corners and shadows survive correctly;
- neighboring components are not merged;
- output sizes are sufficient;
- assets assigned as images really cover the fidelity-sensitive parts of the screen.

If fidelity-critical elements still look weak when rebuilt in HTML/CSS, move them into the next image asset pass instead of accepting a degraded result.

## HTML Assembly Rules

HTML should act mainly as a structured placement system.

Use HTML/CSS for:

- global layout
- containers
- section wrappers
- page columns
- relative positioning
- optional simple titles

Use extracted image assets for:

- the majority of fidelity-sensitive component surfaces
- visually dense widgets
- components whose radius/shadow/detail treatment is hard to redraw accurately

Do not rebuild image-first components in CSS merely because it seems cleaner. The priority is the final visual match.

## Anti-Omission Rule

Nothing visible may disappear.

If an element is not going to be represented in HTML, it must be present in the green-source asset roster. If it is not in the asset roster, it must be explicitly built in HTML/CSS. No visible item may exist in neither place.

## Decision Rule

When deciding between code and image, use this test:

**If recreating the element in HTML/CSS/SVG would noticeably reduce screenshot fidelity, keep it as an image asset.**

That rule overrides the old assumption that simple UI should always be coded.
