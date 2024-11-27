FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Run the server (or Gunicorn, for production use)
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
