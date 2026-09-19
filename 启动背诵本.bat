@echo off
chcp 65001 >nul
cd /d "%~dp0背诵本"
echo Open http://127.0.0.1:8765 after server starts
py -3 server.py
if errorlevel 1 python server.py
pause
