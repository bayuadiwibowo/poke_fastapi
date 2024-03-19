FROM python:3.9-slim-bullseye

RUN apt update

RUN apt install build-essential -y

RUN mkdir /root/app

COPY . /root/app

WORKDIR /root/app

RUN pip install --upgrade pip

RUN pip install .
