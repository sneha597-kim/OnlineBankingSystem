# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements if you have one in root
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose a port (change if needed)
EXPOSE 8080

# Default command — update this to your main app entry file
CMD ["python", "main.py"]
