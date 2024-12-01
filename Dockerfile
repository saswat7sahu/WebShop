# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies required for MySQL and building Python packages
RUN apt-get update && apt-get install -y \
    libmariadb-dev libmariadb-dev-compat gcc pkg-config libssl-dev --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
# Copy application files into the container
COPY . .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the Flask app will run on
EXPOSE 5000
# Define the default command to run the app
CMD ["sh", "-c", "python setup_db.py && gunicorn -w 4 -b 0.0.0.0:5000 app:app"]

