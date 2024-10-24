# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create input and output folders in the container
RUN mkdir -p /app/input_folder /app/output_folder

# Expose the volume for input and output folders
VOLUME ["/app/input_folder", "/app/output_folder"]

# Command to run the Python script
CMD ["python", "main.py"]
