#!/bin/bash
# Test PostgreSQL connection and run migrations

echo "🧪 Testing database connection..."

# Test database connection
python -c "
import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine

async def test_connection():
    database_url = os.getenv('DATABASE_URL', 'sqlite+aiosqlite:///./varsity.db')
    print(f'🔗 Connecting to: {database_url}')

    try:
        engine = create_async_engine(database_url, echo=False)
        async with engine.begin() as conn:
            result = await conn.execute('SELECT 1')
            print('✅ Database connection successful!')
        await engine.dispose()
    except Exception as e:
        print(f'❌ Database connection failed: {e}')
        exit(1)

asyncio.run(test_connection())
"

if [ $? -eq 0 ]; then
    echo "🗄️ Running database migrations..."
    python -m alembic upgrade head
    echo "✅ Migrations completed!"
else
    echo "❌ Database connection test failed. Please check your DATABASE_URL."
    exit 1
fi