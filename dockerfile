# Use a small Python base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install dependencies
# (requests is needed by the script)
RUN pip install --no-cache-dir requests

# Copy script into container
COPY jellysync.py .

# Run the script
CMD ["python", "-u", "jellysync.py"]
