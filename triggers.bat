@echo off
setlocal
cd /d "%APPDATA%\espanso\match"
if errorlevel 1 goto failed
python "%CD%\espanso-shortcuts.py"
if errorlevel 1 goto failed
echo.
echo Updated: "%CD%\espanso-shortcuts.md"
pause
exit /b 0
:failed
echo.
echo Update failed. Check the error above.
pause
exit /b 1
