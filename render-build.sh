#!/bin/bash
# Render deployment script

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python -m alembic upgrade head

# Start the application
python run.py