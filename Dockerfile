# Use a minimal Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080", "--app=app:app"]
