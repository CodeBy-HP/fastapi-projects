@echo off
REM Quick start script for Book Management API (Windows CMD)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting Book Management API...
echo ================================================
echo.
echo Access the API at:
echo   - Swagger UI: http://localhost:8000/docs
echo   - ReDoc: http://localhost:8000/redoc
echo   - Health Check: http://localhost:8000/health
echo.
echo Press Ctrl+C to stop the server
echo ================================================
echo.

cd app
python main.py
