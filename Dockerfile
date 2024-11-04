# Use a minimal Python image
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc && \
    pip install flask plotly pandas psycopg2-binary

COPY . /app

EXPOSE 8080

CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
