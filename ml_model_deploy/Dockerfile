FROM python:3.10-slim-buster

WORKDIR /ml_model_deploy

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Install PostgreSQL adapter
RUN apt-get update && \
    apt-get install -y gcc && \
    apt-get install -y postgresql && \
    apt-get install -y libpq-dev && \
    pip3 install psycopg2-binary
    
COPY . /ml_model_deploy

ENV PYTHONPATH /ml_model_deploy
CMD [ "python3", "app.py"]