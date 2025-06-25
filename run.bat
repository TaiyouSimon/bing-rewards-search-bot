@echo off
title Bing Rewards Automator

echo.
echo [LAUNCHER] Installing/Verifying required Python packages...
pip install -r requirements.txt

timeout /t 2 >nul

cls

echo [LAUNCHER] Starting the Bing Rewards Automator...
echo.
python auto_bing_search.py

echo.
echo [LAUNCHER] Script has finished.
pause