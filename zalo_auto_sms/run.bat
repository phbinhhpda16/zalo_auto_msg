@echo off
cd /d "%~dp0"
echo Running main.py...
python main.py
if %ERRORLEVEL% neq 0 (
    echo Error occurred while running the script. Check the log file for details.
    pause
)
