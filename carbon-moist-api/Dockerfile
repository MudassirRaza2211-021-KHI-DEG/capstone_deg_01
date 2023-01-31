FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY carbon_moist_data_extract_app.py carbon_moist_data_extract_app.py

ENV PYTHONPATH /app
CMD [ "python3", "carbon_moist_data_extract_app.py"]
