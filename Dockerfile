FROM python:3-alpine

RUN mkdir /service
WORKDIR /service
COPY . /service
RUN pip install -r requirements.txt

