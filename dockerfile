# Use official python slim image
FROM python:3.11-slim


# Create app dir
WORKDIR /app


# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


# Copy app
COPY app.py ./
COPY templates ./templates
COPY static ./static


# Create data directory and make it writable by any UID (OpenShift runs with arbitrary UID)
RUN mkdir -p /data && chmod 0777 /data


# Expose expected port for OpenShift
EXPOSE 8080


# Use non-root user (but allow arbitrary UID). We keep root to set perms then drop to nobody.
USER 1001


# Start with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app", "--workers", "2"]