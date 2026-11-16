#!/usr/bin/env python3
"""SYNC 戳的唯一实现（生产者与校验器共用，避免两侧口径漂移）。

戳形态（单行、不可见、不改渲染）：
  HTML  <!-- SYNC id=<id> producer=<repo/path> v=<n> generated=<ISO8601> sha256=<16hex> -->
  JS    /* SYNC id=<id> producer=<repo/path> v=<n> generated=<ISO8601> sha256=<16hex> */

口径（写死在这里，别在调用方另算）：
  * sha256 = 去掉戳行之后其余文本的 sha256 前 16 位十六进制 ⇒ 戳自身不参与哈希（否则自指）
  * generated 必须来自**数据源**（数据包的 generated_at / 源文件 mtime），不能是 now()
    ⇒ 同一输入重复生成必须逐字节相同（幂等），否则每次跑都脏工作树、review 每轮多一笔。
  * 戳行只出现在文件开头 3 行内；strip 只去掉第一处匹配，保留其余内容原样。
"""
import hashlib
import re

FIELDS = ("id", "producer", "v", "generated", "sha256")

_STAMP_RE = re.compile(r"^(?:<!-- SYNC (?P<html>.*?) -->|/\* SYNC (?P<js>.*?) \*/)$")


def digest(text):
    """去掉戳行后的内容哈希（16 位十六进制）。"""
    return hashlib.sha256(strip_stamp(text).encode("utf-8")).hexdigest()[:16]


def _line(fields):
    missing = [k for k in FIELDS if not fields.get(k)]
    if missing:
        raise ValueError(f"stamp fields missing: {missing}")
    return " ".join(f"{k}={fields[k]}" for k in FIELDS)


def html_stamp(text, **fields):
    """打戳并保证 `parse()` 读得到（幂等：已有戳先剥再打）。

    `parse()` 只扫**前 3 行**，而 DOCTYPE 不一定在第 1 行：有的页面把版权/版本注释
    写在 DOCTYPE 之前（实测 daily-poetry.html 的 DOCTYPE 在第 14 行）⇒ 插在 DOCTYPE
    之后等于白打（parse 返回 None，站点判「未打戳」）。所以插入后要回读校验，
    读不到就退回「打首行」。
    """
    anchor = "<!DOCTYPE html>"
    body = strip_stamp(text)
    line = "<!-- SYNC " + _line(fields) + " -->"
    if anchor in body:
        out = body.replace(anchor, anchor + "\n" + line, 1)
        if parse(out):          # 回读：戳落在前 3 行内才算成功
            return out
    # 兜底：DOCTYPE 在第 3 行之后，或页面根本没有 DOCTYPE ⇒ 打首行
    return line + "\n" + body


def js_stamp(text, **fields):
    """在文件首行打戳（幂等）。"""
    line = "/* SYNC " + _line(fields) + " */"
    return line + "\n" + strip_stamp(text)


def strip_stamp(text):
    """去掉第一处戳行（含其换行），其余字节原样返回。"""
    out = []
    removed = False
    for line in text.splitlines(keepends=True):
        if not removed and _STAMP_RE.match(line.strip()):
            removed = True
            continue
        out.append(line)
    return "".join(out)


def parse(text):
    """解析前 3 行内的戳；无戳返回 None。"""
    for line in text.splitlines()[:3]:
        m = _STAMP_RE.match(line.strip())
        if not m:
            continue
        body = m.group("html") or m.group("js") or ""
        fields = {}
        for token in body.split():
            if "=" in token:
                key, value = token.split("=", 1)
                fields[key] = value
        return fields
    return None
