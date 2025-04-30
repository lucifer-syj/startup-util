"""
启动管理器打包脚本
使用PyInstaller将程序打包为独立可执行文件
"""
import os
import PyInstaller.__main__

# 确保工作目录正确
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# 定义图标文件路径（如果存在）
icon_path = 'icon.ico' if os.path.exists('icon.ico') else None

# 构建PyInstaller命令参数
args = [
    'startup_manager.pyw',
    '--name=启动管理器',
    '--windowed',
    '--onefile',
    '--add-data=styles.py;.',
    '--add-data=appList.json;.',
]

# 如果有图标文件，添加图标参数
if icon_path:
    args.append(f'--icon={icon_path}')

# 执行打包命令
print("开始打包启动管理器...")
PyInstaller.__main__.run(args)
print("打包完成！输出文件位于 dist/启动管理器.exe") 