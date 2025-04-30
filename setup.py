from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="startup-util",
    version="1.0.0",
    author="Lucifer-SYJ",
    author_email="547413892@qq.com",
    description="一个Windows启动管理工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lucifer-syj/startup-util",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    package_data={
        "startup_util": ["appList.json"],
    },
    entry_points={
        "console_scripts": [
            "startup-util=startup_util.__main__:main",
        ],
    },
) 