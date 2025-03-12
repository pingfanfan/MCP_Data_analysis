#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, check=True):
    """运行shell命令并返回输出"""
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if check and result.returncode != 0:
        print(f"命令执行失败: {cmd}")
        print(f"错误信息: {result.stderr}")
        sys.exit(1)
    return result

def ask_permission(question):
    """询问用户权限"""
    while True:
        response = input(f"{question} (y/n): ").lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False

def check_uv():
    """检查uv是否安装"""
    if shutil.which('uv') is None:
        print("正在安装uv...")
        run_command('curl -LsSf https://astral.sh/uv/install.sh | sh')

def setup_venv():
    """创建虚拟环境"""
    if not os.path.exists('.venv'):
        print("创建虚拟环境...")
        run_command('python3 -m venv .venv')

def sync_dependencies():
    """同步项目依赖"""
    print("同步依赖...")
    run_command('uv pip install -r requirements.txt')

def check_claude_desktop():
    """检查Claude Desktop是否安装"""
    app_path = '/Applications/Claude.app'
    if not os.path.exists(app_path):
        print("请先安装Claude Desktop应用")
        sys.exit(1)

def build_package():
    """构建包并获取wheel路径"""
    print("构建包...")
    run_command('pip install build')
    run_command('python3 -m build')
    wheel_path = None
    for file in os.listdir('dist'):
        if file.endswith('.whl'):
            wheel_path = os.path.abspath(os.path.join('dist', file))
            break
    return wheel_path

def update_config(config_path, config, wheel_path):
    """更新Claude配置"""
    config['mcpServers'] = {
        'mcp-server-ds': {
            'command': 'uvx',
            'args': ['--from', wheel_path, 'mcp-server-ds']
        }
    }
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

def restart_claude():
    """重启Claude Desktop"""
    if ask_permission("需要重启Claude Desktop，是否继续？"):
        run_command('killall Claude', check=False)
        run_command('open -a Claude')

def main():
    # 检查环境
    check_uv()
    check_claude_desktop()
    
    # 同步依赖
    sync_dependencies()
    
    # 构建包
    wheel_path = build_package()
    if not wheel_path:
        print("构建失败")
        sys.exit(1)
        
    # 更新配置
    config_path = os.path.expanduser('~/Library/Application Support/Claude/claude_desktop_config.json')
    if os.path.exists(config_path):
        with open(config_path) as f:
            config = json.load(f)
    else:
        config = {}
        
    update_config(config_path, config, wheel_path)
    print(f"配置已更新: {config_path}")
    
    # 重启应用
    restart_claude()
    print("安装完成！")

if __name__ == '__main__':
    main() 