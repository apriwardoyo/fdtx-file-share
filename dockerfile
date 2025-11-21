FROM python:3.11-slim

WORKDIR /app

# install Flask
RUN pip install flask

COPY app.py /app/

# buat folder /data untuk PVC mount point
RUN mkdir -p /data && chmod -R 777 /data

EXPOSE 8080

CMD ["python", "app.py"]
