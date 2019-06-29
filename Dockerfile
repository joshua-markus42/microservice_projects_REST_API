FROM python:3.6.8-alpine3.10
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

LABEL maintainer="Eugene"

CMD flask run --host=0.0.0.0 --port=5000