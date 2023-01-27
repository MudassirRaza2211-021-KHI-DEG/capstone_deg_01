FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY positive.csv positive.csv
COPY negative.csv negative.csv
COPY sensorsmock sensorsmock

ENV PYTHONPATH /app

CMD [ "python3", "sensorsmock/app.py"]
