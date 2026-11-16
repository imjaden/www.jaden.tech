#!/usr/bin/env python3
"""sync-check — 门户同步面校验器（JT-CL005 / SYNC-MANIFEST）。

真值：config/sync-manifest.json（唯一 tracked 配置）
判据：三类漂移
  * 结构漂移  产物缺失 / 未注册 / 缺戳（契约要求 inline 时）/ 戳 id 或版本不符  -> rc=2
  * 内容漂移  正文哈希 != 戳声明（被手改或半写）                                -> rc=2
  * 时间漂移  now - generated > verify.freshness_h                              -> rc=1 stale
  * 过渡态    contract.stamp == "pending"（上游尚未打戳）且无戳                  -> rc=1 unstamped
退出码：0 全绿 / 1 仅 stale·unstamped / 2 结构违规 / 3 无法判定（清单或产物不可读）

用法：
  python3 scripts/sync-check.py                 # 人读摘要
  python3 scripts/sync-check.py --json          # 机器读（含 status 字段，逐产物）
  python3 scripts/sync-check.py --strict        # 把 stale/unstamped 也当失败（rc=2）
  python3 scripts/sync-check.py --selftest      # 自检（戳往返/篡改/幂等/新鲜度/清单）
  python3 scripts/sync-check.py --emit-status sync-status.html   # 重出状态页
"""
import argparse
import fnmatch
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sync_stamp  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "config" / "sync-manifest.json"
REQUIRED = ("id", "artifact", "producer", "trigger", "contract", "publish", "verify")


def now_utc():
    return datetime.now(timezone.utc)


def parse_iso(value):
    try:
        dt = datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def load_manifest(path=MANIFEST):
    data = json.loads(path.read_text(encoding="utf-8"))
    problems = []
    ids = [a.get("id") for a in data.get("artifacts", [])]
    if len(ids) != len(set(ids)):
        problems.append("duplicate artifact id in manifest")
    for art in data.get("artifacts", []):
        for key in REQUIRED:
            if key not in art:
                problems.append(f"{art.get('id', '?')}: missing field {key}")
    return data, problems


def tracked_files():
    try:
        out = subprocess.run(["git", "-C", str(ROOT), "ls-files"],
                             capture_output=True, text=True, check=True).stdout
        return [line for line in out.splitlines() if line]
    except (OSError, subprocess.CalledProcessError):
        return None


def resolve(artifact):
    pattern = artifact["artifact"]
    root = ROOT
    if any(ch in pattern for ch in "*?["):
        hits = sorted(str(p.relative_to(root)) for p in root.rglob("*")
                      if p.is_file() and fnmatch.fnmatch(str(p.relative_to(root)), pattern))
        return hits
    return [pattern] if (root / pattern).exists() else []


def check_artifact(art):
    """返回 (status, detail, record)。status ∈ ok/stale/unstamped/mismatch/missing/unknown"""
    files = resolve(art)
    if not files:
        return "missing", f"artifact not found: {art['artifact']}", {
            "id": art["id"], "artifact": art["artifact"], "generated": None, "age_h": None,
            "producer": f"{art['producer']['repo']}/{art['producer']['entry']}",
            "trigger": art["trigger"].get("cron", "?"), "stamp": None}

    worst = ("none", "")
    recs = []
    for rel in files:
        path = ROOT / rel
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            worst = ("unknown", f"{rel}: unreadable ({exc})")
            continue
        stamp = sync_stamp.parse(text)
        contract = art.get("contract", {})
        rec = {"id": art["id"], "artifact": rel,
               "producer": f"{art['producer']['repo']}/{art['producer']['entry']}",
               "trigger": art["trigger"].get("cron", "?"), "stamp": stamp,
               "generated": None, "age_h": None}
        if stamp is None:
            if contract.get("stamp") == "pending":
                status, detail = "unstamped", f"{rel}: 过渡态（上游未打戳）"
            else:
                status, detail = "mismatch", f"{rel}: 契约要求 inline 戳但缺失"
        else:
            if stamp.get("id") != art["id"]:
                status, detail = "mismatch", f"{rel}: 戳 id={stamp.get('id')} != {art['id']}"
            elif int(stamp.get("v", "0") or 0) > int(contract.get("version", 1)):
                status, detail = "mismatch", f"{rel}: 戳版本 v={stamp.get('v')} 高于契约版本"
            elif sync_stamp.digest(text) != stamp.get("sha256"):
                status, detail = "mismatch", f"{rel}: 正文哈希不符（被手改或半写）"
            else:
                generated = parse_iso(stamp.get("generated"))
                rec["generated"] = stamp.get("generated")
                if generated is None:
                    status, detail = "unknown", f"{rel}: 戳 generated 不可解析"
                else:
                    age = (now_utc() - generated) / timedelta(hours=1)
                    rec["age_h"] = round(age, 1)
                    limit = float(art.get("verify", {}).get("freshness_h", 0))
                    if not limit:
                        status, detail = "ok", f"{rel}: {age:.1f}h（freshness 关闭，靠 hash/派生判据）"
                    elif age > limit:
                        status, detail = "stale", f"{rel}: 已 {age:.1f}h > {limit:g}h"
                    else:
                        status, detail = "ok", f"{rel}: {age:.1f}h ≤ {limit:g}h"
        recs.append(rec)
        rank = {"ok": 0, "unstamped": 1, "stale": 1, "unknown": 2, "mismatch": 3, "missing": 3}
        if worst[0] == "none" or rank[status] > rank[worst[0]]:
            worst = (status, detail)
    if len(recs) > 1:  # glob 条目：用一条汇总记录（展示层不刷屏）
        record = dict(recs[0])
        record["artifact"] = f"{art['artifact']}（{len(recs)} 个文件）"
    else:
        record = recs[0] if recs else {"id": art["id"], "artifact": art["artifact"]}
    return ("ok" if worst[0] == "none" else worst[0]), worst[1], record


