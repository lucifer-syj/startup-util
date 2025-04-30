# 启动管理器 (Startup Manager)

一个现代风格的程序启动管理工具，可以管理和组织多个程序，支持预设快速启动。使用PyQt5构建的跨平台图形界面应用程序。

## 功能特点

- 美观的现代界面，支持深色和浅色主题切换
- 直观显示程序运行状态（实时监控）
- 支持创建程序组合预设，一键启动多个程序
- 可视化展示预设与程序的关联关系
- 使用标准JSON配置文件存储设置
- 支持添加/移除程序和预设
- 程序运行状态实时更新

## 安装说明

### 环境要求
- Python 3.6+
- PyQt5
- psutil

### 安装步骤
1. 克隆或下载本项目
2. 安装依赖:
   ```
   pip install -r requirements.txt
   ```
3. 运行程序:
   ```
   python run.py
   ```
   或直接双击 `启动管理器.bat` 文件(Windows)

### 作为Python包安装
你也可以将此项目作为Python包安装：
```
pip install -e .
```

安装后，你可以通过命令行直接启动：
```
startup-util
```

## 使用说明

1. **添加程序**: 点击"添加程序"按钮，选择可执行文件
2. **创建预设**: 点击"添加预设"按钮，输入预设名称
3. **关联程序与预设**: 在预设列下方点击关联按钮
4. **启动程序**: 点击程序行中的"启动"按钮
5. **启动预设**: 点击预设列顶部的"启动"按钮，一键启动关联的所有程序
6. **切换主题**: 点击顶部工具栏的"切换主题"按钮
7. **刷新状态**: 点击顶部工具栏的"刷新状态"按钮更新程序运行状态

## 配置文件格式

程序使用标准的JSON配置文件格式，所有配置存储在`appList.json`中：

```json
{
  "appList": [
    {
      "name": "记事本",
      "exe": "notepad.exe",
      "path": "C:/Windows/notepad.exe"
    },
    {
      "name": "计算器",
      "exe": "calc.exe",
      "path": "C:/Windows/System32/calc.exe"
    }
  ],
  "groupProgramList": [
    {
      "name": "办公工具",
      "key": "o",
      "apps": [
        "记事本",
        "计算器"
      ]
    }
  ]
}
```

## 项目文件结构

```
startup-util/
├── .git/                   # Git仓库
├── .gitignore              # Git忽略文件
├── LICENSE                 # 许可证文件
├── README.md               # 项目说明文档
├── CHANGELOG.md            # 更新日志
├── requirements.txt        # 项目依赖列表
├── setup.py                # 项目安装脚本
├── run.py                  # 项目运行入口
├── 启动管理器.bat          # Windows快捷启动脚本
├── docs/                   # 文档目录
│   ├── 使用指南.md         # 用户使用指南
│   └── 开发文档.md         # 开发文档
├── screenshots/            # 截图目录
└── src/                    # 源代码目录
    └── startup_util/       # 启动管理器包
        ├── __init__.py     # 包初始化文件
        ├── __main__.py     # 包入口点
        ├── startup_manager.pyw # 主程序文件
        ├── styles.py       # 界面样式定义
        ├── appList.json    # 配置文件
        └── build.py        # 打包脚本
```

## 开发者信息

### 修改界面样式
如需修改界面样式，请编辑`src/startup_util/styles.py`文件中的样式表定义。

### 添加新功能
主程序逻辑在`src/startup_util/startup_manager.pyw`文件中，遵循PyQt5的应用程序结构。

### 打包应用
要将应用打包为独立可执行文件，请使用：
```
cd src/startup_util
python build.py
```

### 依赖版本
- PyQt5 v5.15.6
- psutil v5.9.5

## 许可证

本项目采用MIT许可证 