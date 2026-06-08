#!/usr/bin/env python3
"""
SSL 证书管理工具
使用 certbot 生成 Let's Encrypt SSL 证书

用法:
    python ssl-manager.py                  # 交互式选择验证方式
    python ssl-manager.py --http           # 使用 HTTP 验证
    python ssl-manager.py --dns            # 使用 DNS 验证
    python ssl-manager.py --force          # 强制重新生成
    python ssl-manager.py --check          # 仅检查本地证书状态
    python ssl-manager.py --check-remote   # 检查远程域名证书
"""

import os
import sys
import subprocess
import socket
import shutil
import ssl
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional, Tuple
from prettytable import PrettyTable

# ==================== 配置参数 ====================
DOMAINS = [
    "jaden.tech",
    "cloudwise.archived.jaden.tech",
    "intfocus.archived.jaden.tech",
]

EMAIL = "527130673@qq.com"
BASE_CERT_DIR = Path.home() / "CodeSpace" / "jaden.tech" / "certs"
CURRENT_DATE = datetime.now().strftime("%Y%m%d")
CERT_PATH = BASE_CERT_DIR / CURRENT_DATE

# 阿里云 DNS 控制台链接
ALIYUN_DNS_URL = "https://dnsnext.console.aliyun.com/authoritative/domains/jaden.tech"
ALIYUN_SSL_URL = "https://yundun.console.aliyun.com/?p=cas#/overview/cn-hangzhou"


# ==================== 工具函数 ====================
class Colors:
    """终端颜色"""
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    RESET = "\033[0m"


def print_success(msg: str):
    print(f"{Colors.GREEN}✅ {msg}{Colors.RESET}")


def print_error(msg: str):
    print(f"{Colors.RED}❌ {msg}{Colors.RESET}")


def print_warning(msg: str):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.RESET}")


def print_info(msg: str):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.RESET}")


def run_command(cmd: str, sudo: bool = False, check: bool = True) -> Tuple[str, bool]:
    """执行命令并返回输出"""
    if sudo:
        cmd = f"sudo {cmd}"
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode != 0:
            if check and result.stderr:
                print_error(result.stderr)
            return result.stderr, False
        
        return result.stdout.strip(), True
        
    except subprocess.TimeoutExpired:
        print_error("命令执行超时")
        return "", False
    except Exception as e:
        print_error(f"命令执行失败: {e}")
        return "", False


