# jaden.tech

个人主页 — [jaden.tech](https://jaden.tech)

## 项目结构

```
├── index.html                # 主页
├── static/
│   ├── css/index.css         # 样式
│   ├── js/                   # 脚本
│   └── img/                  # 图片
└── scripts/
    ├── ssl-manager.py        # SSL 证书生成
    └── timestamp-manager.py  # 时间戳管理
```

## 技术栈

HTML + CSS + JavaScript | GitHub Pages

```bash
python3 -m http.server 8080
```

## SSL 证书

```bash
python scripts/ssl-manager.py --check-remote
```

域名：`jaden.tech` `cloudwise.archived.jaden.tech` `intfocus.archived.jaden.tech`

## 时间戳管理

```bash
# 检查时间戳状态
python3 scripts/timestamp-manager.py check

# 更新时间戳（如果超过 1 小时）
python3 scripts/timestamp-manager.py update

# 强制更新时间戳
python3 scripts/timestamp-manager.py force
```

## License

© Jaden Li. All rights reserved.
