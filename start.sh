#!/bin/bash

set -e  # Exit on any error

echo "🚀 Starting deployment process..."

# Wait for database to be ready
echo "⏳ Waiting for database connection..."
python -c "
import time
import sys
from app.config import settings
from sqlalchemy import create_engine, text

max_attempts = 30
for attempt in range(max_attempts):
    try:
        engine = create_engine(settings.database_url)
        with engine.connect() as conn:
            conn.execute(text('SELECT 1'))
        print('✅ Database connection successful')
        break
    except Exception as e:
        if attempt == max_attempts - 1:
            print(f'❌ Failed to connect to database after {max_attempts} attempts: {e}')
            sys.exit(1)
        print(f'⏳ Database not ready (attempt {attempt + 1}/{max_attempts}), waiting...')
        time.sleep(2)
"

# Run database migrations
echo "📦 Running database migrations..."
alembic upgrade head

if [ $? -eq 0 ]; then
    echo "✅ Migrations completed successfully"
else
    echo "❌ Migration failed"
    exit 1
fi

# Start the FastAPI application
echo "🚀 Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080} --workers 1