# Start Flask app in background

# python app.py &

# # Start Django app in foreground (this keeps the container running)
# python hotel_reservation/hotelpredictor/manage.py runserver 0.0.0.0:8000


# Cloud Run
PORT=${PORT:-8080}

echo "Starting Django application on port: $PORT"

exec python hotel_reservation/hotelpredictor/manage.py runserver 0.0.0.0:$PORT