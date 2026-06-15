# Tileset Extractor

A small command-line tool that scans a tile-based image (e.g. a tile-by-tile
Mario level export) and produces a tileset image containing every unique
tile found in it.

## How it works

The input image is sliced into a grid of fixed-size tiles (16x16 pixels by
default). Each tile is compared against the others, duplicates are
discarded, and the remaining unique tiles are arranged into a single
tileset image saved as `tileset.png` in the same directory as the input
image.

## Requirements

- Python 3
- Pillow

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python create_tileset.py path/to/level.png
```

This creates `tileset.png` alongside `level.png`.

### Options

| Option          | Description                                  | Default |
| --------------- | -------------------------------------------- | ------- |
| `--tile-size N` | Width/height of each tile in pixels          | `16`    |
| `--columns N`   | Number of columns in the output tileset grid | `10`    |

### Examples

Use a custom tile size (e.g. 32x32 tiles):

```bash
python create_tileset.py path/to/level.png --tile-size 32
```

Arrange the output tileset with 8 columns instead of 10:

```bash
python create_tileset.py path/to/level.png --columns 8
```

## Notes

- The input image's width and height must be evenly divisible by the tile
  size, otherwise the script will raise an error.
- Transparency is preserved in the output tileset.
