FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY central_server/ .

EXPOSE 8080

CMD ["python", "app.py"]
