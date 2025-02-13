# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Varsayılan olarak google modunu çalıştırır. (Parametreleri ihtiyaca göre değiştirebilirsiniz)
CMD ["python", "main.py", "--mode", "google", "--query", "latest+news"]
