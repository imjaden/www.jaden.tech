#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Karpathy Principles - AI编程四大原则
=====================================
1. 先思考 - 不假设，不隐藏困惑 → 不确定就问，多种解释列出
2. 保持简单 - 最小代码解决问题 → 无多余抽象
3. 精准修改 - 只改必须改的 → 不"顺便"改进邻接代码
4. 目标驱动 - 测试先行，验证闭环 → "修bug"→"写测试复现→让测试通过"

Version: 1.0(2026-06-08)
Description
- 管理 HTML 文件中的资源时间戳参数，确保两个 HTML 文件使用相同时间戳
- 当时间戳与当前时间相差超过1小时时自动更新

【指令清单】
| 指令 | 功能说明 |
|------|---------|
| check | 检查时间戳状态 |
| update | 更新时间戳（如果超过1小时） |
| force | 强制更新时间戳 |
| help | 显示帮助信息 |

【辅助工具】
| 工具方法 | 功能说明 |
|---------|---------|
| _format_path() | 路径格式化，支持项目相对路径和 ~ 简写 |
| _print_with_emoji() | 智能打印，自动匹配 Emoji 前缀 |
| _setup_logger() | 设置日志系统 |

Related Paths
- 项目目录: /Users/jadenli/CodeSpace/jaden.tech
- HTML 文件: index.html

Environments:
- Mac MacBookPro-2025-26.5-25F71
- Bash 5.2.26
- Python 3.12.0
- IDE TRAE CN
- LLM GLM-4.7

Dependency
- re (正则表达式)
- time (时间处理)
- datetime (日期时间)

Sublime Text
- Command + k, Command + 1 收缩所有函数代码
- Command + k, Command + j 展示所有函数代码

触发条件
- 需要更新 HTML 资源时间戳时
- 需要检查时间戳状态时

