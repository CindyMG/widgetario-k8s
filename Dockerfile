# Start from official Python slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy everything into container
COPY . /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install sqlite dependencies
RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev

# Expose port for FastAPI
EXPOSE 8000

# Run the app (correct import path)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
