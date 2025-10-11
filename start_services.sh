# Start Flask app in background

# python app.py &

# # Start Django app in foreground (this keeps the container running)
# python hotel_reservation/hotelpredictor/manage.py runserver 0.0.0.0:8000


# # Cloud Run
# PORT=${PORT:-8080}

# echo "Starting Django application on port: $PORT"

# exec python hotel_reservation/hotelpredictor/manage.py runserver 0.0.0.0:$PORT

#!/bin/bash

PORT=${PORT:-8080}

echo "=== Container Startup Debug ==="
echo "PORT: $PORT"
echo "Working directory: $(pwd)"
echo "Directory contents:"
ls -la
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"

# Check if Django files exist
echo "=== Checking Django files ==="
ls -la hotel_reservation/hotelpredictor/
echo "Manage.py exists: $(test -f hotel_reservation/hotelpredictor/manage.py && echo 'YES' || echo 'NO')"

# Test Django configuration
echo "=== Testing Django setup ==="
python hotel_reservation/hotelpredictor/manage.py check --fail-level WARNING

echo "=== Starting Django on port: $PORT ==="
exec python hotel_reservation/hotelpredictor/manage.py runserver 0.0.0.0:$PORT