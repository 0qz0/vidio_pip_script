@echo off
chcp 65001 >nul
title 视频画中画工具

echo.
echo ========================================
echo           视频画中画工具
echo ========================================
echo.

echo 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python，请先安装Python 3.7+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python环境检查通过

echo.
echo 正在检查依赖包...
python -c "import selenium" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  正在安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 依赖包安装失败
        pause
        exit /b 1
    )
)

echo ✅ 依赖包检查通过

echo.
echo 正在启动图形界面...
python quick_start.py

if errorlevel 1 (
    echo.
    echo ❌ 程序运行出错
    pause
) 