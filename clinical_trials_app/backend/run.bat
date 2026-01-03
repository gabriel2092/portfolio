@echo off
REM Start script for the backend server (Windows)

REM Activate virtual environment if it exists
IF EXIST venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Check if .env exists
IF NOT EXIST .env (
    echo Error: .env file not found!
    echo Please copy .env.example to .env and add your ANTHROPIC_API_KEY
    exit /b 1
)

echo Starting Clinical Trial Matcher API...
python main.py
