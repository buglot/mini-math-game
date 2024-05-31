@ECHO OFF
if not defined PYTHON (set PYTHON=python)
if not defined VENV_DIR (set "VENV_DIR=%~dp0%env")


If Not Exist "%VENV_DIR%\Scripts\activate.bat" (
    for /f %%i in ('CALL %PYTHON% -c "import sys; print(sys.executable)"') do set FULL_PATH="%%i"

    echo Creating virtual environment
    !FULL_PATH! -m venv "%VENV_DIR%"
    echo:
)

echo Attempting to start venv
Call "%VENV_DIR%\Scripts\activate.bat"
echo:

echo Updating Pip
python -m pip install --upgrade pip
echo:

echo Installing / 
pip install -r requirement.txt
echo:

python app.py
pause