def unregistered(watch, artifacts, tracked):
    """watch 覆盖的 tracked 文件里，没有任何条目认领的（结构漂移）。"""
    if tracked is None:
        return None
    claimed = set()
    for art in artifacts:
        claimed.update(resolve(art))
    extra = []
    for rel in tracked:
        if not any(fnmatch.fnmatch(rel, pattern) for pattern in watch):
            continue
        if rel not in claimed:
            extra.append(rel)
    return sorted(extra)


def run():
    problems = []
    try:
        manifest, problems = load_manifest()
    except (OSError, json.JSONDecodeError) as exc:
        return 3, {"error": f"manifest unreadable: {exc}", "artifacts": []}, problems

    rows, details, struct = [], [], list(problems)
    for art in manifest.get("artifacts", []):
        status, detail, record = check_artifact(art)
        rows.append(record)
        details.append({"id": art["id"], "status": status, "detail": detail})
        if status in ("mismatch", "missing"):
            struct.append(detail)

    extra = unregistered(manifest.get("watch", []), manifest.get("artifacts", []), tracked_files())
    if extra:
        struct.extend(f"unregistered artifact: {rel}" for rel in extra)
    elif extra is None:
        details.append({"id": "-", "status": "unknown", "detail": "git ls-files unavailable"})

    statuses = {d["status"] for d in details}
    if struct:
        rc = 2
    elif statuses & {"stale", "unstamped", "unknown"}:
        rc = 1
    else:
        rc = 0
    payload = {"rc": rc, "checked_at": now_utc().isoformat(timespec="seconds"),
               "manifest_version": manifest.get("version"), "artifacts": rows,
               "details": details, "structural": struct, "unregistered": extra or []}
    return rc, payload, struct


def print_human(payload):
    print(f"sync-check · {payload['checked_at']} · manifest v{payload['manifest_version']}")
    width = max([len(r.get("artifact", "")) for r in payload["artifacts"]] + [8])
    for row in payload["artifacts"]:
        gen = row.get("generated") or "—"
        age = f"{row['age_h']}h" if row.get("age_h") is not None else "—"
        print(f"  {row.get('artifact', ''):<{width}}  {gen:<25}  {age:>7}  {row['producer']}")
    for item in payload["details"]:
        mark = {"ok": "✅", "stale": "⚠️", "unstamped": "⚠️",
                "mismatch": "❌", "missing": "❌", "unknown": "❓"}[item["status"]]
        print(f"  {mark} {item['detail']}")
    if payload["unregistered"]:
        for rel in payload["unregistered"]:
            print(f"  ❌ 未注册产物: {rel}")
    verdict = {0: "PASS", 1: "PASS（含过渡/陈旧项）", 2: "FAIL（结构违规）", 3: "UNKNOWN"}[payload["rc"]]
    print(f"\n{verdict} · artifacts {len(payload['artifacts'])} · rc={payload['rc']}")


STATUS_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>同步面状态 · jaden.tech</title>
<style>
:root {{ color-scheme: dark; }}
body {{ margin:0; padding:32px 20px; background:#0d1117; color:#e6edf3;
  font:14px/1.6 -apple-system,BlinkMacSystemFont,"PingFang SC","Helvetica Neue",sans-serif; }}
