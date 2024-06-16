# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app2
WORKDIR /app2

# Install necessary OS packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the Python script, requirements, and datasets into the container at /app2
COPY movie_recommender.py .
COPY datasets/tmdb_5000_credits.csv ./movie_recommendations/datasets/
COPY datasets/tmdb_5000_movies.csv ./movie_recommendations/datasets/
COPY init_scripts/constants.ini ./init_scripts/constants.ini

# Install any needed packages specified in requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install requests

# Run frontend_AI_connector.py when the container launches
CMD ["python", "./movie_recommender.py"]