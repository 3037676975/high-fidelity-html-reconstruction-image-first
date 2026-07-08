#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract transparent assets from a pure-green sprite sheet.")
    parser.add_argument("--source", default="green_source.png")
    parser.add_argument("--out-dir", default="assets")
    parser.add_argument("--manifest", default="asset_manifest.json")
    parser.add_argument("--preview", default="asset_preview.png")
    parser.add_argument("--min-component", type=int, default=220)
    parser.add_argument("--padding", type=int, default=10)
    parser.add_argument("--recrop-padding", type=int, default=6)
    parser.add_argument("--edge-mode", choices=("normal", "strong"), default="normal")
    parser.add_argument("--keep-existing", action="store_true")
    return parser.parse_args()


def is_pure_edge_green(px: tuple[int, int, int, int]) -> bool:
    r, g, b, a = px
    return a > 0 and g > 215 and r < 45 and b < 45


def is_green_spill(px: tuple[int, int, int, int], strong: bool) -> bool:
    r, g, b, a = px
    if a == 0:
        return False
    if strong:
        return g > 145 and g > r * 1.12 and g > b * 1.08
    return g > 155 and g > r * 1.18 and g > b * 1.12


def flood_external_background(img: Image.Image) -> list[list[bool]]:
    w, h = img.size
    pix = img.load()
    bg = [[False] * w for _ in range(h)]
    q: deque[tuple[int, int]] = deque()

    def add(x: int, y: int) -> None:
        if not bg[y][x] and is_pure_edge_green(pix[x, y]):
            bg[y][x] = True
            q.append((x, y))

    for x in range(w):
        add(x, 0)
        add(x, h - 1)
    for y in range(h):
        add(0, y)
        add(w - 1, y)

    while q:
        x, y = q.popleft()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and not bg[ny][nx] and is_pure_edge_green(pix[nx, ny]):
                bg[ny][nx] = True
                q.append((nx, ny))
    return bg


def find_components(bg: list[list[bool]], min_component: int) -> list[tuple[int, int, int, int, int]]:
    h = len(bg)
    w = len(bg[0])
    seen = [[False] * w for _ in range(h)]
    comps: list[tuple[int, int, int, int, int]] = []
    for y in range(h):
        for x in range(w):
            if seen[y][x] or bg[y][x]:
                continue
            q: deque[tuple[int, int]] = deque([(x, y)])
            seen[y][x] = True
            xs: list[int] = []
            ys: list[int] = []
            count = 0
            while q:
                cx, cy = q.popleft()
                xs.append(cx)
                ys.append(cy)
                count += 1
                for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                    if 0 <= nx < w and 0 <= ny < h and not seen[ny][nx] and not bg[ny][nx]:
                        seen[ny][nx] = True
                        q.append((nx, ny))
            if count >= min_component:
                comps.append((min(xs), min(ys), max(xs) + 1, max(ys) + 1, count))
    return sorted(comps, key=lambda item: (item[1], item[0]))


def clean_crop(crop: Image.Image, strong: bool, recrop_padding: int) -> Image.Image:
    crop = crop.convert("RGBA")
    w, h = crop.size
    pix = crop.load()
    bg = flood_external_background(crop)

    # Protect assets that are mostly real green/teal by only removing connected edge green.
    content = 0
    greenish = 0
    whiteish = 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = pix[x, y]
            if a and not bg[y][x]:
                content += 1
                if is_green_spill((r, g, b, a), strong):
                    greenish += 1
                if r > 210 and g > 210 and b > 210:
                    whiteish += 1
    protect_green_subject = content > 0 and greenish / content > 0.32 and whiteish / content < 0.35

    for y in range(h):
        for x in range(w):
            r, g, b, a = pix[x, y]
            if bg[y][x]:
                pix[x, y] = (0, 0, 0, 0)
                continue
            if not protect_green_subject and is_green_spill((r, g, b, a), strong):
                touches_transparent = False
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if not (0 <= nx < w and 0 <= ny < h) or bg[ny][nx]:
                        touches_transparent = True
                        break
                if touches_transparent:
                    pix[x, y] = (r, min(255, int(g * 0.72)), b, a)

    box = crop.getbbox()
    if not box:
        return crop
    x0, y0, x1, y1 = box
    x0 = max(0, x0 - recrop_padding)
    y0 = max(0, y0 - recrop_padding)
    x1 = min(w, x1 + recrop_padding)
    y1 = min(h, y1 + recrop_padding)
    return crop.crop((x0, y0, x1, y1))


def make_preview(files: list[Path], preview_path: Path) -> None:
    if not files:
        Image.new("RGBA", (320, 180), (245, 247, 252, 255)).save(preview_path)
        return
    cell_w, cell_h, cols = 180, 150, 8
    rows = math.ceil(len(files) / cols)
    sheet = Image.new("RGBA", (cols * cell_w, rows * cell_h), (245, 247, 252, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for i, file in enumerate(files):
        img = Image.open(file).convert("RGBA")
        img.thumbnail((150, 110), Image.LANCZOS)
        x = (i % cols) * cell_w + (cell_w - img.width) // 2
        y = (i // cols) * cell_h + 12
        sheet.alpha_composite(img, (x, y))
        draw.text(((i % cols) * cell_w + 8, (i // cols) * cell_h + 128), file.name, fill=(40, 50, 70, 255), font=font)
    sheet.save(preview_path)


def main() -> None:
    args = parse_args()
    source = Path(args.source)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    if not args.keep_existing:
        for old in out_dir.glob("asset_*.png"):
            old.unlink()

    img = Image.open(source).convert("RGBA")
    w, h = img.size
    bg = flood_external_background(img)
    comps = find_components(bg, args.min_component)
    manifest = []

    for idx, (x0, y0, x1, y1, count) in enumerate(comps, 1):
        sx0 = max(0, x0 - args.padding)
        sy0 = max(0, y0 - args.padding)
        sx1 = min(w, x1 + args.padding)
        sy1 = min(h, y1 + args.padding)
        crop = img.crop((sx0, sy0, sx1, sy1))
        output = clean_crop(crop, args.edge_mode == "strong", args.recrop_padding)
        name = f"asset_{idx:03d}.png"
        output.save(out_dir / name)
        manifest.append({
            "file": name,
            "type": "transparent",
            "usage": "generated visual asset",
            "source_bbox": [x0, y0, x1, y1],
            "source_size": [w, h],
            "crop_size": [sx1 - sx0, sy1 - sy0],
            "output_size": [output.width, output.height],
            "transparency": "external green flood-fill alpha, green-spill cleanup, alpha recrop",
            "padding": args.padding,
            "recrop_padding": args.recrop_padding,
            "cleanup_mode": args.edge_mode,
            "pixel_count": count,
        })

    Path(args.manifest).write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    make_preview(sorted(out_dir.glob("asset_*.png")), Path(args.preview))
    print(f"exported {len(manifest)} assets")
    print(f"manifest: {args.manifest}")
    print(f"preview: {args.preview}")


if __name__ == "__main__":
    main()
