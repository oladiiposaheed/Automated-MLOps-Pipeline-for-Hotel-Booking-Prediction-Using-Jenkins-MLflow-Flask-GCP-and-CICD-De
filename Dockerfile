FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install --no-cache-dir -e .

COPY . .

CMD ["python", "app.py"]

# Use the CORRECT path - hotelpredictor is in root, not in hotel_reservations/
#CMD ["python", "hotelpredictor/manage.py", "runserver", "0.0.0.0:8080"]