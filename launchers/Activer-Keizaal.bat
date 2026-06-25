@echo off
call "%~dp0_env.bat"
powershell -NoProfile -ExecutionPolicy Bypass -File "%SP_ROOT%\scripts\Switch-SkyrimProfile.ps1" -Profile Keizaal
if errorlevel 1 pause
