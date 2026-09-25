#!/usr/bin/env python3
"""Find and remove the magenta chroma-key halo around sprite cut-outs.

The problem: the sprites were cut out of a magenta background. Every
cut-out kept a magenta rim or glow along its silhouette. On a dark
background the rim shows as a pink halo.

The rule: a pixel is halo if it is magenta and it connects to the
transparent outside of the sprite through other magenta or near-
transparent pixels. Magenta that the art encloses (Clipi's screen
band, the grid on the glitched screen) does not connect to the
outside, so the rule does not touch it.

The fix, for each halo pixel:
  - Within EDGE_PX of clean (non-magenta, visible) art: take the colour
    of the nearest clean pixel. Keep the alpha, so the anti-aliased
    edge stays smooth. Fade alpha below 128, so the soft glow goes.
  - Farther out: make it fully transparent. This removes the wide glow
    and stray magenta lines on the canvas.

Modes:
  --scan DIR               Report halo pixel counts for every PNG in DIR.
                           Exit 1 if any file has halo pixels.
  --fix FILE... [--out DIR]
                           Remove the halo. In place, or into DIR.

Requires Pillow, NumPy and SciPy.
"""
import argparse
import glob
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

HUE_MIN, HUE_MAX = 285, 345  # the magenta band, in degrees
MIN_SAT = 0.3        # greyer than this is not a hue
MIN_VALUE = 8        # darker than this is not a hue
SOLID_ALPHA = 16     # alpha below this counts as see-through
EDGE_PX = 3          # halo within this distance of clean art is recoloured

EIGHT = np.ones((3, 3), dtype=bool)


def _channels(im):
    a = np.asarray(im.convert("RGBA")).astype(np.int32)
    return a, a[..., 0], a[..., 1], a[..., 2], a[..., 3]


def is_magenta(r, g, b):
    """Elementwise: True where the colour's hue is magenta.

    Hue, not a channel margin: the halo runs from dark (13, 0, 7) through
    pale (194, 80, 150), and all of it sits near hue 325. Skin (about
    20) and the shaded face (about 353) fall outside the band.
    """
    hi = np.maximum(np.maximum(r, g), b)
    lo = np.minimum(np.minimum(r, g), b)
    span = np.maximum(hi - lo, 1)
    hue = np.where(
        hi == r, (60 * (g - b) / span) % 360,
        np.where(hi == g, 60 * (b - r) / span + 120, 60 * (r - g) / span + 240),
    )
    sat = (hi - lo) / np.maximum(hi, 1)
    return (hue >= HUE_MIN) & (hue <= HUE_MAX) & (sat >= MIN_SAT) & (hi >= MIN_VALUE)


def halo_mask(im):
    """Return a boolean array: True for halo pixels."""
    _, r, g, b, alpha = _channels(im)
    mag = is_magenta(r, g, b) & (alpha > 0)
    passable = mag | (alpha < SOLID_ALPHA)
    labels, _ = ndimage.label(passable, structure=EIGHT)
    outside = np.unique(labels[alpha == 0])
    outside = outside[outside != 0]
    reached = np.isin(labels, outside)
    return mag & reached


def scan_image(im):
    """Return (halo_pixels, enclosed_magenta_pixels) for im."""
    _, r, g, b, alpha = _channels(im)
    halo = halo_mask(im)
    enclosed = is_magenta(r, g, b) & (alpha > 0) & ~halo
    return int(halo.sum()), int(enclosed.sum())


def despill_image(im):
    """Return a copy of im with the magenta halo removed."""
    a, r, g, b, alpha = _channels(im)
    halo = halo_mask(im)
    if not halo.any():
        return im.convert("RGBA").copy()
    clean = (alpha >= SOLID_ALPHA) & ~is_magenta(r, g, b)
    if not clean.any():
        out = a.copy()
        out[..., 3] = np.where(halo, 0, alpha)
        return Image.fromarray(out.astype(np.uint8), "RGBA")
    dist, (iy, ix) = ndimage.distance_transform_edt(~clean, return_indices=True)
    near = halo & (dist <= EDGE_PX)
    far = halo & (dist > EDGE_PX)
    out = a.copy()
    for c in range(3):
        out[..., c] = np.where(near, a[..., c][iy, ix], a[..., c])
    faded = np.where(alpha < 128, alpha * alpha // 128, alpha)
    out[..., 3] = np.where(near, faded, alpha)
    out[..., 3] = np.where(far, 0, out[..., 3])
    return Image.fromarray(out.astype(np.uint8), "RGBA")


def cmd_scan(directory):
    found = False
    for path in sorted(glob.glob(os.path.join(directory, "*.png"))):
        halo, enclosed = scan_image(Image.open(path))
        flag = "HALO" if halo else "ok"
        print(f"{flag:4}  halo={halo:6}  enclosed_magenta={enclosed:6}  {os.path.basename(path)}")
        found = found or halo > 0
    return 1 if found else 0


def cmd_fix(files, out_dir):
    for path in files:
        if scan_image(Image.open(path))[0] == 0:
            print(f"clean {path}")
            continue
        fixed = despill_image(Image.open(path))
        target = os.path.join(out_dir, os.path.basename(path)) if out_dir else path
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        fixed.save(target)
        print(f"fixed {target}")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--scan", metavar="DIR", help="scan all PNGs in DIR for magenta halo")
    group.add_argument("--fix", metavar="FILE", nargs="+", help="remove the halo from one or more PNG files")
    parser.add_argument("--out", metavar="DIR", help="write fixed files to DIR instead of in place (--fix only)")
    args = parser.parse_args(argv)
    if args.scan:
        return cmd_scan(args.scan)
    return cmd_fix(args.fix, args.out)


if __name__ == "__main__":
    sys.exit(main())
