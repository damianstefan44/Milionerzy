@echo off

:: Install the requirements from requirements.txt
IF EXIST requirements.txt (
    echo Installing requirements from requirements.txt...
    python3 -m pip install -r requirements.txt
) ELSE (
    echo requirements.txt not found. Please make sure it exists in the same directory as this script.
    pause
    exit /b
)

echo Installation complete.
pause