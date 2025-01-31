FROM python:3.11-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# RUN apt-get update && apt-get install -y \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create directories for static and media files
RUN mkdir -p /app/staticfiles /app/mediafiles

# Collect static files if RUN_COLLECTSTATIC is true
RUN if [ "$RUN_COLLECTSTATIC" = "true" ]; then \
    python manage.py collectstatic --noinput; \
    fi

# Set permissions for static and media directories
RUN chmod -R 755 /app/staticfiles /app/mediafiles

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
