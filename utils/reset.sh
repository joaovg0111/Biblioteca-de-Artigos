# Stop the server if it's running

# Step 1: Delete the database file
rm db.sqlite3

# Step 2: Delete the old migration history
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

# Step 3: Recreate the migration files and the database
python manage.py makemigrations
python manage.py migrate
