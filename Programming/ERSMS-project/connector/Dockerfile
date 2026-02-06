# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Install necessary OS packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the Python script, requirements, and constants.ini file into the container at /app
COPY Include/frontend_AI_connector.py /app/
COPY Include/requirements.txt /app/
COPY Include/init_scripts/constants.ini /app/init_scripts/
COPY Include/init_scripts/movies.csv /app/init_scripts/
# tls
# COPY ./certs/connector.crt /app/
# COPY ./certs/connector.key /app/

# Modify requirements.txt to use psycopg2-binary
RUN sed -i 's/psycopg2==2.9.9/psycopg2-binary==2.9.9/' requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run frontend_AI_connector.py when the container launches
CMD ["python", "./frontend_AI_connector.py"]