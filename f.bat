@echo off
setlocal

REM Switch to this repository root (folder where this script lives)
cd /d "%~dp0%"

REM This batch file is a simple wrapper to execute the fetch-genesis.py Python script.
REM It passes all command-line arguments to the Python script.

echo Calling the Python script to fetch genesis...

REM Check if a virtual environment exists and activate it.
set "VENV_PYTHON=.venv\Scripts\python.exe"
if exist "%VENV_PYTHON%" (
    echo Found virtual environment. Using its Python interpreter.
    "%VENV_PYTHON%" "scripts\fetch-genesis.py" %*
) else (
    echo No virtual environment found. Using default 'python' from PATH.
    python "scripts\fetch-genesis.py" %*
)

echo.
echo Done.

endlocal