版本说明
- 主版本号默认为 1，修订号从 0 开始
- 每次代码修改后修订号 +1
- 重大架构变更时主版本号 +1，修订号归零
"""

import re
import time
from datetime import datetime, timedelta
from pathlib import Path


class TimestampManager:
    """时间戳管理器"""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.project_root = self.script_dir.parent
        self.html_files = [
            self.project_root / 'index.html'
        ]
        self.timestamp_pattern = re.compile(r'\?t=(\d+)')
        self.update_threshold = timedelta(hours=1)
    
    def _format_path(self, absolute_path):
        """【辅助工具】格式化路径：绝对路径若包含当前项目路径，则打印相对路径"""
        if str(absolute_path).startswith(str(self.project_root)):
            return str(absolute_path.relative_to(self.project_root))
        return str(absolute_path)
    
    def _print_with_emoji(self, message, prefix_emoji=None):
        """【辅助工具】智能打印：根据内容自动添加 Emoji 前缀
        
        Args:
            message: 打印内容
            prefix_emoji: 强制指定 Emoji（可选），未指定时根据内容智能匹配
        """
        if prefix_emoji:
            print(f"{prefix_emoji} {message}")
            return
        
        msg_lower = message.lower()
        emoji_rules = [
            (['完成', '成功', 'done', '已生成', '已创建', '已更新', 'success', 'ok'], '✅'),
            (['错误', '失败', 'error', 'fail', '中止', '不存在'], '❌'),
            (['警告', '注意', 'warning', 'warn', '已过期', '检测', '已有'], '⚠️'),
            (['帮助', 'help', '文档', '说明'], '📖'),
            (['创建', '笔记', '写入', 'create', 'write'], '📝'),
            (['缓存', '保存', 'cache', 'save'], '💾'),
            (['查看', '打开', '编辑', 'open', 'view', 'edit'], '⌨️'),
            (['跳过', '忽略', 'skip', 'ignore'], '⏭️'),
            (['刷新', '更新', '重置', 'refresh', 'update'], '🔄'),
        ]
        
        for keywords, emoji in emoji_rules:
            if any(k in msg_lower for k in keywords):
                print(f"{emoji} {message}")
                return
        
        print(f"ℹ️ {message}")
    
    def _extract_timestamp(self, content):
        """从 HTML 内容中提取时间戳
        
        Args:
            content: HTML 内容
            
        Returns:
            时间戳（整数），如果没有找到则返回 None
        """
        matches = self.timestamp_pattern.findall(content)
        if not matches:
            return None
        
        # 返回第一个匹配的时间戳（所有时间戳应该相同）
        return int(matches[0])
    
    def _update_timestamps(self, content, new_timestamp):
        """更新 HTML 内容中的所有时间戳
        
        Args:
            content: HTML 内容
            new_timestamp: 新时间戳
            
        Returns:
            更新后的 HTML 内容
        """
        return self.timestamp_pattern.sub(f'?t={new_timestamp}', content)
    
    def _get_timestamp_age(self, timestamp):
        """获取时间戳的年龄
        
        Args:
            timestamp: 时间戳（整数）
            
        Returns:
            时间差（timedelta）
        """
        timestamp_dt = datetime.fromtimestamp(timestamp)
        return datetime.now() - timestamp_dt
    
    def handle_check(self):
        """【1】检查时间戳状态
        
        检查所有 HTML 文件中的时间戳，显示当前时间戳和年龄
        """
        print("\n" + "=" * 60)
        print("📊 时间戳状态检查")
        print("=" * 60)
        
        all_timestamps = []
        
        for html_file in self.html_files:
            if not html_file.exists():
                self._print_with_emoji(f"文件不存在: {self._format_path(html_file)}", '❌')
                continue
            
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            timestamp = self._extract_timestamp(content)
            
            if timestamp is None:
                self._print_with_emoji(f"{self._format_path(html_file)}: 未找到时间戳", '⚠️')
                continue
            
            age = self._get_timestamp_age(timestamp)
            age_str = self._format_age(age)
            
            print(f"\n📄 {self._format_path(html_file)}")
            print(f"   时间戳: {timestamp}")
            print(f"   年龄: {age_str}")
            print(f"   时间: {datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')}")
            
            all_timestamps.append(timestamp)
        
        # 检查所有文件的时间戳是否一致
        if len(all_timestamps) > 0:
            unique_timestamps = set(all_timestamps)
            if len(unique_timestamps) == 1:
                print(f"\n✅ 所有文件使用相同时间戳: {all_timestamps[0]}")
            else:
                print(f"\n⚠️ 文件时间戳不一致: {unique_timestamps}")
        
        print("\n" + "=" * 60)
    
    def _format_age(self, age):
        """格式化时间差为可读字符串
        
        Args:
            age: 时间差（timedelta）
            
        Returns:
            格式化的时间差字符串
        """
        total_seconds = int(age.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        
        if hours > 24:
            days = hours // 24
            hours = hours % 24
            return f"{days}天{hours}小时{minutes}分钟"
        elif hours > 0:
            return f"{hours}小时{minutes}分钟"
        else:
            return f"{minutes}分钟"
    
    def handle_update(self, force=False):
        """【2】更新时间戳
        
        Args:
            force: 是否强制更新（忽略时间阈值）
        """
        print("\n" + "=" * 60)
        print("🔄 时间戳更新")
        print("=" * 60)
        
        # 收集所有文件的时间戳
        all_timestamps = []
        file_timestamps = {}
        
        for html_file in self.html_files:
            if not html_file.exists():
                self._print_with_emoji(f"文件不存在: {self._format_path(html_file)}", '❌')
                continue
            
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            timestamp = self._extract_timestamp(content)
            
            if timestamp is None:
                self._print_with_emoji(f"{self._format_path(html_file)}: 未找到时间戳", '⚠️')
                continue
            
            all_timestamps.append(timestamp)
            file_timestamps[html_file] = timestamp
        
        if not all_timestamps:
            self._print_with_emoji("没有找到任何时间戳", '❌')
            return
        
        # 检查是否需要更新
        unique_timestamps = set(all_timestamps)
        
        if len(unique_timestamps) > 1:
            self._print_with_emoji(f"文件时间戳不一致，将统一更新", '⚠️')
            should_update = True
        else:
            current_timestamp = all_timestamps[0]
            age = self._get_timestamp_age(current_timestamp)
            
            if force:
                should_update = True
                self._print_with_emoji(f"强制更新模式，忽略时间阈值", '🔄')
            elif age > self.update_threshold:
                should_update = True
                self._print_with_emoji(f"时间戳已过期（{self._format_age(age)}），需要更新", '⚠️')
            else:
                should_update = False
                self._print_with_emoji(f"时间戳未过期（{self._format_age(age)}），跳过更新", '⏭️')
        
        if not should_update:
            print("\n" + "=" * 60)
            return
        
        # 生成新时间戳
        new_timestamp = int(time.time())
        self._print_with_emoji(f"新时间戳: {new_timestamp}", '📝')
        
        # 更新所有文件
        updated_count = 0
        for html_file in self.html_files:
            if not html_file.exists():
                continue
            
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = self._update_timestamps(content, new_timestamp)
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            updated_count += 1
            self._print_with_emoji(f"已更新: {self._format_path(html_file)}")
        
        print(f"\n✅ 成功更新 {updated_count} 个文件")
        print("\n" + "=" * 60)
    
    def handle_force(self):
        """【3】强制更新时间戳
        
        忽略时间阈值，强制更新所有时间戳
        """
        self.handle_update(force=True)
    
    def handle_help(self):
        """【打印帮助信息】"""
        print("\n" + "=" * 60)
        print("📖 timestamp-manager 使用说明")
        print("=" * 60)
        
        print("\n【功能概述】")
        print("  管理 HTML 文件中的资源时间戳参数，确保两个 HTML 文件使用相同时间戳")
        print("  当时间戳与当前时间相差超过1小时时自动更新")
        
        print("\n【支持的指令】")
        print("  check      - 检查时间戳状态")
        print("  update     - 更新时间戳（如果超过1小时）")
        print("  force      - 强制更新时间戳")
        print("  help       - 显示帮助信息")
        
        print("\n【使用示例】")
        print("  python3 timestamp-manager.py check      # 检查时间戳状态")
        print("  python3 timestamp-manager.py update     # 更新时间戳")
        print("  python3 timestamp-manager.py force      # 强制更新时间戳")
        print("  python3 timestamp-manager.py help       # 显示帮助信息")
        
        print("\n【配置说明】")
        print(f"  更新阈值: {self.update_threshold}")
        print(f"  监控文件: {', '.join([self._format_path(f) for f in self.html_files])}")
        
        print("\n" + "=" * 60)
    
    def run(self, command):
        """运行命令
        
        Args:
            command: 命令名称
        """
        commands = {
            'check': self.handle_check,
            'update': self.handle_update,
            'force': self.handle_force,
            'help': self.handle_help,
        }
        
        if command in commands:
            commands[command]()
        else:
            self._print_with_emoji(f"未知命令: {command}", '❌')
            self.handle_help()


def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 timestamp-manager.py <command>")
        print("Commands: check, update, force, help")
        sys.exit(1)
    
    command = sys.argv[1]
    
    manager = TimestampManager()
    manager.run(command)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)