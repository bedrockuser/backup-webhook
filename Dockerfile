# Use a lightweight base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Create app directory
WORKDIR /usr/src/app

# Copy app file
COPY app.py .

# Install dependencies
RUN pip install --no-cache-dir requests schedule

# Command to run the app
CMD ["python", "app.py"]
