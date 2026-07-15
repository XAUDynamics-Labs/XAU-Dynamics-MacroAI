# Use an official, highly optimized Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables to optimize Python for containerized environments
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies efficiently
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Run the AI engine as the main process
CMD ["python", "analyzer.py"]
