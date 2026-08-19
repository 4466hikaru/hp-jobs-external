#!/usr/bin/env python3
"""Alpha-edge chromatic fringe detector for job-007 UI parts.

Looks at RGBA alpha-boundary pixels (alpha in 1..250, or opaque pixels
adjacent to alpha<16) and flags ANY chromatic fringe — magenta/purple/
green/cyan/red/yellow plus light-neutral (near-white) fringes.

A pixel is fringe if it sits on the alpha boundary AND
  (high chroma in any hue  OR  near-white RGB with a transparent neighbor).
Magenta/purple is also flagged at modest chroma (the job-006 miss).

Exit non-zero if any file has fringe_count > 0, except startup_backdrop
(opaque full-bleed is allowed).
"""
from __future__ import annotations

import argparse
import os
import sys

import numpy as np
from PIL import Image

HUE_BUCKETS = (
    "magenta",
    "purple",
    "green",
    "cyan",
    "red",
    "yellow",
    "white",
    "other",
)

CHROMA_HI = 22
# magenta/purple even when chroma is modest (job-006 leftover)
MAG_R_OVER_G = 10
MAG_B_OVER_G = 6
MAG_CHROMA_MIN = 10
WHITE_LUMA = 150
WHITE_CHROMA_MAX = 35
WHITE_MIN_CHANNEL = 110
SEMI_LO, SEMI_HI = 1, 250
TRANS_MAX = 15  # alpha < 16
OPAQUE_MIN = 251


def _neighbor_transparent(trans: np.ndarray) -> np.ndarray:
    """8-connected: True if any neighbor has alpha < 16."""
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


def _hue_deg(r: np.ndarray, g: np.ndarray, b: np.ndarray, chroma: np.ndarray) -> np.ndarray:
    """Vectorized HSV hue in degrees [0, 360). Undefined (chroma=0) -> -1."""
    rf = r.astype(np.float32)
    gf = g.astype(np.float32)
    bf = b.astype(np.float32)
    c = chroma.astype(np.float32)
    mx = np.maximum(np.maximum(rf, gf), bf)
    hue = np.full(r.shape, -1.0, dtype=np.float32)
    ok = c > 0
    # R max
    m = ok & (mx == rf)
    hue[m] = np.mod((gf[m] - bf[m]) / c[m], 6.0) * 60.0
    # G max
    m = ok & (mx == gf)
    hue[m] = ((bf[m] - rf[m]) / c[m] + 2.0) * 60.0
    # B max
    m = ok & (mx == bf)
    hue[m] = ((rf[m] - gf[m]) / c[m] + 4.0) * 60.0
    hue[hue >= 360] -= 360
    return hue


def _bucket_arrays(r, g, b, chroma, luma, white_mask) -> dict:
    hue = _hue_deg(r, g, b, chroma)
    mxch = np.maximum(np.maximum(r, g), b).astype(np.float32)
    sat = np.divide(chroma.astype(np.float32), mxch, out=np.zeros_like(mxch), where=mxch > 0)
    buckets = {k: np.zeros(r.shape, dtype=bool) for k in HUE_BUCKETS}
    buckets["white"] = white_mask | ((sat < 0.12) & (luma >= 140) & (chroma < CHROMA_HI))
    rest = ~buckets["white"]
    # magenta: 285–345, or 345–15 when B is elevated vs G (pink, not fire-red)
    mag = rest & (
        ((hue >= 285) & (hue < 345))
        | (((hue >= 345) | ((hue >= 0) & (hue < 15))) & (b > g + 4))
    )
    buckets["magenta"] = mag
    rest = rest & ~mag
    buckets["red"] = rest & ((hue >= 345) | ((hue >= 0) & (hue < 20)))
    rest = rest & ~buckets["red"]
    buckets["yellow"] = rest & (hue >= 20) & (hue < 80)
    rest = rest & ~buckets["yellow"]
    buckets["green"] = rest & (hue >= 80) & (hue < 160)
    rest = rest & ~buckets["green"]
    buckets["cyan"] = rest & (hue >= 160) & (hue < 210)
    rest = rest & ~buckets["cyan"]
    buckets["purple"] = rest & (hue >= 210) & (hue < 285)
    rest = rest & ~buckets["purple"]
    buckets["other"] = rest
    return buckets


