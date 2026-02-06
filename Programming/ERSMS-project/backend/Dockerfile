# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Install necessary OS packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the Python script, requirements, and constants.ini file into the container at /app
COPY ./app.py /app/

COPY requirements.txt .
COPY .env .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run frontend_AI_connector.py when the container launches
CMD ["python", "./app.py"]