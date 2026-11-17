#!/usr/bin/env python3
"""site_chrome —— 给上游直写的单页产物补站点 chrome，并把 SYNC 戳重打在本仓名下。

背景
----
`bmi-tracker.html` 由 daily-tracker 的 deploy 直写（本仓不能手改：下一次写盘会整页覆盖）。
但站点一致性要求它和 `/tokens-tracker/` 一样有：
  · 右上角 GitHub 外链（corner）
  · 右侧垂直居中的「返回首页」悬浮按钮
于是把 chrome 放在**上游写盘之后**的加工步骤里，本脚本负责注入并重打戳。

戳怎么处理（关键，别改成「不重打」）
--------------------------------
注入会改变正文 ⇒ 上游戳里的 sha256 必然对不上（sync-check 判 mismatch / rc=2）。
所以注入后要重打戳：
  · `id`      沿用上游的（必须等于 manifest.artifact.id，校验器会比对）
  · `generated` 沿用上游的（新鲜度语义不变：仍是「数据最后变化时刻」）
  · `producer` 改成我方加工器（谁产出最终字节，就由谁签）
  · `sha256`  按注入后的正文重算
因此 `sync-check` 的三条判据（id 对齐 / 哈希自证 / 新鲜度）继续成立。

幂等
----
标记块按 `<!-- jt-chrome:start --> … <!-- jt-chrome:end -->` 包裹；重跑时先替换，
不重复堆叠 ⇒ 同输入逐字节同输出（可安全放进每日链路）。

用法
----
  python3 scripts/site_chrome.py --check     # 只报是否需要注入（rc=0 已最新 / 1 需要注入）
  python3 scripts/site_chrome.py --write     # 注入 + 重打戳（不碰 git）
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SITE / "scripts"))
import sync_stamp  # noqa: E402

PRODUCER = "www.jaden.tech/scripts/site_chrome.py"
TARGETS = [("bmi-tracker.html", "./")]     # 产物 → 首页相对路径（根级页面用 ./）
CHROME_START = "<!-- jt-chrome:start -->"
CHROME_END = "<!-- jt-chrome:end -->"

CHROME_CSS = """<style id="jt-chrome-css">
/* 站点 chrome（由 scripts/site_chrome.py 注入，勿手改；上游写盘后重跑本脚本即可恢复） */
.jt-gh { position: fixed; top: 0; right: 0; z-index: 999; width: 64px; height: 64px; }
.jt-gh svg { position: absolute; top: 0; right: 0; border: 0; fill: #e6edf3; color: #0d1117; }
.jt-gh:hover svg { filter: drop-shadow(0 0 8px rgba(96,165,250,.55)); }
.jt-gh .octo-arm { transform-origin: 130px 106px; }
.jt-gh:hover .octo-arm { animation: jt-octo 560ms ease-in-out; }
@keyframes jt-octo { 0%,100%{transform:rotate(0)} 20%,60%{transform:rotate(-25deg)} 40%,80%{transform:rotate(10deg)} }
.jt-home { position: fixed; right: 18px; top: 50%; transform: translateY(-50%); z-index: 999;
  width: 44px; height: 44px; display: flex; align-items: center; justify-content: center;
  border-radius: 12px; color: #e6edf3; text-decoration: none;
  background: rgba(8,12,20,.55); border: 1px solid rgba(255,255,255,.22);
  box-shadow: 0 6px 18px rgba(0,0,0,.28);
  backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
  transition: background .18s ease, border-color .18s ease, transform .18s ease; }
.jt-home:hover { background: rgba(12,18,30,.72); border-color: rgba(255,255,255,.45);
  transform: translateY(-50%) scale(1.05); }
.jt-home:focus-visible { outline: 2px solid #9ecbff; outline-offset: 2px; }
@media (max-width: 600px) {
  .jt-gh { width: 52px; height: 52px; }
  .jt-gh svg { width: 52px; height: 52px; }
  .jt-home { right: 10px; width: 40px; height: 40px; border-radius: 10px; }
}
@media (prefers-reduced-motion: reduce) { .jt-home { transition: none; } .jt-gh:hover .octo-arm { animation: none; } }
</style>"""

CHROME_HTML = """{start}
<a href="https://github.com/imjaden" class="jt-gh" target="_blank" rel="noopener" aria-label="在 GitHub 查看源码 ｜ View source on GitHub" title="在 GitHub 查看源码 ｜ View source on GitHub">
<svg width="64" height="64" viewBox="0 0 250 250" aria-hidden="true" focusable="false"><path d="M0,0 L115,115 L130,115 L142,142 L250,250 L250,0 Z" fill="rgba(0,0,0,0.35)"/><path d="M128.3,109.0 C113.8,99.7 119.0,89.6 119.0,89.6 C122.0,82.7 120.5,78.6 120.5,78.6 C119.2,72.0 123.4,76.3 123.4,76.3 C127.3,80.9 125.5,87.3 125.5,87.3 C122.9,97.6 130.6,101.9 134.4,103.2" fill="currentColor" class="octo-arm"/><path d="M115.0,115.0 C114.9,115.1 118.7,116.5 119.8,115.4 L133.7,101.6 C136.9,99.2 139.9,98.4 142.2,98.6 C133.8,88.0 127.5,74.4 143.8,58.0 C148.5,53.4 154.0,51.2 159.7,51.0 C160.3,49.4 163.2,43.6 171.4,40.1 C171.4,40.1 176.1,42.5 178.8,56.2 C183.1,58.6 187.2,61.8 190.9,65.4 C194.5,69.0 197.7,73.2 200.1,77.6 C213.8,80.2 216.3,84.9 216.3,84.9 C212.7,93.1 206.9,96.0 205.4,96.6 C205.1,102.4 203.0,107.8 198.3,112.5 C181.9,128.9 168.3,122.5 157.7,114.1 C157.9,116.9 156.7,120.9 152.7,124.9 L141.0,136.5 C139.8,137.7 141.6,141.9 141.8,141.8 Z" fill="currentColor" class="octo-body"/></svg>
</a>
<a href="{home}" class="jt-home" aria-label="返回首页 ｜ Back to home" title="返回首页 ｜ Back to home">
<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" focusable="false"><path d="M12 3.2 2.8 11h2.5v9.2h5.1v-6h3.2v6h5.1V11h2.5z" fill="currentColor"/></svg>
</a>
{end}"""


def _strip_chrome(html: str) -> str:
    """去掉上一次注入的块（含 CSS），保证幂等。"""
    html = re.sub(re.escape(CHROME_START) + r".*?" + re.escape(CHROME_END) + r"\n?", "", html, flags=re.S)
    return re.sub(r'<style id="jt-chrome-css">.*?</style>\n?', "", html, flags=re.S)


def inject(html: str, home: str) -> str:
    """注入 chrome（先清旧块 ⇒ 幂等），CSS 进 </head> 前，标记块进 </body> 前。"""
    body = _strip_chrome(html)
    if "</head>" not in body:
        raise RuntimeError("no </head> — cannot inject chrome (fail-closed)")
    body = body.replace("</head>", CHROME_CSS + "\n</head>", 1)
    block = CHROME_HTML.format(start=CHROME_START, home=home, end=CHROME_END)
    if "</body>" in body:
        return body.replace("</body>", block + "\n</body>", 1)
    return body + "\n" + block + "\n"


def restamp(html: str) -> str:
    """保留上游 id / generated，producer 换成我方加工器，哈希按注入后正文重算。"""
    stamp = sync_stamp.parse(html)
    if not stamp:
        raise RuntimeError("no SYNC stamp — cannot restamp (fail-closed)")
    body = sync_stamp.strip_stamp(html)
    return sync_stamp.html_stamp(body, id=stamp["id"], producer=PRODUCER,
                                 v=stamp.get("v") or "1",
                                 generated=stamp.get("generated") or "",
                                 sha256=sync_stamp.digest(body))


def process(path: Path, home: str) -> tuple[bool, str]:
    """返回 (是否改动, 说明)。"""
    html = path.read_text(encoding="utf-8")
    new = restamp(inject(html, home))
    if new == html:
        return False, f"{path.name}: 已是目标形态"
    path.write_text(new, encoding="utf-8")
    return True, f"{path.name}: chrome 已更新并重打戳"


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--write", action="store_true")
    g.add_argument("--check", action="store_true")
    a = ap.parse_args()
    changed = 0
    for name, home in TARGETS:
        p = SITE / name
        if not p.exists():
            print(f"❌ {name} 不存在", file=sys.stderr)
            return 2
        html = p.read_text(encoding="utf-8")
        want = restamp(inject(html, home))
        if want != html:
            changed += 1
            if a.write:
                p.write_text(want, encoding="utf-8")
            print(("✅ " if a.write else "⚠️ ") + f"{name}: "
                  + ("chrome 已更新并重打戳" if a.write else "需要注入 chrome"))
        else:
            print(f"·  {name}: 已是目标形态")
    if a.check:
        return 1 if changed else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
