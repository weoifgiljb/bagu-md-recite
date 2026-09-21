@echo off
chcp 65001 >nul
cd /d "%~dp0"
py -3 build_graph.py
echo Open http://127.0.0.1:8766
py -3 -m http.server 8766
pause
