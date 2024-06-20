# Dockerfile
FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY config.yaml .

CMD ["streamlit", "run", "app.py"]