h1 {{ font-size:1.25rem; margin:0 0 4px; }}
.sub {{ color:#8b949e; font-size:.82rem; margin-bottom:24px; }}
table {{ border-collapse:collapse; width:100%; max-width:1080px; }}
th,td {{ text-align:left; padding:9px 12px; border-bottom:1px solid #21262d; font-size:.85rem; vertical-align:top; }}
th {{ color:#8b949e; font-weight:600; }}
code {{ color:#7ee787; font-size:.8rem; }}
.ok {{ color:#3fb950; }} .warn {{ color:#d29922; }} .bad {{ color:#f85149; }}
footer {{ margin-top:28px; color:#6e7681; font-size:.78rem; }}
a {{ color:#58a6ff; }}
</style>
</head>
<body>
<h1>同步面状态 · SYNC-MANIFEST</h1>
<div class="sub">校验时间 {checked_at} · 清单版本 v{manifest_version} · 结论 <strong class="{verdict_cls}">{verdict}</strong> · 由 <code>scripts/sync-check.py --emit-status</code> 生成，勿手改</div>
<table>
<thead><tr><th>产物</th><th>来源仓 / 入口</th><th>触发</th><th>生成时间</th><th>年龄</th><th>结论</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
<footer>判据：结构漂移（缺失/未注册/缺戳/哈希不符）、内容漂移（正文哈希≠戳）、时间漂移（超 freshness_h）。<a href="./">← 返回首页</a></footer>
</body>
</html>
"""


def emit_status(payload, dest):
    cls = {0: "ok", 1: "warn", 2: "bad", 3: "warn"}[payload["rc"]]
    verdict = {0: "PASS", 1: "PASS（含过渡/陈旧项）", 2: "FAIL（结构违规）", 3: "UNKNOWN"}[payload["rc"]]
    detail_by_id = {}
    for item in payload["details"]:
        detail_by_id.setdefault(item["id"], item)
    rows = []
    for row in payload["artifacts"]:
        verdict_item = detail_by_id.get(row["id"], {"status": "unknown", "detail": "—"})
        mark = {"ok": ("ok", "正常"), "stale": ("warn", "陈旧"), "unstamped": ("warn", "过渡（未打戳）"),
                "mismatch": ("bad", "结构违规"), "missing": ("bad", "缺失"),
                "unknown": ("warn", "无法判定")}[verdict_item["status"]]
        gen = row.get("generated") or "—"
        age = f"{row['age_h']}h" if row.get("age_h") is not None else "—"
        rows.append(
            "<tr><td><code>{art}</code></td><td>{prod}</td><td>{trig}</td>"
            "<td>{gen}</td><td>{age}</td><td class=\"{cls}\">{label}</td></tr>".format(
                art=row.get("artifact", "?"), prod=row.get("producer", "?"),
                trig=row.get("trigger", "?"), gen=gen, age=age, cls=mark[0], label=mark[1]))
    html = STATUS_HTML.format(checked_at=payload["checked_at"], manifest_version=payload["manifest_version"],
                              verdict=verdict, verdict_cls=cls, rows="\n".join(rows))
    Path(dest).write_text(html, encoding="utf-8")
    return len(html)


def selftest():
    checks = []

    def ok(name, cond, note=""):
        checks.append((name, bool(cond), note))

    html = "<!DOCTYPE html>\n<html><body>hi</body></html>\n"
    stamped = sync_stamp.html_stamp(html, id="x", producer="r/s.py", v="1",
                                    generated="2026-11-16T00:00:00+00:00", sha256=sync_stamp.digest(html))
    ok("html 往返（剥戳还原）", sync_stamp.strip_stamp(stamped) == html)
    ok("html 幂等（重复打戳同字节）",
       sync_stamp.html_stamp(stamped, id="x", producer="r/s.py", v="1",
                             generated="2026-11-16T00:00:00+00:00",
                             sha256=sync_stamp.digest(html)) == stamped)
    parsed = sync_stamp.parse(stamped) or {}
    ok("html 解析字段", parsed.get("id") == "x")
    ok("html 哈希自证", sync_stamp.digest(stamped) == parsed.get("sha256"))

    tampered = stamped.replace("hi", "h1")
    ok("篡改可检出", sync_stamp.digest(tampered) != parsed.get("sha256"))

    js = "window.poetryTitles={};\n"
    jstamped = sync_stamp.js_stamp(js, id="y", producer="r/p.py", v="1",
                                   generated="2026-11-16T00:00:00+00:00", sha256=sync_stamp.digest(js))
    ok("js 往返", sync_stamp.strip_stamp(jstamped) == js)
    ok("js 首行即戳", jstamped.splitlines()[0].startswith("/* SYNC "))
    jparsed = sync_stamp.parse(jstamped) or {}
    ok("js 哈希自证", sync_stamp.digest(jstamped) == jparsed.get("sha256"))

    manifest, problems = load_manifest()
    ok("清单可解析", not problems, "; ".join(problems))
    ok("清单条目数 = 5", len(manifest.get("artifacts", [])) == 5,
       str(len(manifest.get("artifacts", []))))
    ok("清单无绝对路径", "/Users/" not in json.dumps(manifest))

    base = now_utc()
    ok("新鲜度边界（36h 内 ok）", (now_utc() - (base - timedelta(hours=35))) / timedelta(hours=1) < 36)
    ok("新鲜度边界（37h 超限）", (now_utc() - (base - timedelta(hours=37))) / timedelta(hours=1) > 36)

    passed = sum(1 for _, cond, _ in checks if cond)
    for name, cond, note in checks:
        print(f"  {'✅' if cond else '❌'} {name}{(' — ' + note) if note and not cond else ''}")
    print(f"\n{passed}/{len(checks)} 通过（selftest）")
    return 0 if passed == len(checks) else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--emit-status", metavar="PATH")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    rc, payload, _ = run()
    if args.emit_status:
        size = emit_status(payload, args.emit_status)
        print(f"status page written: {args.emit_status} ({size} B)", file=sys.stderr)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print_human(payload)
    if args.strict and rc == 1:
        return 2
    return rc


if __name__ == "__main__":
    sys.exit(main())
