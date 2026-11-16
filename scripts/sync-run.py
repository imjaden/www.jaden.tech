#!/usr/bin/env python3
"""sync-run — 门户同步面编排器（JT-CL005 pull 模型）。

定位：**调度在本仓，渲染在上游**。
  * mode=local   -> 本仓脚本生成（poetry-titles-gen.py）
  * mode=mirror  -> 本仓投影脚本拉上游产物（tokens-tracker-mirror.py）
  * mode=emit-site -> 上游仓 CLI 输出本仓产物；上游尚无稳定 CLI 时**显式 SKIP**（不在本仓复制渲染逻辑）

默认 dry-run（只打印将要执行的命令）；`--apply` 才真正执行。执行后自动跑一次 sync-check 汇总。

用法：
  python3 scripts/sync-run.py                 # 预览全部
  python3 scripts/sync-run.py --apply         # 执行 local/mirror 两类，emit-site 仍 SKIP
  python3 scripts/sync-run.py --apply --only tokens-board
  python3 scripts/sync-run.py --json          # 机器读
退出码：0 未出现失败 / 1 有失败 / 2 清单不可读 / 3 仅 SKIP（无可执行项）
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "config" / "sync-manifest.json"

# 本仓可执行的入口（mode -> 命令模板）；上游 emit-site 一律 SKIP，等 P4 跨仓交接
LOCAL_ENTRIES = {
    "local": ["python3", "scripts/poetry-titles-gen.py"],
    "mirror": ["python3", "scripts/tokens-tracker-mirror.py"],
}


def load():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return data


def plan(manifest, only=None):
    steps = []
    for art in manifest.get("artifacts", []):
        if only and art["id"] not in only:
            continue
        mode = art.get("producer", {}).get("mode", "?")
        cmd = LOCAL_ENTRIES.get(mode)
        if cmd is None:
            steps.append({"id": art["id"], "mode": mode, "action": "skip",
                          "reason": f"mode={mode} 需上游 CLI（P4 跨仓交接后启用）"})
            continue
        steps.append({"id": art["id"], "mode": mode, "action": "run", "cmd": cmd})
    return steps


def run_step(step):
    proc = subprocess.run(step["cmd"], cwd=ROOT, capture_output=True, text=True)
    out = ((proc.stdout or "") + (proc.stderr or "")).strip()
    return proc.returncode, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="真正执行（默认 dry-run）")
    ap.add_argument("--only", action="append", help="只跑指定 id（可重复）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--skip-check", action="store_true", help="执行后不跑 sync-check")
    args = ap.parse_args()

    try:
        manifest = load()
    except (OSError, json.JSONDecodeError) as exc:
        print(f"manifest unreadable: {exc}", file=sys.stderr)
        return 2

    steps = plan(manifest, args.only)
    results = []
    failures = 0
    for step in steps:
        if step["action"] == "skip":
            results.append({**step, "rc": None})
            continue
        if not args.apply:
            results.append({**step, "rc": None, "preview": " ".join(step["cmd"])})
            continue
        rc, out = run_step(step)
        failures += 1 if rc else 0
        results.append({**step, "rc": rc, "output": out[-400:]})

    check = None
    if args.apply and not args.skip_check:
        proc = subprocess.run(["python3", "scripts/sync-check.py", "--json"], cwd=ROOT,
                              capture_output=True, text=True)
        try:
            check = json.loads(proc.stdout)
        except json.JSONDecodeError:
            check = {"rc": 3, "error": "sync-check json unparsable"}

    if args.json:
        print(json.dumps({"apply": args.apply, "steps": results, "check": check}, ensure_ascii=False, indent=2))
    else:
        for r in results:
            if r["action"] == "skip":
                print(f"SKIP  {r['id']:<14} {r['reason']}")
            elif r.get("preview"):
                print(f"DRY   {r['id']:<14} {r['preview']}")
            else:
                print(f"{'OK  ' if not r['rc'] else 'FAIL'}  {r['id']:<14} rc={r['rc']}  {r.get('output','')[:120]}")
        if check:
            print(f"\nsync-check rc={check.get('rc')} "
                  f"（0 全绿 / 1 过渡·陈旧 / 2 结构违规 / 3 无法判定）")
        if not args.apply:
            print("\n（dry-run：加 --apply 才执行）")

    if failures:
        return 1
    if steps and all(s["action"] == "skip" for s in steps):
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
