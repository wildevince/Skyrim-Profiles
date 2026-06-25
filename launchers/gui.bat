@echo off
call "%~dp0_env.bat"

where python3 >nul 2>&1
if %errorlevel%==0 (
    python3 "%SP_ROOT%\gui\app.py"
    goto :end
)

where python >nul 2>&1
if %errorlevel%==0 (
    python "%SP_ROOT%\gui\app.py"
    goto :end
)

echo.
echo Python introuvable. Installe Python depuis https://python.org
echo Cochez "Add Python to PATH" a l'installation.
pause
exit /b 1

:end
if errorlevel 1 pause
