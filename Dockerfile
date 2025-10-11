FROM python:3.9-slim

WORKDIR /app

# Copy requirements first
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install --no-cache-dir -e .

# Start Django
CMD ["python", "hotel_reservation/hotelpredictor/manage.py", "runserver", "0.0.0.0:8080"]