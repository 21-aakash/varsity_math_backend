#!/bin/bash
# Render deployment script for FastAPI

# Install dependencies
pip install -r requirements.txt

# Install gunicorn for production
pip install gunicorn

# Run database migrations
python -m alembic upgrade head

# Start the application with gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT