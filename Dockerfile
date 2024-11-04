# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Set environment variables for database configuration
# You can override these values in the Cloud Run configuration as well.
ENV PORT=8080

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
