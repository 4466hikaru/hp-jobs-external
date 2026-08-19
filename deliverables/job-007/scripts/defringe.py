#!/usr/bin/env python3
"""Remove chromatic leftover on RGBA alpha edges.

For each boundary semi-transparent pixel (alpha 1..250):
  - pull RGB from the nearest fully-opaque interior pixel, and/or
  - set alpha=0 when the pixel is a thin high-chroma / near-white fringe.

Does not eat more than ~2px of real metal highlight: opaque (alpha=255)
pixels that do not neighbor transparent are left untouched. Opaque pixels
that *do* sit on a hard edge are recolored from further interior only when
they look like magenta/purple/green/cyan/white fringe, not gold/metal.

Usage: python3 defringe.py infile outfile
"""
from __future__ import annotations

import sys

import numpy as np
from PIL import Image

try:
    from scipy.ndimage import binary_erosion, distance_transform_edt
except ImportError:  # pragma: no cover
    distance_transform_edt = None
    binary_erosion = None

TRANS_MAX = 15
SEMI_LO, SEMI_HI = 1, 250
CHROMA_HI = 22
EAT_ALPHA_MAX = 80  # only punch out low-alpha fringe, not the 2px metal rim


def _nearest_opaque_indices(opaque: np.ndarray):
    if distance_transform_edt is not None:
        _, (iy, ix) = distance_transform_edt(~opaque, return_indices=True)
        return iy, ix
    # slow fallback: flood nearest via two-pass chamfer
    h, w = opaque.shape
    iy = np.zeros((h, w), dtype=np.int32)
    ix = np.zeros((h, w), dtype=np.int32)
    dist = np.full((h, w), 1e9, dtype=np.float32)
    ys, xs = np.where(opaque)
    iy[opaque] = ys
    ix[opaque] = xs
    dist[opaque] = 0
    # forward
    for y in range(h):
        for x in range(w):
            d = dist[y, x]
            if y > 0 and dist[y - 1, x] + 1 < d:
                d = dist[y - 1, x] + 1
                iy[y, x] = iy[y - 1, x]
                ix[y, x] = ix[y - 1, x]
                dist[y, x] = d
            if x > 0 and dist[y, x - 1] + 1 < dist[y, x]:
                dist[y, x] = dist[y, x - 1] + 1
                iy[y, x] = iy[y, x - 1]
                ix[y, x] = ix[y, x - 1]
    # backward
    for y in range(h - 1, -1, -1):
        for x in range(w - 1, -1, -1):
            if y + 1 < h and dist[y + 1, x] + 1 < dist[y, x]:
                dist[y, x] = dist[y + 1, x] + 1
                iy[y, x] = iy[y + 1, x]
                ix[y, x] = ix[y + 1, x]
            if x + 1 < w and dist[y, x + 1] + 1 < dist[y, x]:
                dist[y, x] = dist[y, x + 1] + 1
                iy[y, x] = iy[y, x + 1]
                ix[y, x] = ix[y, x + 1]
    return iy, ix


def _neighbor_transparent(trans: np.ndarray) -> np.ndarray:
    n = np.zeros_like(trans)
    n[1:, :] |= trans[:-1, :]
    n[:-1, :] |= trans[1:, :]
    n[:, 1:] |= trans[:, :-1]
    n[:, :-1] |= trans[:, 1:]
    n[1:, 1:] |= trans[:-1, :-1]
    n[1:, :-1] |= trans[:-1, 1:]
    n[:-1, 1:] |= trans[1:, :-1]
    n[:-1, :-1] |= trans[1:, 1:]
    return n


def _is_fringe_rgb(r, g, b) -> np.ndarray:
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    chroma = mx - mn
    luma = 0.2126 * r + 0.7152 * g + 0.0722 * b
    high_c = chroma >= CHROMA_HI
    mag = (r > g + 10) & (b > g + 6) & (chroma >= 10)
    white = (luma >= 150) & (chroma <= 35) & (mn >= 110)
    return high_c | mag | white


def _is_bad_chroma(r, g, b) -> np.ndarray:
    """Magenta/purple/green/cyan leftover — not gold/silver metal."""
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    chroma = mx - mn
    mag_purp = (r > g + 8) & (b > g + 6) & (chroma >= 10)
    # green/cyan: G high, R low-ish
    green_cyan = (g > r + 12) & (chroma >= 18)
    return mag_purp | green_cyan


def defringe(arr: np.ndarray) -> np.ndarray:
    out = arr.copy()
    rgb = out[:, :, :3].astype(np.int16)
    alpha = out[:, :, 3]
    r, g, bch = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    opaque = alpha == 255
    if not opaque.any():
        # nothing to sample from — just drop semi fringe
        semi = (alpha >= SEMI_LO) & (alpha <= SEMI_HI)
        out[:, :, 3] = np.where(semi, 0, alpha)
        return out

    trans = alpha < 16
    n_trans = _neighbor_transparent(trans)
    # 2px-eroded opaque: skip the rim so we do not copy leftover magenta inward.
    if binary_erosion is not None:
        deep = binary_erosion(opaque, iterations=2)
    else:
        deep = opaque & ~n_trans
        # one extra homemade erode
        rim = _neighbor_transparent(~deep)
        deep = deep & ~rim
    sample_from = deep if deep.any() else (opaque & ~n_trans)
    if not sample_from.any():
        sample_from = opaque
    iy, ix = _nearest_opaque_indices(sample_from)
    src_rgb = arr[:, :, :3][iy, ix]

    semi = (alpha >= SEMI_LO) & (alpha <= SEMI_HI)
    almost = (alpha >= 251) & (alpha <= 254)
    fringe_rgb = _is_fringe_rgb(r, g, bch)
    bad = _is_bad_chroma(r, g, bch)

    # Semi + almost-opaque rim: pull deep-interior RGB (kills magenta leftover).
    pull = semi | almost
    out[:, :, 0][pull] = src_rgb[:, :, 0][pull]
    out[:, :, 1][pull] = src_rgb[:, :, 1][pull]
    out[:, :, 2][pull] = src_rgb[:, :, 2][pull]

    # Punch the thin outer chromatic / near-white halo. Never punch alpha=255.
    eat = semi & fringe_rgb & n_trans & (alpha <= EAT_ALPHA_MAX)
    out[:, :, 3][eat] = 0

    # Hard-edge opaque: recolor only bad hues (magenta/purple/green/cyan).
    # Gold/silver metal highlights on the rim stay.
    hard = (alpha == 255) & n_trans & bad
    if hard.any():
        out[:, :, 0][hard] = src_rgb[:, :, 0][hard]
        out[:, :, 1][hard] = src_rgb[:, :, 1][hard]
        out[:, :, 2][hard] = src_rgb[:, :, 2][hard]

    return out


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) != 2:
        print("usage: python3 defringe.py infile outfile", file=sys.stderr)
        return 2
    infile, outfile = argv
    im = Image.open(infile)
    arr = np.array(im.convert("RGBA"))
    out = defringe(arr)
    Image.fromarray(out, mode="RGBA").save(outfile)
    return 0


if __name__ == "__main__":
    sys.exit(main())
