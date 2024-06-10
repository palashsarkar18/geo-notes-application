# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY ../backend/requirements.txt /workspace/backend/

# Install Python dependencies
RUN pip install --no-cache-dir -r /workspace/backend/requirements.txt

# Copy the backend code
COPY ../backend /workspace/backend

# Install Node.js dependencies
COPY ../frontend/package.json ../frontend/package-lock.json /workspace/frontend/
WORKDIR /workspace/frontend
RUN npm install

# Return to the backend working directory
WORKDIR /workspace/backend
