# Use a minimal Python image
FROM python:3.10-slim

# Set environment variables to prevent Python from writing .pyc files and buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Set the Flask environment variable to point to the app
ENV FLASK_APP=app:app

# Command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
