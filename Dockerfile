FROM python:3.9-slim

WORKDIR /app

# Copy requirements first
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install --no-cache-dir -e .

# Direct CMD - no script needed
CMD python -c "from http.server import HTTPServer, SimpleHTTPRequestHandler; HTTPServer(('0.0.0.0', 8080), SimpleHTTPRequestHandler).serve_forever()"