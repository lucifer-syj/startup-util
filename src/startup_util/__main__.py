#!/usr/bin/env python
"""
启动管理器的主入口点
"""
import sys
import os
from PyQt5.QtWidgets import QApplication
from pathlib import Path

# 确保可以正确导入模块
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

# 使用绝对导入
from src.startup_util.startup_manager import StartupManager

def main():
    """主函数，启动应用程序"""
    app = QApplication(sys.argv)
    app.setApplicationName("启动管理器")
    
    window = StartupManager()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 