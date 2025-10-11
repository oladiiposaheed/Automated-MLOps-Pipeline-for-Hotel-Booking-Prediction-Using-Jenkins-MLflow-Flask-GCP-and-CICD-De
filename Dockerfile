FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# DEBUG: Find the exact path to manage.py
RUN echo "=== CURRENT DIRECTORY ===" && pwd
RUN echo "=== LIST ALL FILES ===" && ls -la
RUN echo "=== FIND manage.py FILE ===" && find . -name "manage.py" -type f
RUN echo "=== LIST hotel* directories ===" && find . -name "hotel*" -type d

RUN pip install --no-cache-dir -e .

# Simple server for now
CMD ["python", "-m", "http.server", "8080", "--bind", "0.0.0.0"]