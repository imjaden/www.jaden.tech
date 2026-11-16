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
  python3 scripts/sync-run.py --apply --include-upstream   # 含 emit-site 上游腿（上游会自行 commit/push）
  python3 scripts/sync-run.py --json          # 机器读

注意：不带 --include-upstream 时，mode=emit-site 的产物一律 SKIP（--only <emit-site id> 亦为 SKIP/rc=3）。
退出码：0 未出现失败 / 1 有失败 / 2 清单不可读 / 3 仅 SKIP（无可执行项）
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "config" / "sync-manifest.json"

# 本仓可执行的入口（mode -> 命令模板）
LOCAL_ENTRIES = {
    "local": ["python3", "scripts/poetry-titles-gen.py"],
    "mirror": ["python3", "scripts/tokens-tracker-mirror.py"],
}

# 跨仓路径解析：**不得**写进 config/sync-manifest.json（那是公开面）。
# 覆写文件 cache/sync-paths.json（gitignored）形如 {"daily-tracker": "/abs/path"}；
# 缺省按 ~/CodeSpace/<repo> 解析，repo 为本仓时用仓库根。
PATHS_FILE = ROOT / "cache" / "sync-paths.json"


def repo_path(repo):
    if repo in ("www.jaden.tech", "jaden-tech"):
        return ROOT
    try:
        overrides = json.loads(PATHS_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        overrides = {}
    if repo in overrides:
        return Path(overrides[repo]).expanduser()
    return Path.home() / "CodeSpace" / repo


def resolve_cmd(art):
    """优先用清单里的 producer.cmd（跨仓 emit-site）；否则按 mode 用本仓内置入口。"""
    producer = art.get("producer", {})
    cmd = producer.get("cmd")
    if cmd:
        return [str(ROOT) if tok == "{site}" else tok for tok in cmd]
    return LOCAL_ENTRIES.get(producer.get("mode"))


def load():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return data


def plan(manifest, only=None, include_upstream=False):
    steps = []
    for art in manifest.get("artifacts", []):
        if only and art["id"] not in only:
            continue
        producer = art.get("producer", {})
        mode = producer.get("mode", "?")
        # N-2：emit-site 会驱动上游仓的完整流水线（其内部自行 commit/push，本站关不掉），
        # 因此默认不跑；要跑必须显式 --include-upstream，且知道副作用。
        if mode == "emit-site" and not include_upstream:
            steps.append({"id": art["id"], "mode": mode, "action": "skip",
                          "reason": "emit-site 默认不跑（上游会自行 commit/push）；加 --include-upstream 才执行"})
            continue
        cmd = resolve_cmd(art)
        if cmd is None:
            steps.append({"id": art["id"], "mode": mode, "action": "skip",
                          "reason": f"mode={mode} 无可用入口"})
            continue
        cwd = repo_path(producer.get("run_in") or producer.get("repo", ""))
        if not cwd.exists():
            steps.append({"id": art["id"], "mode": mode, "action": "skip",
                          "reason": f"producer repo 不存在: {producer.get('repo')}（可用 cache/sync-paths.json 覆写）"})
            continue
        steps.append({"id": art["id"], "mode": mode, "action": "run", "cmd": cmd,
                      "cwd": str(cwd), "repo": producer.get("repo")})
    return steps


def run_step(step):
    proc = subprocess.run(step["cmd"], cwd=step.get("cwd") or ROOT, capture_output=True, text=True)
    out = ((proc.stdout or "") + (proc.stderr or "")).strip()
    return proc.returncode, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="真正执行（默认 dry-run）")
    ap.add_argument("--only", action="append", help="只跑指定 id（可重复）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--skip-check", action="store_true", help="执行后不跑 sync-check")
    ap.add_argument("--include-upstream", action="store_true",
                    help="同时跑 emit-site 上游腿（会上游仓自行 commit/push，副作用自负）")
    args = ap.parse_args()

    try:
        manifest = load()
    except (OSError, json.JSONDecodeError) as exc:
        print(f"manifest unreadable: {exc}", file=sys.stderr)
        return 2

    steps = plan(manifest, args.only, args.include_upstream)
    # 同一 (cwd, cmd) 只执行一次：多个产物可能来自同一次生成（如 tokens-board + tokens-live 同属 mirror）
    seen, deduped = set(), []
    for step in steps:
        key = (step.get("cwd"), tuple(step["cmd"])) if step["action"] == "run" else (step["id"],)
        if key in seen:
            deduped.append({**step, "action": "dup", "reason": "与上一条共用同一入口，已合并执行"})
            continue
        seen.add(key)
        deduped.append(step)
    steps = deduped
    results = []
    failures = 0
    for step in steps:
        if step["action"] in ("skip", "dup"):
            results.append({**step, "rc": None, "action": step["action"]})
            continue
        if not args.apply:
            results.append({**step, "rc": None,
                            "preview": f"[{step.get('repo')}] " + " ".join(step["cmd"])})
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
            if r["action"] in ("skip", "dup"):
                print(f"{'SKIP' if r['action']=='skip' else 'DUP '}  {r['id']:<14} {r['reason']}")
            elif r.get("preview"):
                print(f"DRY   {r['id']:<14} {r['preview']}")
            else:
                print(f"{'OK  ' if not r['rc'] else 'FAIL'}  {r['id']:<14} rc={r['rc']}  {r.get('output','')[:120]}")
        if check:
            print(f"\nsync-check rc={check.get('rc')} "
                  f"（0 全绿 / 1 过渡·陈旧 / 2 结构违规 / 3 无法判定）")
        if not args.apply:
            print("\n（dry-run：加 --apply 才执行）")

    if isinstance(check, dict) and check.get("rc", 0) >= 2:
        failures += 1           # F-3：结构违规也要非零退出（否则「跑了但红了」被当成功）
    if failures:
        return 1
    if steps and all(s["action"] == "skip" for s in steps):
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
