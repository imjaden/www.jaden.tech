#!/usr/bin/env python3
"""chrome_assets —— 站点双页共用的悬浮按钮资产（单一真源）。

背景（2026-11-20）
------------------
`.jt-home`「返回首页」原本在两处各写一份：
  · `scripts/site_chrome.py`      —— 给上游直写的 bmi-tracker / archive 事后注入
  · `scripts/tokens-tracker-mirror.py` —— 给镜像页生成时内建
两份 HTML 相同，CSS 只差一个 `color`（`#e6edf3` / `#fff`）⇒ 改一处忘一处，
用户看到的就是「两个页面的按钮不太一样」。这里合并成唯一真源，两边都从这里取。

用法
----
    import chrome_assets
    chrome_assets.home_html("./")    # 根级页面
    chrome_assets.home_html("../")   # 一级目录页面（如 /tokens-tracker/）
    chrome_assets.HOME_CSS           # 样式（拼进各自的 <style> 块）

约定
----
· 链接一律相对路径：根级 `./`、一级目录 `../`（root-absolute 违 JT-SEC-018）。
· 尺寸 40×40 / right:10px / 垂直居中：754 档实测 44px 会压住卡片右上角徽章（已回退 40px）。
· `box-sizing: border-box` 必写：tokens 页上游是 content-box，不写会渲染成 42×42（实测差 2px）
· 颜色统一 `#fff`（深底上更稳；原 bmi 用 #e6edf3 属历史差异，合并后以本文件为准）。
"""
from __future__ import annotations

HOME_HTML = (
    '<a href="{home}" class="jt-home" aria-label="返回首页 ｜ Back to home" '
    'title="返回首页 ｜ Back to home">'
    '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" focusable="false">'
    '<path d="M12 3.2 2.8 11h2.5v9.2h5.1v-6h3.2v6h5.1V11h2.5z" fill="currentColor"/>'
    "</svg></a>"
)

HOME_CSS = """/* 右侧垂直居中的「返回首页」悬浮按钮（chrome_assets，双页共用同一份） */
.jt-home {
  position: fixed; right: 10px; top: 50%; transform: translateY(-50%); z-index: 999;
  width: 40px; height: 40px; box-sizing: border-box; display: flex; align-items: center; justify-content: center;
  border-radius: 12px; color: #fff; text-decoration: none;
  background: rgba(8, 12, 20, .55); border: 1px solid rgba(255, 255, 255, .22);
  box-shadow: 0 6px 18px rgba(0, 0, 0, .28);
  backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
  transition: background .18s ease, border-color .18s ease, transform .18s ease;
}
.jt-home:hover { background: rgba(12, 18, 30, .72); border-color: rgba(255, 255, 255, .45);
  transform: translateY(-50%) scale(1.05); }
.jt-home:focus-visible { outline: 2px solid #9ecbff; outline-offset: 2px; }
@media (max-width: 600px) { .jt-home { right: 10px; width: 40px; height: 40px; border-radius: 10px; } }
@media (prefers-reduced-motion: reduce) { .jt-home { transition: none; } }"""


def home_html(home: str = "./") -> str:
    """返回首页按钮的 HTML；home 为相对链接（根级 './'、一级目录 '../'）。"""
    if not home.endswith("/") or home.startswith("/"):
        raise ValueError(f"home 必须是相对目录链接（'./' 或 '../'），收到 {home!r}")
    return HOME_HTML.format(home=home)