def min_opaque_margin(alpha: np.ndarray) -> int:
    h, w = alpha.shape
    op = alpha >= 250
    if not op.any():
        return 0
    rows = np.where(op.any(axis=1))[0]
    cols = np.where(op.any(axis=0))[0]
    return int(
        min(int(rows.min()), int(h - 1 - rows.max()), int(cols.min()), int(w - 1 - cols.max()))
    )


def inspect(path: str) -> dict:
    im = Image.open(path)
    w, h = im.size
    mode = im.mode
    arr = np.array(im.convert("RGBA"))
    rgb = arr[:, :, :3].astype(np.int16)
    alpha = arr[:, :, 3]
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    mx = rgb.max(axis=2)
    mn = rgb.min(axis=2)
    chroma = mx - mn
    luma = 0.2126 * r + 0.7152 * g + 0.0722 * b

    has_alpha = mode in ("RGBA", "LA", "PA") or (alpha < 255).any()
    trans = alpha < 16
    n_trans = _neighbor_transparent(trans)
    semi = (alpha >= SEMI_LO) & (alpha <= SEMI_HI)
    opaque_adj = (alpha >= OPAQUE_MIN) & n_trans
    boundary = semi | opaque_adj

    high_chroma = chroma >= CHROMA_HI
    magentaish = (r > g + MAG_R_OVER_G) & (b > g + MAG_B_OVER_G) & (chroma >= MAG_CHROMA_MIN)
    near_white = (luma >= WHITE_LUMA) & (chroma <= WHITE_CHROMA_MAX) & (mn >= WHITE_MIN_CHANNEL)
    fringe = boundary & (high_chroma | magentaish | (n_trans & near_white))

    buckets = _bucket_arrays(r, g, b, chroma, luma, n_trans & near_white)
    fringe_by = {k: int((fringe & buckets[k]).sum()) for k in HUE_BUCKETS}

    return {
        "file": os.path.basename(path),
        "size": f"{w}x{h}",
        "mode": mode,
        "has_alpha": bool(has_alpha),
        "fringe_count": int(fringe.sum()),
        "fringe_by_hue_bucket": fringe_by,
        "min_opaque_margin": min_opaque_margin(alpha),
        "excepted": "startup_backdrop" in os.path.basename(path),
    }


def format_report(info: dict) -> str:
    fb = info["fringe_by_hue_bucket"]
    bucket_s = ", ".join(f"{k}={fb[k]}" for k in HUE_BUCKETS)
    failed = info["fringe_count"] > 0 and not info["excepted"]
    result = "FAIL" if failed else ("OK (excepted)" if info["excepted"] else "OK")
    return (
        f"{info['file']}\n"
        f"  size: {info['size']}\n"
        f"  mode: {info['mode']}\n"
        f"  has_alpha: {info['has_alpha']}\n"
        f"  fringe_count: {info['fringe_count']}\n"
        f"  fringe_by_hue_bucket: {bucket_s}\n"
        f"  min_opaque_margin: {info['min_opaque_margin']}\n"
        f"  RESULT: {result}"
    )


def collect_pngs(dirpath: str) -> list[str]:
    return sorted(
        os.path.join(dirpath, f)
        for f in os.listdir(dirpath)
        if f.lower().endswith(".png")
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Detect chromatic alpha-edge fringe on UI part PNGs.")
    p.add_argument("--dir", dest="dirpath", help="Directory of PNG parts")
    p.add_argument("files", nargs="*", help="Explicit PNG paths (optional)")
    args = p.parse_args(argv)

    paths: list[str] = []
    if args.dirpath:
        if not os.path.isdir(args.dirpath):
            print(f"error: not a directory: {args.dirpath}", file=sys.stderr)
            return 2
        paths.extend(collect_pngs(args.dirpath))
    paths.extend(args.files)
    if not paths:
        print("error: pass --dir DIR and/or PNG files", file=sys.stderr)
        return 2

    any_fail = False
    reports = []
    for path in paths:
        info = inspect(path)
        reports.append(info)
        print(format_report(info))
        print()
        if info["fringe_count"] > 0 and not info["excepted"]:
            any_fail = True

    n_fail = sum(1 for i in reports if i["fringe_count"] > 0 and not i["excepted"])
    n_ok = len(reports) - n_fail
    print(f"summary: {n_ok} OK, {n_fail} FAIL / {len(reports)} files")
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main())
