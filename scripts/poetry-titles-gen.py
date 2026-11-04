#!/usr/bin/env python3
"""Generate per-month lightweight poetry title indexes for the homepage.

The homepage only renders ONE line (today's poem title), but the monthly
archive payload (static/js/today-poetry-YYYYMM.js) is 118-155 KB because it
carries lunar data, solar terms and full recommendation bodies for every day.

This tool derives a ~1 KB sibling file per month:

    static/js/poetry-titles-YYYYMM.js   ->  window.poetryTitles = { "YYYY-MM-DD": "《title》" }

index.html loads only the sibling file; daily-poetry.html keeps using the full
monthly archive. Re-run this whenever a new today-poetry-YYYYMM.js lands
(same event that adds the month), i.e. it has no runtime dependency and adds
no cron job.

Usage:
    python3 scripts/poetry-titles-gen.py            # generate all months found
    python3 scripts/poetry-titles-gen.py --check    # verify siblings are in sync, rc=1 when stale
"""
import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
JS_DIR = ROOT / "static" / "js"
MONTHLY = re.compile(r"today-poetry-(\d{6})\.js$")
PREFIX = "window.dailyPoetryArchive"


def load_archive(path):
    text = path.read_text(encoding="utf-8").strip()
    if not text.startswith(PREFIX):
        raise ValueError(f"{path.name}: unexpected prefix")
    payload = text[len(PREFIX):].lstrip()
    if not payload.startswith("="):
        raise ValueError(f"{path.name}: missing '='")
    payload = payload[1:].strip()
    if payload.endswith(";"):
        payload = payload[:-1]
    return json.loads(payload)


def titles_for(archive):
    out = {}
    for iso, day in archive.items():
        recs = (day or {}).get("recommendations") or []
        if not recs:
            continue
        title = (recs[0] or {}).get("title")
        if title:
            out[iso] = "《%s》" % title
    return out


def render(titles):
    ordered = {k: titles[k] for k in sorted(titles)}
    body = json.dumps(ordered, ensure_ascii=False, separators=(",", ":"))
    return "window.poetryTitles=%s;\n" % body


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="do not write; fail when a sibling is missing/stale")
    args = ap.parse_args()

    months = sorted(p for p in JS_DIR.iterdir() if MONTHLY.search(p.name))
    if not months:
        print("no today-poetry-YYYYMM.js found", file=sys.stderr)
        return 2

    stale = []
    for src in months:
        match = MONTHLY.search(src.name)
        if match is None:  # guarded by the months list comprehension
            continue
        dest = JS_DIR / f"poetry-titles-{match.group(1)}.js"
        expected = render(titles_for(load_archive(src)))
        if dest.exists() and dest.read_text(encoding="utf-8") == expected:
            print(f"ok      {dest.name} ({dest.stat().st_size} B)")
            continue
        if args.check:
            stale.append(dest.name)
            print(f"STALE   {dest.name}")
            continue
        dest.write_text(expected, encoding="utf-8")
        print(f"write   {dest.name} ({dest.stat().st_size} B, from {src.name})")

    if args.check and stale:
        print("stale: " + ", ".join(stale), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
