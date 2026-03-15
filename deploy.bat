@echo off
REM Production deployment script for Windows
REM Run this script to deploy the backend to production

echo 🚀 Starting Varsity Backend Deployment

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Run database migrations
echo 🗄️ Running database migrations...
python -m alembic upgrade head

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  Warning: .env file not found. Please create one with production settings.
    echo    Copy from .env.production and update the values.
)

REM Start the server
echo 🌟 Starting server...
python run.py

pause