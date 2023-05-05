@echo off

set /p week="Please enter a week number (1-8): "
if "%week%" LSS "1" echo Invalid week number. Please try again. & exit /b 1
if "%week%" GTR "8" echo Invalid week number. Please try again. & exit /b 1
dir ..\CryCollege\week%week% /B | findstr /E ".py"
set /p class="Please enter a class name: "
if not exist ..\CryCollege\week%week%\%class% echo Invalid class name. Please try again. & exit /b 1
set current_dir=%cd%
python3 -m venv crycollege_env
call crycollege_env\Scripts\activate.bat
python3 -m pytest %current_dir%\..\CryCollege\week%week%\%class%