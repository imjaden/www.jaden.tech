# SSL 证书管理工具

使用 certbot 生成 Let's Encrypt SSL 证书。

## 域名

- `www.jaden.tech`
- `cloudwise.archived.jaden.tech`
- `intfocus.archived.jaden.tech`

## 用法

```bash
cd /Users/jadenli/CodeSpace/jaden.tech/scripts

# 检查远程域名证书
python ssl-manager.py --check-remote

# 检查本地证书
python ssl-manager.py --check

# 生成证书（DNS 验证）
python ssl-manager.py --dns

# 生成证书（HTTP 验证）
python ssl-manager.py --http

# 强制重新生成
python ssl-manager.py --dns --force

# 列出所有证书
python ssl-manager.py --list
```

## 验证方式

| 方式 | 说明 |
|:---|:---|
| HTTP | 需 80 端口开放 |
| DNS | 需添加 TXT 记录（推荐） |

## 证书目录

```
certs/
├── YYYYMMDD/        # 按日期命名
│   ├── fullchain.pem
│   └── privkey.pem
├── work/
├── config/
└── logs/
```

## 链接

- [阿里云 DNS](https://dnsnext.console.aliyun.com/authoritative/domains/jaden.tech)
- [阿里云 SSL](https://yundun.console.aliyun.com/?p=cas#/overview/cn-hangzhou)
