FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install --no-cache-dir -e .

# Use the CORRECT directory name (hotel_reservations, not hotel_reservation)
RUN cd hotel_reservations/hotelpredictor && python manage.py check

CMD ["python", "hotel_reservations/hotelpredictor/manage.py", "runserver", "0.0.0.0:8080"]