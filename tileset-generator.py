#!/usr/bin/env python3
"""
Extract every unique tile from a tile-based image (e.g. a Mario level PNG)
and save them as a single tileset image.

Usage:
    python create_tileset.py path/to/level.png
    python create_tileset.py path/to/level.png --tile-size 16 --columns 10

The output "tileset.png" is written into the same directory as the input
image.
"""

import argparse
import math
import os

from PIL import Image


def build_tileset(image_path, tile_size=16, columns=10):
    img = Image.open(image_path).convert("RGBA")
    width, height = img.size

    if width % tile_size or height % tile_size:
        raise ValueError(
            f"Image dimensions {width}x{height} are not evenly divisible "
            f"by tile size {tile_size}. Pass a different --tile-size."
        )

    cols = width // tile_size
    rows = height // tile_size

    seen = set()
    tiles = []

    for r in range(rows):
        for c in range(cols):
            box = (
                c * tile_size,
                r * tile_size,
                (c + 1) * tile_size,
                (r + 1) * tile_size,
            )
            tile = img.crop(box)
            key = tile.tobytes()
            if key not in seen:
                seen.add(key)
                tiles.append(tile)

    n = len(tiles)
    tileset_cols = min(columns, n)
    tileset_rows = math.ceil(n / tileset_cols)

    tileset = Image.new(
        "RGBA", (tileset_cols * tile_size, tileset_rows * tile_size), (0, 0, 0, 0)
    )
    for idx, tile in enumerate(tiles):
        x = (idx % tileset_cols) * tile_size
        y = (idx // tileset_cols) * tile_size
        tileset.paste(tile, (x, y))

    out_dir = os.path.dirname(os.path.abspath(image_path))
    tileset_path = os.path.join(out_dir, "tileset.png")
    tileset.save(tileset_path)

    print(f"Image size:    {width}x{height} px  ({cols}x{rows} tiles)")
    print(f"Unique tiles:  {n}")
    print(
        f"Tileset saved: {tileset_path}  "
        f"({tileset.width}x{tileset.height} px, {tileset_cols} cols x {tileset_rows} rows)"
    )

    return tileset_path


def main():
    parser = argparse.ArgumentParser(
        description="Extract a tileset of unique tiles from a tile-based image."
    )
    parser.add_argument(
        "image_path", help="Path to the source image (e.g. a tile-by-tile level PNG)."
    )
    parser.add_argument(
        "--tile-size",
        type=int,
        default=16,
        help="Tile width/height in pixels (default: 16).",
    )
    parser.add_argument(
        "--columns",
        type=int,
        default=10,
        help="Number of columns in the output tileset image (default: 10).",
    )
    args = parser.parse_args()

    build_tileset(args.image_path, args.tile_size, args.columns)


if __name__ == "__main__":
    main()