def check_port_available(port: int) -> bool:
    """检查端口是否可用"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex(('localhost', port))
            return result != 0
    except Exception:
        return False


def check_dependencies() -> bool:
    """检查依赖"""
    print("\n=== 检查依赖 ===")
    
    if shutil.which("brew"):
        print_success("已安装 Homebrew")
    else:
        print_error("请先安装 Homebrew")
        return False
    
    if shutil.which("certbot"):
        print_success("已安装 certbot")
    else:
        print_warning("未安装 certbot，正在安装...")
        _, ok = run_command("brew install certbot")
        if not ok:
            print_error("certbot 安装失败")
            return False
    
    if shutil.which("openssl"):
        print_success("已安装 openssl")
    else:
        print_error("请先安装 openssl")
        return False
    
    return True


# ==================== 证书操作 ====================
def get_latest_cert_dir() -> Optional[Path]:
    """获取最新证书目录"""
    if not BASE_CERT_DIR.exists():
        return None
    
    cert_dirs = []
    for d in BASE_CERT_DIR.iterdir():
        if d.is_dir() and d.name.isdigit() and len(d.name) == 8:
            cert_dirs.append(d)
    
    return max(cert_dirs) if cert_dirs else None


def check_cert_expiry(cert_path: Path) -> Optional[int]:
    """检查本地证书有效期，返回剩余天数"""
    fullchain = cert_path / "fullchain.pem"
    if not fullchain.exists():
        print_warning(f"证书文件不存在: {fullchain}")
        return None
    
    print(f"\n=== 本地证书检查 ===")
    print(f"路径: {cert_path}")
    
    output, ok = run_command(f"openssl x509 -in {fullchain} -noout -dates", check=False)
    if not ok:
        return None
    
    for line in output.split("\n"):
        if line.startswith("notAfter="):
            expiry_str = line.replace("notAfter=", "").strip()
            expiry_time = datetime.strptime(expiry_str, "%b %d %H:%M:%S %Y %Z")
            remaining = (expiry_time - datetime.now(timezone.utc)).days
            
            print(f"过期时间: {expiry_time}")
            print(f"剩余天数: {remaining} 天")
            
            if remaining <= 0:
                print_error("证书已过期！")
            elif remaining <= 30:
                print_warning(f"即将过期，建议续期")
            else:
                print_success("证书有效")
            
            return remaining
    
    return None


def get_remote_cert_info(domain: str) -> dict:
    """获取远程域名证书信息"""
    info = {
        "domain": domain,
        "success": False,
        "not_before": None,
        "not_after": None,
        "remaining_days": None,
        "error": None
    }
    
    try:
        # 创建 SSL 上下文
        ctx = ssl.create_default_context()
        
        with socket.create_connection((domain, 443), timeout=30) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                
                # 解析证书时间
                not_before_str = cert['notBefore']
                not_after_str = cert['notAfter']
                
                # 格式: Jun  7 12:00:00 2026 GMT
                info["not_before"] = datetime.strptime(not_before_str, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
                info["not_after"] = datetime.strptime(not_after_str, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
                info["remaining_days"] = (info["not_after"] - datetime.now(timezone.utc)).days
                info["success"] = True
                
    except Exception as e:
        info["error"] = str(e)
    
    return info


def check_remote_certs() -> None:
    """检查所有远程域名证书"""
    print("\n=== 远程域名 SSL 证书检查 ===\n")
    
    results = []
    for domain in DOMAINS:
        print(f"检查 {domain} ...")
        info = get_remote_cert_info(domain)
        results.append(info)
    
    # 使用 prettytable 打印表格
    table = PrettyTable()
    table.field_names = ["域名", "创建时间", "过期时间", "剩余天数"]
    table.align["域名"] = "l"
    table.align["创建时间"] = "c"
    table.align["过期时间"] = "c"
    table.align["剩余天数"] = "c"
    
    for info in results:
        domain = info["domain"]
        
        if info["success"]:
            not_before = info["not_before"].strftime("%Y-%m-%d")
            not_after = info["not_after"].strftime("%Y-%m-%d")
            remaining = info["remaining_days"]
            
            if remaining <= 0:
                remaining_str = f"已过期 ({remaining}天)"
            else:
                remaining_str = f"{remaining}天"
            
            table.add_row([domain, not_before, not_after, remaining_str])
        else:
            table.add_row([domain, "-", "-", "无法获取"])
    
    print(f"\n{table}")
    
    # 统计
    success_count = sum(1 for r in results if r["success"])
    expired_count = sum(1 for r in results if r["success"] and r["remaining_days"] <= 0)
    warning_count = sum(1 for r in results if r["success"] and 0 < r["remaining_days"] <= 30)
    
    print(f"\n统计: 共 {len(DOMAINS)} 个域名, "
          f"{success_count} 个成功, "
          f"{expired_count} 个已过期, "
          f"{warning_count} 个即将过期")


def generate_certificate(auth_method: str, force: bool = False) -> Optional[Path]:
    """生成 SSL 证书"""
    if CERT_PATH.exists() and not force:
        print_info(f"今日已生成证书 ({CERT_PATH})")
        print_info("使用 --force 强制重新生成")
        return CERT_PATH
    
    print("\n=== 生成 SSL 证书 ===")
    print(f"域名: {', '.join(DOMAINS)}")
    print(f"目录: {CERT_PATH}")
    
    domain_params = " ".join(f"-d {d}" for d in DOMAINS)
    
    work_dir = BASE_CERT_DIR / "work"
    config_dir = BASE_CERT_DIR / "config"
    logs_dir = BASE_CERT_DIR / "logs"
    
    for d in [work_dir, config_dir, logs_dir]:
        d.mkdir(parents=True, exist_ok=True)
    
    if auth_method == "http":
        if not check_port_available(80):
            print_error("80 端口被占用")
            return None
        
        cmd = (
            f"certbot certonly --standalone --preferred-challenges http "
            f"--email {EMAIL} --agree-tos --no-eff-email "
            f"{domain_params} "
            f"--work-dir {work_dir} --config-dir {config_dir} --logs-dir {logs_dir} "
            f"--cert-path {CERT_PATH}"
        )
        
    elif auth_method == "dns":
        print("\n请添加 DNS TXT 记录:")
        print("-" * 50)
        for domain in DOMAINS:
            print(f"  域名: _acme-challenge.{domain}")
        print("-" * 50)
        print(f"阿里云 DNS: {ALIYUN_DNS_URL}")
        
        cmd = (
            f"certbot certonly --manual --preferred-challenges dns "
            f"--email {EMAIL} --agree-tos --no-eff-email "
            f"{domain_params} "
            f"--work-dir {work_dir} --config-dir {config_dir} --logs-dir {logs_dir} "
            f"--cert-path {CERT_PATH}"
        )
    else:
        print_error(f"未知验证方式: {auth_method}")
        return None
    
    print("\n开始生成证书...")
    print_warning("按提示操作，需要时按回车继续")
    
    process = subprocess.Popen(
        cmd,
        shell=True,
        stdin=sys.stdin,
        stdout=sys.stdout,
        stderr=sys.stderr
    )
    process.wait()
    
    if process.returncode != 0:
        print_error("证书生成失败")
        return None
    
    if (CERT_PATH / "fullchain.pem").exists():
        current_user = os.getenv("USER", "jadenli")
        run_command(f"chown -R {current_user} {BASE_CERT_DIR}", sudo=True)
        run_command(f"find {BASE_CERT_DIR} -type d -exec chmod 755 {{}} \\;", sudo=True)
        run_command(f"find {BASE_CERT_DIR} -type f -exec chmod 644 {{}} \\;", sudo=True)
    
    print_success("证书生成完成！")
    return CERT_PATH


def upload_guide(cert_path: Path) -> None:
    """显示上传指引"""
    fullchain = cert_path / "fullchain.pem"
    privkey = cert_path / "privkey.pem"
    
    if not fullchain.exists() or not privkey.exists():
        print_error("证书文件不存在")
        return
    
    print("\n=== 上传指引 ===")
    print(f"1. 访问: {ALIYUN_SSL_URL}")
    print(f"2. 上传证书 → 上传自有证书")
    print(f"3. 填写公钥和私钥")
    print(f"4. 绑定域名: {', '.join(DOMAINS)}")


def list_certs() -> None:
    """列出所有证书"""
    print("\n=== 证书列表 ===")
    
    if not BASE_CERT_DIR.exists():
        print_info("暂无证书")
        return
    
    cert_dirs = sorted([
        d for d in BASE_CERT_DIR.iterdir()
        if d.is_dir() and d.name.isdigit() and len(d.name) == 8
    ])
    
    if not cert_dirs:
        print_info("暂无证书")
        return
    
    for d in cert_dirs:
        date_str = d.name
        date_display = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
        fullchain = d / "fullchain.pem"
        
        if fullchain.exists():
            remaining = check_cert_expiry(d)
            if remaining is not None:
                if remaining <= 0:
                    status = f"{Colors.RED}已过期{Colors.RESET}"
                elif remaining <= 30:
                    status = f"{Colors.YELLOW}即将过期{Colors.RESET}"
                else:
                    status = f"{Colors.GREEN}有效{Colors.RESET}"
            else:
                status = "未知"
            print(f"  {date_display}  {status}")
        else:
            print(f"  {date_display}  {Colors.RED}不完整{Colors.RESET}")


# ==================== 主流程 ====================
def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="SSL 证书管理工具")
    parser.add_argument("--http", action="store_true", help="HTTP 验证")
    parser.add_argument("--dns", action="store_true", help="DNS 验证")
    parser.add_argument("--force", action="store_true", help="强制重新生成")
    parser.add_argument("--check", action="store_true", help="检查本地证书")
    parser.add_argument("--check-remote", action="store_true", help="检查远程域名证书")
    parser.add_argument("--list", action="store_true", help="列出所有证书")
    parser.add_argument("--guide", action="store_true", help="显示上传指引")
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("  SSL 证书管理工具")
    print(f"  域名: {', '.join(DOMAINS)}")
    print("=" * 50)
    
    try:
        if args.list:
            list_certs()
            return
        
        if args.check_remote:
            check_remote_certs()
            return
        
        if not check_dependencies():
            sys.exit(1)
        
        latest_cert = get_latest_cert_dir()
        
        if args.check:
            if latest_cert:
                check_cert_expiry(latest_cert)
            else:
                print_warning("暂无本地证书")
            return
        
        if args.guide:
            if latest_cert:
                upload_guide(latest_cert)
            else:
                print_warning("暂无证书")
            return
        
        if args.http:
            auth_method = "http"
        elif args.dns:
            auth_method = "dns"
        else:
            print("\n选择验证方式:")
            print("1. HTTP（需 80 端口）")
            print("2. DNS（推荐）")
            choice = input("请选择 (1/2，默认 2): ").strip() or "2"
            auth_method = "http" if choice == "1" else "dns"
        
        cert_path = generate_certificate(auth_method, force=args.force)
        
        if cert_path:
            check_cert_expiry(cert_path)
            upload_guide(cert_path)
        
        print("\n操作完成！")
        
    except KeyboardInterrupt:
        print("\n\n[中断] 用户终止")
        sys.exit(1)
    except Exception as e:
        print_error(f"执行失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
