# Start Flask app in background

python app.py &

# Start Django app in foreground (this keeps the container running)
python hotel_reservation/hotelpredictor/manage.py runserver 0.0.0.0:8000