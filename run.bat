\
@echo off
cd /d "%~dp0"
title Customer Churn Analytics
set PYTHONDONTWRITEBYTECODE=1

where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found. Install Python 3.10 or newer from https://www.python.org/downloads/
  echo Tick "Add Python to PATH" during setup, then run this file again.
  pause
  exit /b 1
)

echo Installing required packages (first run may take a few minutes)...
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo Package installation failed. Check your internet connection and try again.
  pause
  exit /b 1
)

echo Starting the dashboard...
python -m streamlit run app.py
pause
