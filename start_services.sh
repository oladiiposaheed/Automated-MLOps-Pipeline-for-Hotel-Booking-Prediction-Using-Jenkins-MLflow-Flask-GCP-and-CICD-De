PORT=${PORT:-8080}

echo "Starting Django application on port: $PORT"

# Change to Django project directory
cd hotel_reservation/hotelpredictor

# Start Django development server
exec python manage.py runserver 0.0.0.0:$PORT