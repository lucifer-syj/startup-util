import os
import sys
import json
import psutil
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QScrollArea, 
                            QFileDialog, QMessageBox, QGroupBox, QFrame,
                            QStyleFactory)
from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtGui import QFont, QIcon

# 从同一包中导入styles模块
from . import styles


class StartupManager(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.programs = []
        self.presets = []
        self.connections = []
        self.processes = {}
        self.running_processes = set()
        self.preset_button_width = 50  # 添加默认预设按钮宽度
        
        self.app = QApplication.instance()
        self.initUI()
        
        # 获取当前模块所在目录，加载配置文件
        module_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(module_dir, 'appList.json')
        self.loadAppListJson(config_path)
        
        self.checkRunningProcesses()
        
    def initUI(self):
        self.setWindowTitle('启动管理器')
        
        # 获取屏幕分辨率
        desktop = QApplication.desktop()
        screen_rect = desktop.screenGeometry()
        screen_width, screen_height = screen_rect.width(), screen_rect.height()
        
        # 设置窗口位置贴近屏幕右下方
        window_width = 600
        window_height = 800  # 修改为800px
        
        # 计算位置：距离右侧20%屏幕宽度，距离底部10%屏幕高度
        x_position = screen_width - window_width - int(screen_width * 0.2)
        y_position = screen_height - window_height - int(screen_height * 0.1)
        
        # 设置窗口位置和大小
        self.setGeometry(x_position, y_position, window_width, window_height)
        
        # 设置应用样式为Fusion
        self.app.setStyle(QStyleFactory.create('Fusion'))
        
        # 应用暗色主题
        self.applyDarkTheme()
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(5)
        
        # 顶部工具栏
        toolbar = QHBoxLayout()
        refresh_btn = QPushButton('刷新状态')
        refresh_btn.setIcon(QIcon.fromTheme('view-refresh'))
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.clicked.connect(self.checkRunningProcesses)
        
        theme_btn = QPushButton('切换主题')
        theme_btn.setIcon(QIcon.fromTheme('preferences-desktop-theme'))
        theme_btn.setCursor(Qt.PointingHandCursor)
        theme_btn.clicked.connect(self.toggleTheme)
        
        toolbar.addWidget(refresh_btn)
        toolbar.addWidget(theme_btn)
        toolbar.addStretch()
        
        main_layout.addLayout(toolbar)
        
        # 创建滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        main_layout.addWidget(scroll)
        
        # 滚动区域的内容部件
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(5)
        scroll.setWidget(self.content_widget)
        
        # 程序列表组
        group_box = QGroupBox("程序和预设")
        group_box.setFlat(True)
        self.program_layout = QVBoxLayout()
        self.program_layout.setContentsMargins(5, 10, 5, 5)
        self.program_layout.setSpacing(4)  # 设置固定的行间距为4px
        group_box.setLayout(self.program_layout)
        self.content_layout.addWidget(group_box)
        
        self.statusBar().showMessage('就绪')
        self.is_dark_theme = True
    
    def applyDarkTheme(self):
        self.app.setPalette(styles.dark_palette())
        self.app.setStyleSheet(styles.DARK_STYLESHEET)
        self.is_dark_theme = True
    
    def applyLightTheme(self):
        self.app.setPalette(QApplication.style().standardPalette())
        self.app.setStyleSheet(styles.LIGHT_STYLESHEET)
        self.is_dark_theme = False
    
    def toggleTheme(self):
        if self.is_dark_theme:
            self.applyLightTheme()
        else:
            self.applyDarkTheme()
        self.updateUI()

    def loadAppListJson(self, filename):
        """加载appList.json格式的配置文件"""
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # 清空现有数据
                    self.programs = []
                    self.presets = []
                    self.connections = []
                    
                    # 加载程序列表
                    app_dict = {}  # 用于快速查找程序
                    if 'appList' in data:
                        for app in data['appList']:
                            program = {
                                'name': app['name'],
                                'path': app['path'],
                                'exe': app.get('exe', os.path.basename(app['path']))
                            }
                            self.programs.append(program)
                            app_dict[app['name']] = len(self.programs) - 1
                    
                    # 加载预设组
                    if 'groupProgramList' in data:
                        for idx, group in enumerate(data['groupProgramList']):
                            preset = {
                                'name': group['name'],
                                'programs': []
                            }
                            self.presets.append(preset)
                            
                            # 添加连接和程序路径
                            for app_name in group['apps']:
                                if app_name in app_dict:
                                    program_idx = app_dict[app_name]
                                    program_path = self.programs[program_idx]['path']
                                    
                                    self.connections.append({
                                        'program_index': program_idx,
                                        'preset_index': idx
                                    })
                                    
                                    preset['programs'].append(program_path)
                    
                    self.updateUI()
                    self.statusBar().showMessage(f'已加载appList配置: {filename}')
            except Exception as e:
                QMessageBox.critical(self, "错误", f"加载appList配置失败: {str(e)}")
                print(f"错误详情: {str(e)}")
    
    def checkRunningProcesses(self):
        """检查程序是否正在运行"""
        self.running_processes.clear()
        
        # 获取所有运行进程的信息
        running_procs = {}
        running_paths = set()
        
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                proc_info = proc.info
                proc_name = proc_info['name'].lower()
                self.running_processes.add(proc_name)
                
                # 保存进程路径信息
                if proc_info['exe']:
                    running_paths.add(proc_info['exe'].lower())
                    running_procs[proc_name] = proc_info
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        # 调试输出所有可检测到的进程名
        process_debug = ", ".join(sorted(list(self.running_processes)))
        print(f"检测到的进程: {process_debug}")
                
        self.updateUI()
        self.statusBar().showMessage('已刷新程序运行状态')
    
    def isAppRunning(self, program):
        """检查应用是否正在运行，使用多种方法检测"""
        exe_name = program.get('exe', '').lower()
        path = program.get('path', '').lower()
        base_name = os.path.basename(path).lower()
        
        # 1. 通过exe名称匹配
        if exe_name in self.running_processes:
            return True
            
        # 2. 通过可执行文件名匹配
        if base_name in self.running_processes:
            return True
            
        # 3. 一些特殊情况的处理（如腾讯元宝）
        if program.get('name') == '腾讯元宝' and 'yuanbao.exe' in self.running_processes:
            return True
            
        return False
    
    def createAppRow(self, i, program, preset_count):
        # 创建程序行容器框架
        program_frame = QFrame()
        program_frame.setObjectName("program_frame")
        program_frame.setFrameShape(QFrame.StyledPanel)
        program_frame.setFixedHeight(36)
        
        # 检查程序是否正在运行
        is_running = self.isAppRunning(program)
        
        # 设置运行中程序的背景色
        if is_running:
            if self.is_dark_theme:
                program_frame.setStyleSheet(f"QFrame#program_frame {{ background-color: {styles.DARK_RUNNING_BG}; }}")
            else:
                program_frame.setStyleSheet(f"QFrame#program_frame {{ background-color: {styles.LIGHT_RUNNING_BG}; }}")
        
        row = QHBoxLayout(program_frame)
        row.setContentsMargins(5, 3, 5, 3)
        row.setSpacing(2)  # 减小间距，与标题一致
        
        # 程序名称部分(固定宽度240px)
        program_name_widget = QWidget()
        program_name_widget.setFixedWidth(240)
        program_name_layout = QHBoxLayout(program_name_widget)
        program_name_layout.setContentsMargins(5, 0, 0, 0)
        program_name_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        # 程序状态指示器
        status_indicator = QLabel()
        status_indicator.setObjectName("status_indicator")
        status_indicator.setFixedSize(14, 14)
        
        if is_running:
            if self.is_dark_theme:
                status_indicator.setStyleSheet(f"background-color: {styles.DARK_RUNNING_COLOR};")
            else:
                status_indicator.setStyleSheet(f"background-color: {styles.LIGHT_RUNNING_COLOR};")
        else:
            if self.is_dark_theme:
                status_indicator.setStyleSheet(f"background-color: {styles.DARK_NOT_RUNNING_COLOR};")
            else:
                status_indicator.setStyleSheet(f"background-color: {styles.LIGHT_NOT_RUNNING_COLOR};")
        
        # 设置程序名标签
        label = QLabel(program['name'])
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        if is_running:
            font = QFont()
            font.setBold(True)
            label.setFont(font)
        
        program_name_layout.addWidget(status_indicator)
        program_name_layout.addWidget(label)
        
        row.addWidget(program_name_widget)
        
        # 程序状态部分(固定宽度60px)
        status_widget = QWidget()
        status_widget.setFixedWidth(60)
        status_layout = QHBoxLayout(status_widget)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setAlignment(Qt.AlignCenter)
        
        start_btn = QPushButton("启动")
        if is_running:
            start_btn.setEnabled(False)
            start_btn.setText("已运行")
        start_btn.setCursor(Qt.PointingHandCursor)
        start_btn.clicked.connect(lambda checked, p=program: self.startProgram(p))
        start_btn.setFixedWidth(55)  # 设置按钮固定宽度以适应60px容器
        
        status_layout.addWidget(start_btn)
        row.addWidget(status_widget)
        
        # 为每个预设添加关联指示器(平分剩余宽度)
        for j, preset in enumerate(self.presets):
            # 勾选标记直接添加到行布局中，与表头预设按钮对齐
            is_connected = any(conn['program_index'] == i and conn['preset_index'] == j for conn in self.connections)
            check_label = QLabel("✓" if is_connected else "")
            check_label.setAlignment(Qt.AlignCenter)
            check_label.setFixedWidth(self.preset_button_width)
            
            if is_connected:
                if self.is_dark_theme:
                    check_label.setStyleSheet("color: #3498db; font-weight: bold; font-size: 14px;")
                else:
                    check_label.setStyleSheet("color: #2980b9; font-weight: bold; font-size: 14px;")
            
            row.addWidget(check_label)
        
        return program_frame
    
    def updateUI(self):
        # 清除当前布局
        while self.program_layout.count():
            item = self.program_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                while item.layout().count():
                    sub_item = item.layout().takeAt(0)
                    if sub_item.widget():
                        sub_item.widget().deleteLater()
        
        # 获取窗口宽度用于计算
        window_width = self.width()
        
        # 计算预设按钮宽度（确保最小为30px）
        preset_count = len(self.presets)
        remaining_width = window_width - 300 - 20  # 减去程序标题宽度和左右边距
        self.preset_button_width = max(30, min(50, remaining_width // max(1, preset_count)))  # 限制最小宽度为30px，最大为50px
        
        # 创建表头
        header = QHBoxLayout()
        header.setContentsMargins(5, 2, 5, 2)
        header.setSpacing(2)  # 设置较小的间距
        
        # 程序标题列(固定宽度300px)
        program_header = QLabel("程序")
        program_header.setFont(QFont("Arial", 9, QFont.Bold))
        program_header.setAlignment(Qt.AlignCenter)
        program_header.setFixedWidth(300)
        header.addWidget(program_header)
        
        # 预设标题按钮(平分剩余宽度)
        for i, preset in enumerate(self.presets):
            preset_btn = QPushButton(preset['name'])
            preset_btn.setObjectName("preset_button")
            preset_btn.setCursor(Qt.PointingHandCursor)
            preset_btn.setFixedWidth(self.preset_button_width)
            preset_btn.clicked.connect(lambda checked, idx=i: self.startPreset(idx))
            header.addWidget(preset_btn)
            
        self.program_layout.addLayout(header)
        
        # 添加分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.program_layout.addWidget(line)
        
        # 为每个程序创建一行
        for i, program in enumerate(self.programs):
            program_frame = self.createAppRow(i, program, preset_count)
            self.program_layout.addWidget(program_frame)
    
    def startProgram(self, program):
        try:
            # 使用独立进程方式启动程序，与Python进程分离
            if sys.platform == 'win32':
                # Windows平台使用startfile方式启动，完全独立
                os.startfile(program['path'])
            else:
                # 其他平台使用subprocess，指定nohup并分离进程
                import subprocess
                subprocess.Popen(['nohup', program['path']], 
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL,
                                preexec_fn=os.setpgrp if hasattr(os, 'setpgrp') else None)
                
            self.statusBar().showMessage(f"已启动程序: {program['name']}")
            
            # 短暂延迟后刷新状态
            QApplication.processEvents()
            time.sleep(0.5)
            self.checkRunningProcesses()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"启动程序失败: {str(e)}")
    
    def startPreset(self, preset_index):
        preset = self.presets[preset_index]
        started_count = 0
        
        for program_path in preset['programs']:
            try:
                # 查找程序信息并检查是否已运行
                for program in self.programs:
                    if program['path'] == program_path:
                        # 使用新的检测方法
                        if self.isAppRunning(program):
                            continue
                        
                        # 使用独立进程方式启动
                        if sys.platform == 'win32':
                            os.startfile(program_path)
                        else:
                            import subprocess
                            subprocess.Popen(['nohup', program_path], 
                                            stdout=subprocess.DEVNULL,
                                            stderr=subprocess.DEVNULL,
                                            preexec_fn=os.setpgrp if hasattr(os, 'setpgrp') else None)
                        
                        started_count += 1
                        break
            except Exception as e:
                QMessageBox.warning(self, "警告", f"启动程序失败: {program_path}, 错误: {str(e)}")
        
        self.statusBar().showMessage(f"已启动预设: {preset['name']} ({started_count} 个程序)")
        
        # 短暂延迟后刷新状态
        QApplication.processEvents()
        time.sleep(0.5)
        self.checkRunningProcesses()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StartupManager()
    window.show()
    sys.exit(app.exec_()) 