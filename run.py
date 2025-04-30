#!/usr/bin/env python
"""
启动管理器运行脚本
"""
import sys
import os
from pathlib import Path

# 重定向标准输出和标准错误（在无控制台环境中运行时防止错误）
if hasattr(sys, 'frozen'):
    # 如果是打包后的可执行文件
    log_path = os.path.join(os.path.expanduser("~"), "startup_util_log.txt")
    sys.stdout = open(log_path, "w", encoding="utf-8")
    sys.stderr = sys.stdout

# 将项目根目录添加到Python路径
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

from src.startup_util.startup_manager import StartupManager
from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("启动管理器")
    
    window = StartupManager()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # 确保异常被记录
        if hasattr(sys, 'frozen'):
            import traceback
            sys.stdout.write(f"错误: {str(e)}\n")
            sys.stdout.write(traceback.format_exc())
            sys.stdout.flush()
        raise 