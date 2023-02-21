FROM python:3.10-slim-buster

WORKDIR /app

# Install Java and PySpark
RUN apt-get update && \
    apt-get install -y default-jre wget && \
    pip3 install pyspark


# Install PostgreSQL adapter
RUN apt-get update && \
    apt-get install -y gcc && \
    apt-get install -y postgresql && \
    apt-get install -y libpq-dev && \
    pip3 install psycopg2-binary

# Install PostgreSQL JDBC driver
RUN wget https://jdbc.postgresql.org/download/postgresql-42.3.1.jar -P /usr/local/lib/python3.10/site-packages/pyspark/jars/

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY transformation.py transformation.py

ENV PYTHONPATH /app
ENV PYSPARK_PYTHON python3
ENV PYSPARK_DRIVER_PYTHON python3
ENV SPARK_HOME /usr/local/lib/python3.10/site-packages/pyspark
CMD [ "python3","transformation.py"]