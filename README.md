# Varsity Website Backend

This is the FastAPI backend for the Varsity Website.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up PostgreSQL database and update the DATABASE_URL in `app/config/database.py`.

3. Run migrations:
   ```bash
   alembic upgrade head
   ```

4. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

Once the server is running, visit `http://localhost:8000/docs` for the interactive API documentation.

## Features

- User authentication and authorization
- Course management
- Assignments
- Study materials
- Quizzes