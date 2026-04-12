@echo off
cls
title Josia Project Manager - Install Requirements
color 0A

echo ======================================================
echo          Josia Project Manager - Auto Setup
echo ======================================================
echo  1. Download Python 3.13 (64-bit)
echo  2. Silent Install Python
echo  3. Configure Environment Variables
echo  4. Install Dependencies From requirements.txt
echo ======================================================
echo.

echo [1/4] Downloading Python 3.13.1...
curl -L -o python-installer.exe https://mirrors.huaweicloud.com/python/3.13.1/python-3.13.1-amd64.exe

echo [2/4] Installing Python...
python-installer.exe /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
del python-installer.exe

echo [3/4] Configuring Environment Variables...
set "PY_PATH=C:\Users\%username%\AppData\Local\Programs\Python\Python313"
set "PATH=%PY_PATH%;%PY_PATH%\Scripts;%PATH%"
echo Configuration completed.

echo [4/4] Installing Dependencies from requirements.txt...
"%PY_PATH%\python.exe" -m pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
"%PY_PATH%\python.exe" -m pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

echo.
echo ======================================================
echo  All dependencies installed successfully!
echo  You can now run EXE or main.py
echo ======================================================
echo.
pause
exit
