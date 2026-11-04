#!/usr/bin/env python3
"""Perf regression nail for the static homepage.

No build step, no test runner in this repo -> this script is the guard that
keeps the first-visit payload from silently creeping back up.

Checks
  1. gzip budgets per first-visit asset on index.html
  2. first-visit request set: no monthly poetry pack (today-poetry-*.js),
     only the ~1 KB poetry-titles-*.js index
  3. framing guarantees: avif preload, preset background colour, sized <img>
  4. ?t= parity between index.html and wechat.html (AGENTS.md cache-bust rule)
  5. poetry title indexes are in sync with the monthly archives

Exit code 0 = all green, 1 = at least one assertion failed.

Usage
    python3 scripts/perf-check.py            # human readable
    python3 scripts/perf-check.py --quiet    # only failures + summary
"""
import argparse
import gzip
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# gzip byte budgets (measured 2026-11-04; leave ~25-40% headroom over actual)
BUDGETS = {
    "index.html": 8_000,
    "static/css/index.css": 3_500,
    "static/js/index.js": 2_500,
    "static/js/poetry-titles-202611.js": 1_500,   # any month, matched by glob below
    "static/img/bear01-1600.avif": 100_000,
    "static/img/bear01-1600.webp": 85_000,
    "static/img/logo-260.webp": 15_000,
    "static/img/favicon-64.png": 15_000,
    "static/img/wechat-qr-400.png": 45_000,
}


def gz_size(path):
    with open(path, "rb") as fh:
        return len(gzip.compress(fh.read(), 9))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    failures = []
    notes = []

    def check(ok, label, detail=""):
        if not ok:
            failures.append(f"{label}{(' — ' + detail) if detail else ''}")
        elif not args.quiet:
            print(f"PASS  {label}{(' — ' + detail) if detail else ''}")

    index = (ROOT / "index.html").read_text(encoding="utf-8")

    # 1. gzip budgets
    for rel, budget in BUDGETS.items():
        if "*" in rel:
            continue
        p = ROOT / rel
        if not p.exists():
            check(False, f"budget {rel}", "file missing")
            continue
        size = gz_size(p)
        check(size <= budget, f"budget {rel}", f"{size} B ≤ {budget} B")

    # any poetry-titles-*.js must stay tiny
    for p in sorted((ROOT / "static/js").glob("poetry-titles-*.js")):
        size = gz_size(p)
        check(size <= 1_500, f"budget static/js/{p.name}", f"{size} B ≤ 1500 B")

    # 2. first-visit request set
    check("today-poetry-" not in index, "no monthly poetry pack on the homepage",
          "index.html must load poetry-titles-*.js only")
    check("poetry-titles-" in index, "poetry title index wired", "poetry-titles-YYYYMM.js")

    # 3. framing guarantees
    check('type="image/avif"' in index and "rel=\"preload\"" in index,
          "hero avif preload present")
    check("background: #b0b2b8" in index, "preset background colour inlined",
          "#b0b2b8 (photo average)")
    check(re.search(r'<img id="background"[^>]*width="\d+"[^>]*height="\d+"', index) is not None,
          "hero <img> carries intrinsic width/height", "avoids CLS")
    check("<picture>" in index, "hero served through <picture>", "avif → webp → jpg")

    # 3b. layout contract (上一版布局：48px 归档图标行 + 底部药丸栈；5 个入口 / 2 个区块标题)
    check('class="icon-links"' in index and 'class="bottom-stack"' in index,
          "layout: icon-links row + bottom pill stack present")
    check('class="app-band"' not in index, "layout: no app-band drift")
    n_band = index.count('<a class="now-card"')
    m_icons = re.search(r'<div class="icon-links">(.*?)</div>', index, re.S)
    n_icon = m_icons.group(1).count("<a ") if m_icons else 0
    check(n_band + n_icon == 5, "layout: exactly 5 entries", f"pills={n_band} + icon-links={n_icon}")
    n_titles = index.count('class="now-title"')
    check(n_titles == 2, "layout: 2 section titles", f"found {n_titles}")

    # 4. ?t= parity
    stamps = {}
    for name in ("index.html", "wechat.html"):
        vals = set(re.findall(r"\?t=(\d{9,})", (ROOT / name).read_text(encoding="utf-8")))
        stamps[name] = vals
        check(len(vals) == 1, f"{name} has one uniform ?t=", f"found {sorted(vals)}")
    check(stamps["index.html"] == stamps["wechat.html"],
          "?t= parity index.html ↔ wechat.html", f"{sorted(stamps['index.html'])} vs {sorted(stamps['wechat.html'])}")

    # 5. poetry indexes in sync
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "poetry-titles-gen.py"), "--check"],
                       capture_output=True, text=True)
    check(r.returncode == 0, "poetry-titles-*.js in sync with monthly archives",
          (r.stderr or r.stdout).strip().splitlines()[-1] if (r.returncode and (r.stderr or r.stdout)) else "")

    print()
    if failures:
        print(f"FAIL  {len(failures)} assertion(s) failed")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"OK    all perf assertions passed")
    for n in notes:
        print(f"note  {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
