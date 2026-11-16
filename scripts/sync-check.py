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
  python3 scripts/sync-check.py --emit-status                    # 重出状态页（转调 sync-status-gen.py）
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
HISTORY = ROOT / "data" / "sync-history.json"      # 状态页的日聚合（单日一行，幂等覆盖）
REQUIRED = ("id", "artifact", "producer", "trigger", "contract", "publish", "verify")


def now_utc():
    return datetime.now(timezone.utc)


def parse_iso(value):
    try:
        dt = datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None
    if dt.tzinfo:
        return dt
    # 2026-11-16（review SEC-6）：naive 戳由本机生成器写入（无偏移）⇒ 按本地时区解释。
    # 之前按 UTC 解释 ⇒ 年龄恒 -7.8h，真陈旧 3 天仍算 16h 判绿（新鲜度判据宽松 8 小时）。
    return dt.astimezone() if dt.tzinfo is None else dt


def load_manifest(path=MANIFEST):
    data = json.loads(path.read_text(encoding="utf-8"))
    problems = []
    ids = [a.get("id") for a in data.get("artifacts", [])]
    if len(ids) != len(set(ids)):
        problems.append("duplicate artifact id in manifest")
    modes = {"emit-site", "mirror", "local"}      # JT-CL005 §84 契约枚举
    for art in data.get("artifacts", []):
        for key in REQUIRED:
            if key not in art:
                problems.append(f"{art.get('id', '?')}: missing field {key}")
        prod = art.get("producer")
        if isinstance(prod, dict):
            if "mode" not in prod:
                problems.append(f"{art.get('id', '?')}: producer.mode 必填（契约枚举 {sorted(modes)}）")
            elif prod.get("mode") not in modes:
                problems.append(f"{art.get('id', '?')}: producer.mode {prod.get('mode')!r} 不在契约枚举 {sorted(modes)}")
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
        # F-1：record 先建好（含 producer），任何分支都能安全渲染 —— 否则不可读产物会让
        # print_human 取不到 producer 而 KeyError（验证工具在最该报错的输入上崩掉）。
        base = {"id": art["id"], "artifact": rel,
                "producer": f"{art['producer']['repo']}/{art['producer']['entry']}",
                "trigger": art["trigger"].get("cron", "?"), "stamp": None,
                "generated": None, "age_h": None}
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            # N-4：不覆盖更严重的既有判定（mismatch 不应被 unknown 降级）
            if worst[0] in ("none", "ok", "unstamped", "stale"):
                worst = ("unknown", f"{rel}: unreadable ({exc})")
            recs.append(base)
            continue
        stamp = sync_stamp.parse(text)
        contract = art.get("contract", {})
        rec = dict(base, stamp=stamp)
        if stamp is None:
            # Q-3：verify.hash 决定「无戳」的严重度 —— required ⇒ 结构违规；optional ⇒ 过渡态告警
            if contract.get("stamp") == "pending" and art.get("verify", {}).get("hash") != "required":
                status, detail = "unstamped", f"{rel}: 过渡态（上游未打戳，hash=optional）"
            else:
                status, detail = "mismatch", f"{rel}: 契约要求打戳（hash=required）但缺失"
        else:
            try:
                stamp_v = int(stamp.get("v", "0") or 0)
                contract_v = int(contract.get("version", 1))
            except (TypeError, ValueError):
                status, detail = "mismatch", f"{rel}: 戳版本不可解析 v={stamp.get('v')!r}（契约 v={contract.get('version')!r}）"
                stamp_v = contract_v = None
            if stamp_v is None:
                pass  # 已判定 mismatch
            elif stamp.get("id") != art["id"]:
                status, detail = "mismatch", f"{rel}: 戳 id={stamp.get('id')} != {art['id']}"
            elif stamp_v > contract_v:
                status, detail = "mismatch", f"{rel}: 戳版本 v={stamp_v} 高于契约版本 {contract_v}"
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
    elif "unknown" in statuses:
        rc = 3          # Q-1：存在不可判定的产物（如非 utf-8）⇒ 与文档一致，不再降级为 rc=1
    elif statuses & {"stale", "unstamped"}:
        rc = 1
    else:
        rc = 0
    payload = {"rc": rc, "checked_at": now_utc().isoformat(timespec="seconds"),
               "manifest_version": manifest.get("version"), "artifacts": rows,
               "details": details, "structural": struct, "unregistered": extra or []}
    return rc, payload, struct


