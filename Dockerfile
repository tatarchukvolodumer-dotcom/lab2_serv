FROM python:3.11-slim

WORKDIR /app

# Вимикаємо буферизацію логів та генерацію .pyc файлів
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

EXPOSE 8080

# Запускаємо через Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]