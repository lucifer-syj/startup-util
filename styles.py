"""
存放应用样式的模块
"""
from PyQt5.QtGui import QPalette, QColor


# 暗色主题调色板
def dark_palette():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.Base, QColor(35, 35, 35))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
    palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QColor(35, 35, 35))
    
    # 设置禁用状态的颜色
    palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(127, 127, 127))
    palette.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 127, 127))
    palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127))
    
    return palette


# 暗色主题样式表
DARK_STYLESHEET = """
QMainWindow {
    background-color: #353535;
}
QGroupBox {
    border: 1px solid #5c5c5c;
    border-radius: 5px;
    margin-top: 10px;
    font-weight: bold;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 3px 0 3px;
}
QPushButton {
    background-color: #424242;
    border: 1px solid #5c5c5c;
    border-radius: 3px;
    padding: 1px 3px;
    color: white;
    min-width: 40px;
    max-width: 60px;
    min-height: 20px;
}
QPushButton:hover {
    background-color: #4f4f4f;
    border: 1px solid #7c7c7c;
}
QPushButton:pressed {
    background-color: #383838;
    border: 1px solid #7c7c7c;
}
QPushButton:disabled {
    background-color: #2d2d2d;
    border: 1px solid #3c3c3c;
    color: #787878;
}
QLabel {
    color: white;
}
QScrollArea {
    background-color: transparent;
    border: none;
}

/* 程序状态指示器样式 */
QLabel#status_indicator {
    border-radius: 8px;
    min-width: 16px;
    min-height: 16px;
    max-width: 16px;
    max-height: 16px;
}

/* 预设关联指示器样式 */
QFrame#connection_indicator {
    border-radius: 6px;
    min-width: 12px;
    min-height: 12px;
    max-width: 12px;
    max-height: 12px;
}

/* 启动中的程序行背景 */
QFrame#program_frame {
    border-radius: 3px;
    margin-top: 1px;
    margin-bottom: 1px;
    min-height: 36px;
}

/* 预设按钮样式 */
QPushButton#preset_button {
    background-color: #424242;
    color: white;
    border-radius: 3px;
    padding: 1px 3px;
    font-weight: bold;
    min-width: 40px;
    max-width: none;
    min-height: 22px;
    margin: 0px; /* 移除外边距 */
}
QPushButton#preset_button:hover {
    background-color: #4f4f4f;
    border: 1px solid #7c7c7c;
}
QPushButton#preset_button:pressed {
    background-color: #383838;
}
"""

# 亮色主题样式表
LIGHT_STYLESHEET = """
QMainWindow {
    background-color: #f5f5f5;
}
QGroupBox {
    border: 1px solid #c0c0c0;
    border-radius: 5px;
    margin-top: 10px;
    font-weight: bold;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 3px 0 3px;
}
QPushButton {
    background-color: #f0f0f0;
    border: 1px solid #c0c0c0;
    border-radius: 3px;
    padding: 1px 3px;
    color: #333333;
    min-width: 40px;
    max-width: 60px;
    min-height: 20px;
}
QPushButton:hover {
    background-color: #e0e0e0;
    border: 1px solid #a0a0a0;
}
QPushButton:pressed {
    background-color: #d0d0d0;
    border: 1px solid #a0a0a0;
}
QPushButton:disabled {
    background-color: #f5f5f5;
    border: 1px solid #d0d0d0;
    color: #a0a0a0;
}
QScrollArea {
    background-color: transparent;
    border: none;
}

/* 程序状态指示器样式 */
QLabel#status_indicator {
    border-radius: 8px;
    min-width: 16px;
    min-height: 16px;
    max-width: 16px;
    max-height: 16px;
}

/* 预设关联指示器样式 */
QFrame#connection_indicator {
    border-radius: 6px;
    min-width: 12px;
    min-height: 12px;
    max-width: 12px;
    max-height: 12px;
}

/* 启动中的程序行背景 */
QFrame#program_frame {
    border-radius: 3px;
    margin-top: 1px;
    margin-bottom: 1px;
    min-height: 36px;
}

/* 预设按钮样式 */
QPushButton#preset_button {
    background-color: #e0e0e0;
    color: #333333;
    border-radius: 3px;
    padding: 1px 3px;
    font-weight: bold;
    min-width: 40px;
    max-width: none;
    min-height: 22px;
    margin: 0px; /* 移除外边距 */
}
QPushButton#preset_button:hover {
    background-color: #d0d0d0;
    border: 1px solid #a0a0a0;
}
QPushButton#preset_button:pressed {
    background-color: #c0c0c0;
}
"""

# 运行状态指示器颜色
# 暗色主题
DARK_RUNNING_COLOR = "#5cb85c"     # 更柔和的绿色
DARK_NOT_RUNNING_COLOR = "#7f8c8d" # 灰色

# 亮色主题
LIGHT_RUNNING_COLOR = "#5cb85c"    # 相同的绿色但在亮色主题中
LIGHT_NOT_RUNNING_COLOR = "#bdc3c7" # 浅灰色

# 程序运行背景色
DARK_RUNNING_BG = "rgba(50, 120, 50, 30)"  # 更柔和的背景色
LIGHT_RUNNING_BG = "rgba(220, 255, 220, 80)" 

# 连接指示器颜色
DARK_CONNECTED_COLOR = "#3498db"   # 蓝色
DARK_NOT_CONNECTED_BORDER = "#7f8c8d" # 灰色边框

LIGHT_CONNECTED_COLOR = "#2980b9"  # 深蓝色
LIGHT_NOT_CONNECTED_BORDER = "#bdc3c7" # 浅灰色边框 