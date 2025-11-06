# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependency list
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose the port for this service
EXPOSE 5002

# Command to run the Flask application
CMD ["python", "app.py"]
