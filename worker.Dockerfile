FROM python:latest

WORKDIR /usr/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY /../.env .
COPY requirements.txt .
COPY /backend/config.py .
COPY /backend /usr/src/backend

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PYTHONPATH /usr/src/backend