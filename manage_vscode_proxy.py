#!/usr/bin/env python3
"""
VSCode Server 代理配置管理器
用于管理 ~/.vscode-server/data/Machine/settings.json 中的代理设置

Author: Nan Li
License: MIT
Version: 1.0.2
"""

import os
import json
import argparse
import yaml
import sys
import shutil
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


class VSCodeProxyManager:
    def __init__(self, config_path: str = "config.yaml"):
        """
        初始化VSCode代理管理器
        
        Args:
            config_path: 配置文件路径
            
        Raises:
            FileNotFoundError: 当配置文件不存在且无法使用默认配置时
        """
        self.config_path = config_path
        self.config = self.load_config(config_path)
        self.settings_path = Path.home() / ".vscode-server" / "data" / "Machine" / "settings.json"
        logger.debug(f"Settings path: {self.settings_path}")
        
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """
        加载配置文件
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            配置字典
            
        Raises:
            yaml.YAMLError: 当配置文件格式错误时
        """
        if not os.path.exists(config_path):
            logger.warning(f"配置文件 {config_path} 不存在，使用默认配置")
            return self.get_default_config()
            
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                if not config:
                    logger.warning("配置文件为空，使用默认配置")
                    return self.get_default_config()
                logger.info(f"成功加载配置文件: {config_path}")
                return config
        except yaml.YAMLError as e:
            logger.error(f"配置文件格式错误: {e}")
            raise
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """
        获取默认配置
        
        Returns:
            Dict[str, Any]: 默认配置字典，包含 proxy, python, backup 三个部分
        """
        return {
            'proxy': {
                'host': 'localhost',
                'port': 7890,
                'enabled': True,
                'proxy_support': 'override',
                'strict_ssl': False
            },
            'python': {
                'interpreter': ''
            },
            'backup': {
                'enabled': True,
                'suffix': '.backup',
                'max_backups': 5
            }
        }
    
    def backup_settings(self) -> bool:
        """
        备份当前设置文件
        
        Returns:
            bool: 备份是否成功
        """
        if not self.config['backup']['enabled']:
            return True
            
        if not self.settings_path.exists():
            return True
            
        try:
            # 清理旧的备份文件
            backup_dir = self.settings_path.parent
            backup_files = list(backup_dir.glob(f"settings.json{self.config['backup']['suffix']}*"))
            backup_files.sort()
            
            # 保留最近的max_backups-1个备份
            while len(backup_files) >= self.config['backup']['max_backups']:
                oldest = backup_files.pop(0)
                oldest.unlink()
            
            # 创建新备份
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = backup_dir / f"settings.json{self.config['backup']['suffix']}.{timestamp}"
            
            shutil.copy2(self.settings_path, backup_path)
            logger.info(f"已备份原始设置文件到: {backup_path}")
            return True
            
        except PermissionError as e:
            logger.error(f"权限不足，无法创建备份: {e}")
            return False
        except Exception as e:
            logger.warning(f"备份失败: {e}")
            return False
    
    def load_settings(self) -> Dict[str, Any]:
        """
        加载当前设置
        
        Returns:
            Dict[str, Any]: 设置字典，如果文件不存在或格式错误返回空字典
            
        Raises:
            PermissionError: 当没有读取权限时
        """
        if not self.settings_path.exists():
            logger.info("设置文件不存在，将创建新文件")
            return {}
            
        try:
            with open(self.settings_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                logger.debug(f"成功加载设置文件，包含 {len(settings)} 个配置项")
                return settings
        except json.JSONDecodeError as e:
            logger.warning(f"设置文件格式错误: {e}，将创建新的设置")
            return {}
        except PermissionError as e:
            logger.error(f"权限不足，无法读取设置文件: {e}")
            raise
        except Exception as e:
            logger.error(f"读取设置文件失败: {e}")
            return {}
    
    def _check_and_show_changes(self, current_settings: Dict[str, Any], new_config: Dict[str, Any]) -> bool:
        """
        检查并显示配置变化
        
        Args:
            current_settings: 当前设置
            new_config: 新的代理配置
            
        Returns:
            bool: 是否有变化
        """
        changes = []
        
        for key, new_value in new_config.items():
            old_value = current_settings.get(key)
            
            # 特殊处理 http.proxy，隐藏可能的密码信息
            if key == "http.proxy":
                old_display = self._mask_proxy_url(old_value) if old_value else None
                new_display = self._mask_proxy_url(new_value)
                
                if old_value != new_value:
                    if old_value is None:
                        changes.append(f"  + {key}: {new_display}")
                    else:
                        changes.append(f"  ~ {key}: {old_display} → {new_display}")
            else:
                if old_value != new_value:
                    if old_value is None:
                        changes.append(f"  + {key}: {new_value}")
                    else:
                        changes.append(f"  ~ {key}: {old_value} → {new_value}")
        
        if changes:
            logger.info("检测到配置变化:")
            for change in changes:
                print(change)
            return True
        
        return False
    
    def _mask_proxy_url(self, proxy_url: Optional[str]) -> Optional[str]:
        """
        遮蔽代理URL中的密码信息
        
        Args:
            proxy_url: 代理URL
            
        Returns:
            str: 遮蔽后的URL
        """
        if not proxy_url:
            return None
            
        # 检查是否包含认证信息
        if '@' in proxy_url:
            # 格式: http://username:password@host:port
            protocol, rest = proxy_url.split('://', 1)
            auth, host = rest.split('@', 1)
            
            if ':' in auth:
                username = auth.split(':')[0]
                return f"{protocol}://{username}:****@{host}"
        
        return proxy_url
    
    def save_settings(self, settings: Dict[str, Any]) -> bool:
        """
        保存设置到文件
        
        Args:
            settings: 设置字典
            
        Returns:
            bool: 保存是否成功
            
        Raises:
            PermissionError: 当没有写入权限时
        """
        try:
            # 确保目录存在
            self.settings_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 保存设置
            with open(self.settings_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
            
            logger.info(f"设置已保存到: {self.settings_path}")
            return True
            
        except PermissionError as e:
            logger.error(f"权限不足，无法保存设置: {e}")
            raise
        except Exception as e:
            logger.error(f"保存设置失败: {e}")
            return False
    
    def check_proxy_changes(self, enable: bool, host: Optional[str] = None, port: Optional[int] = None) -> Tuple[bool, Optional[str]]:
        """
        检查代理配置是否会发生变化
        
        Args:
            enable: 是否启用代理
            host: 代理主机（可选，默认使用配置）
            port: 代理端口（可选，默认使用配置）
            
        Returns:
            tuple[bool, Optional[str]]: (是否有变化, 变化描述或None)
        """
        try:
            settings = self.load_settings()
            
            if enable:
                # 构建新的代理配置
                proxy_host = host or self.config['proxy']['host']
                proxy_port = port or self.config['proxy']['port']
                proxy_url = f"http://{proxy_host}:{proxy_port}"
                
                proxy_config = {
                    "http.proxySupport": self.config['proxy']['proxy_support'],
                    "http.proxy": proxy_url,
                    "http.proxyStrictSSL": self.config['proxy']['strict_ssl']
                }
                
                # 检查变化
                has_changes = self._check_and_show_changes(settings, proxy_config)
                return has_changes, None
            else:
                # 检查是否已经禁用
                has_proxy = any(key in settings for key in ["http.proxy", "http.proxySupport", "http.proxyStrictSSL"])
                return has_proxy, None
                
        except Exception as e:
            logger.error(f"检查配置变化失败: {e}")
            return True, None  # 发生错误时，假设有变化以允许操作继续
    
    def set_proxy(self, enable: bool, host: Optional[str] = None, port: Optional[int] = None) -> bool:
        """
        设置或移除代理
        
        Args:
            enable: 是否启用代理
            host: 代理主机（可选，默认使用配置）
            port: 代理端口（可选，默认使用配置）
            
        Returns:
            bool: 操作是否成功
        """
        try:
            # 加载当前设置
            settings = self.load_settings()
            
            # 构建代理配置
            proxy_config = {}
            
            if enable:
                # 使用参数或配置中的值
                proxy_host = host or self.config['proxy']['host']
                proxy_port = port or self.config['proxy']['port']
                proxy_url = f"http://{proxy_host}:{proxy_port}"
                
                proxy_config = {
                    "http.proxySupport": self.config['proxy']['proxy_support'],
                    "http.proxy": proxy_url,
                    "http.proxyStrictSSL": self.config['proxy']['strict_ssl']
                }
                
                # 备份原始设置
                if not self.backup_settings():
                    print("警告: 备份失败，继续操作...")
                
                # 更新设置
                settings.update(proxy_config)
                logger.info(f"设置代理: {proxy_url}")
            else:
                # 备份原始设置
                if not self.backup_settings():
                    print("警告: 备份失败，继续操作...")
                
                logger.info("移除代理配置")
                # 移除代理相关配置
                settings.pop("http.proxySupport", None)
                settings.pop("http.proxy", None)
                settings.pop("http.proxyStrictSSL", None)
            
            # 保存设置
            return self.save_settings(settings)
            
        except PermissionError:
            # 已经在 save_settings 中记录了错误
            return False
        except Exception as e:
            logger.error(f"设置代理失败: {e}")
            return False
    
    def show_current_proxy(self) -> None:
        """
        显示当前代理设置
        
        输出当前 VSCode Server 的代理配置信息，包括代理地址、SSL 验证等
        """
        try:
            settings = self.load_settings()
            
            proxy_support = settings.get("http.proxySupport", "未设置")
            proxy = settings.get("http.proxy", "未设置")
            strict_ssl = settings.get("http.proxyStrictSSL", "未设置")
            
            print("\n" + "="*50)
            print("当前代理配置")
            print("="*50)
            print(f"  配置文件: {self.settings_path}")
            print(f"  http.proxySupport: {proxy_support}")
            print(f"  http.proxy: {proxy}")
            print(f"  http.proxyStrictSSL: {strict_ssl}")
            print("="*50)
            
            if proxy and proxy != "未设置":
                print(f"\n✓ 状态: 已启用代理 ({proxy})")
            else:
                print("\n○ 状态: 未配置代理")
            print()
            
        except Exception as e:
            logger.error(f"显示配置失败: {e}")


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="VSCode Server代理配置管理器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s enable                    # 启用代理
  %(prog)s disable                   # 禁用代理
  %(prog)s status                    # 查看当前状态
  %(prog)s enable --host 127.0.0.1 --port 8888  # 指定主机和端口
  %(prog)s --config /path/to/config.yaml enable  # 指定配置文件
        """
    )
    
    # 主要命令
    parser.add_argument(
        'action',
        choices=['enable', 'disable', 'status', 'on', 'off'],
        nargs='?',
        default='status',
        help='操作类型: enable/on (启用), disable/off (禁用), status (查看状态)'
    )
    
    # 可选参数
    parser.add_argument(
        '-c', '--config',
        default='config.yaml',
        help='配置文件路径 (默认: config.yaml)'
    )
    
    parser.add_argument(
        '--host',
        help='代理主机地址 (覆盖配置文件)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        help='代理端口 (覆盖配置文件)'
    )
    
    parser.add_argument(
        '-y', '--yes',
        action='store_true',
        help='自动确认操作'
    )
    
    return parser.parse_args()


def main():
    """主函数"""
    args = parse_arguments()
    
    # 初始化管理器
    try:
        manager = VSCodeProxyManager(args.config)
    except Exception as e:
        print(f"初始化失败: {e}")
        return 1
    
    # 根据action执行操作
    if args.action in ['enable', 'on']:
        # 先检查是否有变化
        has_changes, _ = manager.check_proxy_changes(True, args.host, args.port)
        
        if not has_changes:
            logger.info("代理配置未发生变化")
            print("✓ 代理配置已是最新状态")
            return 0
        
        # 确认操作
        if not args.yes:
            confirm = input("确定要启用代理吗？(y/N): ")
            if confirm.lower() not in ['y', 'yes']:
                print("操作已取消")
                return 0
        
        # 启用代理
        success = manager.set_proxy(True, args.host, args.port)
        if success:
            print("✓ 代理已启用")
        else:
            print("✗ 启用代理失败")
            return 1
            
    elif args.action in ['disable', 'off']:
        # 先检查是否有变化
        has_changes, _ = manager.check_proxy_changes(False)
        
        if not has_changes:
            logger.info("代理配置已经处于禁用状态")
            print("✓ 代理配置已是禁用状态")
            return 0
        
        # 确认操作
        if not args.yes:
            confirm = input("确定要禁用代理吗？(y/N): ")
            if confirm.lower() not in ['y', 'yes']:
                print("操作已取消")
                return 0
        
        # 禁用代理
        success = manager.set_proxy(False)
        if success:
            print("✓ 代理已禁用")
        else:
            print("✗ 禁用代理失败")
            return 1
            
    else:  # status
        manager.show_current_proxy()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
