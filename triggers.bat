@echo off
setlocal
python "%~dp0espanso-shortcuts.py" --match-dir "%APPDATA%\espanso\match"
if errorlevel 1 goto failed
echo.
echo Updated: "%APPDATA%\espanso\match\espanso-shortcuts.md"
pause
exit /b 0
:failed
echo.
echo Update failed. Check the error above. Install dependencies with: python -m pip install -r "%~dp0requirements.txt"
pause
exit /b 1