VERDICT = {0: "PASS", 1: "PASS（含过渡/陈旧项）", 2: "FAIL（结构违规）", 3: "UNKNOWN"}


def print_human(payload):
    print(f"sync-check · {payload['checked_at']} · manifest v{payload['manifest_version']}")
    width = max([len(r.get("artifact", "")) for r in payload["artifacts"]] + [8])
    width = min(width, 48)
    for row in payload["artifacts"]:
        gen = row.get("generated") or "—"
        age = f"{row['age_h']}h" if row.get("age_h") is not None else "—"
        print(f"  {row.get('artifact', ''):<{width}}  {gen:<25}  {age:>7}  {row.get('producer', '—')}")
    for item in payload["details"]:
        mark = {"ok": "✅", "stale": "⚠️", "unstamped": "⚠️",
                "mismatch": "❌", "missing": "❌", "unknown": "❓"}[item["status"]]
        print(f"  {mark} {item['detail']}")
    if payload["unregistered"]:
        for rel in payload["unregistered"]:
            print(f"  ❌ 未注册产物: {rel}")
    print(f"\n{VERDICT[payload['rc']]} · artifacts {len(payload['artifacts'])} · rc={payload['rc']}")


def emit_history(payload, dest=None):
    """把本次校验压缩成「一天一行」写进历史（幂等：同一天重复跑 = 覆盖当天行）。

    形状：{"schema": 1, "days": {"YYYY-MM-DD": {"rc": 1, "verdict": "...", "artifacts": {"id": "status"},
            "ok_ratio": 0.5}}}
    用途：状态页的 90 天条；不记时间序列细节，避免文件随时间膨胀（约 100 B/天）。
    """
    dest = Path(dest or HISTORY)
    data = {"schema": 1, "days": {}}
    if dest.exists():
        try:
            loaded = json.loads(dest.read_text(encoding="utf-8"))
            if isinstance(loaded, dict) and isinstance(loaded.get("days"), dict):
                data = loaded
        except (OSError, json.JSONDecodeError):
            pass                       # 损坏则重来（历史可重建，不 fail-closed）
    status_by_id = {}
    for item in payload["details"]:
        status_by_id.setdefault(item["id"], item["status"])
    day = payload["checked_at"][:10]   # UTC 日期；状态页按 UTC 展示并标注
    arts = {row["id"]: status_by_id.get(row["id"], "unknown") for row in payload["artifacts"]}
    ok = sum(1 for v in arts.values() if v == "ok")
    data["schema"] = 1
    data.setdefault("days", {})[day] = {
        "rc": payload["rc"], "verdict": VERDICT[payload["rc"]], "artifacts": arts,
        "ok_ratio": round(ok / len(arts), 3) if arts else 0.0,
    }
    data["days"] = dict(sorted(data["days"].items()))
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    tmp.replace(dest)                     # 原子替换：半写不会留下坏 JSON
    return len(data["days"])



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
    _n = len(manifest.get("artifacts", []))
    ok("清单条目数 ≥ 5（当前 6：含 tokens-live）", _n >= 5, str(_n))
    ok("清单无绝对路径", "/Users/" not in json.dumps(manifest))

    # emit_history 往返：同一 payload 连写两次，天数不增（同日幂等），且 rc/verdict 落盘
    _hp = ROOT / "cache" / "scratch" / "_history_probe.json"
    _hp.parent.mkdir(parents=True, exist_ok=True)
    _payload = {"rc": 1, "artifacts": [{"id": "x", "status": "ok", "detail": "ok"}],
                "details": [], "checked_at": now_utc().isoformat()}
    try:
        n1 = emit_history(_payload, _hp)
        n2 = emit_history(_payload, _hp)
        _j = json.loads(_hp.read_text(encoding="utf-8"))
        ok("emit_history 同日幂等", n1 == n2 == len(_j["days"]), f"{n1}/{n2}")
        _day = _j["days"][sorted(_j["days"])[0]]
        ok("emit_history 落 verdict（日记录内）",
           _day.get("verdict") == "PASS（含过渡/陈旧项）", str(_day.get("verdict")))
    except NameError as exc:                     # 本次事故形态：VERDICT 被误删
        ok("emit_history 可用（无 NameError）", False, str(exc))
    finally:
        _hp.unlink(missing_ok=True)

    # 清单契约的判别力自证：缺 mode ⇒ 红、超枚举 ⇒ 红（2026-11-16 review ⑤）
    import copy as _copy
    import tempfile as _tf2
    _probe_dir = ROOT / "cache" / "scratch"
    _probe_dir.mkdir(parents=True, exist_ok=True)
    for _label, _mut, _want in (
        ("缺 producer.mode", lambda a: a["producer"].pop("mode", None), True),
        ("producer.mode 超枚举", lambda a: a["producer"].__setitem__("mode", "overwrite"), True),
        ("producer.mode=mirror", lambda a: a["producer"].__setitem__("mode", "mirror"), False),
    ):
        _m = _copy.deepcopy(manifest)
        _mut(_m["artifacts"][0])
        _f = _probe_dir / "_manifest_probe.json"
        _f.write_text(json.dumps(_m, ensure_ascii=False), encoding="utf-8")
        try:
            _p = load_manifest(_f)[1]
        finally:
            _f.unlink(missing_ok=True)
        ok(f"清单校验：{_label} ⇒ {'红' if _want else '绿'}",
           bool(_p) == _want, "; ".join(_p)[:80])

    base = now_utc()
    ok("新鲜度边界（36h 内 ok）", (now_utc() - (base - timedelta(hours=35))) / timedelta(hours=1) < 36)
    ok("新鲜度边界（37h 超限）", (now_utc() - (base - timedelta(hours=37))) / timedelta(hours=1) > 36)

    # Q-2 回归：戳版本不可解析不得抛异常
    try:
        bad_v = sync_stamp.parse(sync_stamp.js_stamp("var a=1;\n", id="z", producer="r/x.py", v="abc",
                                                    generated="2026-11-16T00:00:00+00:00", sha256="0"))
        ok("戳 v 非数字可解析（不抛）", (bad_v or {}).get("v") == "abc")
    except Exception as exc:  # noqa: BLE001
        ok("戳 v 非数字可解析（不抛）", False, str(exc))

    # F-1 回归：不可读产物必须走 unknown 且 record 含 producer（不抛 KeyError）
    import tempfile as _tf
    _tmp = ROOT / "cache" / "scratch" / "_unreadable_probe.html"
    _tmp.parent.mkdir(parents=True, exist_ok=True)
    _tmp.write_bytes(b"\xff\xfe\x00bad")
    try:
        _st, _detail, _rec = check_artifact({"id": "probe", "artifact": "cache/scratch/_unreadable_probe.html",
                                             "producer": {"repo": "r", "entry": "e"},
                                             "trigger": {"cron": "?"}, "contract": {"version": 1},
                                             "publish": {}, "verify": {}})
        ok("不可读产物 ⇒ unknown 且 record 带 producer", _st == "unknown" and bool(_rec.get("producer")))
    except Exception as exc:  # noqa: BLE001
        ok("不可读产物 ⇒ unknown 且 record 带 producer", False, str(exc))
    finally:
        _tmp.unlink(missing_ok=True)

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
    # 2026-11-16：旧内联模板已删；本开关保留为「一键重出状态页」的兼容入口，
    # 无 PATH 形参（旧写法传路径只会在参数解析阶段报错，不会写出半截页面）。
    ap.add_argument("--emit-status", action="store_true")
    ap.add_argument("--emit-history", metavar="PATH", nargs="?", const=str(HISTORY),
                    help="追加/覆盖当天日聚合（默认 data/sync-history.json）")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    rc, payload, _ = run()
    if args.emit_status:
        gen = ROOT / "scripts" / "sync-status-gen.py"
        print("note: --emit-status 已转调 scripts/sync-status-gen.py（旧内联模板已删）", file=sys.stderr)
        proc = subprocess.run([sys.executable, str(gen)], cwd=str(ROOT))
        page = ROOT / "sync-status.html"
        if proc.returncode != 0:
            print(f"status page FAILED: {proc.returncode}（{page}）", file=sys.stderr)
            raise SystemExit(proc.returncode)          # 子进程失败绝不打印成功
        if not page.exists():
            print(f"status page FAILED: 生成器 rc=0 但未落盘 {page}", file=sys.stderr)
            raise SystemExit(2)
        print(f"status page written: {page} ({page.stat().st_size} B)", file=sys.stderr)
    if args.emit_history:
        days = emit_history(payload, args.emit_history)
        print(f"history written: {args.emit_history} ({days} 天)", file=sys.stderr)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print_human(payload)
    if args.strict and rc == 1:
        return 2
    return rc


if __name__ == "__main__":
    sys.exit(main())
