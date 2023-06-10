FROM python:3.10-slim-buster

ENV PYTHONBUFFERED=1

WORKDIR /store

RUN mkdir /store/static && mkdir /store/media

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt