# Dockerfile

# Start from a slim Python base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies required for psycopg2 (PostgreSQL driver)
RUN apt-get update \
    && apt-get -y install netcat-traditional \
    && apt-get -y install build-essential libpq-dev \
    && apt-get clean

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entrypoint script
COPY entrypoint.sh .
# Make the script executable
RUN chmod +x /app/entrypoint.sh

# Copy the rest of the application code into the container
COPY . .

# Set the entrypoint for the container
ENTRYPOINT ["/app/entrypoint.sh"]