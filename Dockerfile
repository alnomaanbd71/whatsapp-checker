# Use official Python image with Playwright dependencies pre-installed
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

# Set work directory
WORKDIR /app

# Copy all project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose the port for Render to detect
EXPOSE 5000

# Start the Flask app
CMD ["python", "main.py"]
