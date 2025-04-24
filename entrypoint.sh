#!/bin/bash

# Wait for database to be ready
echo "Waiting for PostgreSQL..."

while ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER > /dev/null 2> /dev/null; do
  echo "Waiting for database connection..."
  sleep 2
done

echo "PostgreSQL started"

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Create superuser if not exists
echo "Setting up admin user..."
python manage.py seed_data

# Start server
echo "Starting server..."
exec "$@"