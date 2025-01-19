FROM python:3.9-slim-buster

WORKDIR /app

RUN apt update

RUN pip3 install --upgrade pip

COPY requirements.txt .
COPY server.py .

RUN pip3 install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/

CMD ["python3", "./server.py"]