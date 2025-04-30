#!/usr/bin/env python
"""
启动管理器运行脚本
"""
import sys
import os
from pathlib import Path

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
    main() 