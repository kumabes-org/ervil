FROM python:3.10-slim

LABEL maintainer Rodrigo Kumabe <rodrigo.kumabe@gmail.com>

WORKDIR /app

COPY . /app/

RUN pip3 install -r requirements.txt

CMD python3 src/app.py