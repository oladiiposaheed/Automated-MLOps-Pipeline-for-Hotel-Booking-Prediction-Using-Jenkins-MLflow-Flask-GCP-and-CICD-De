FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install --no-cache-dir -e .

# Test if Django works at build time
RUN cd hotel_reservation/hotelpredictor && python manage.py check

# Simple Django startup
CMD ["python", "hotel_reservation/hotelpredictor/manage.py", "runserver", "0.0.0.0:8080"]