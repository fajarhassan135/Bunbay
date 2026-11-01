@echo off
cd /d "%~dp0"
py serve_bunbay.py
if errorlevel 1 python serve_bunbay.py
pause