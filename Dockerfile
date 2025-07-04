FROM python:3.12-slim


RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY . .


RUN mkdir -p videos thumbnails


EXPOSE 8000


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 