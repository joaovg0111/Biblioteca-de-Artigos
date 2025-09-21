#!/bin/bash
set -e

# Stop the server if it's running
echo "🚀 Starting database and media reset..."

# Step 1: Delete the database file
echo "🗑️ Deleting database file (db.sqlite3)..."
rm -f db.sqlite3

# Step 2: Delete uploaded article files
echo "🗑️ Deleting uploaded article files in media/articles/..."
if [ -d "media/articles" ]; then
    find media/articles -mindepth 1 -delete
fi

# Step 3: Delete the old migration history
echo "🗑️ Deleting old migration files..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

# Step 4: Recreate the migration files and the database
echo "✨ Creating new migrations..."
python manage.py makemigrations
echo "Applying new migrations..."
python manage.py migrate

echo "✅ Reset complete! You can now run the server."
