# Use Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port for this service
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
