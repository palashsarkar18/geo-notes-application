# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Run the application
CMD ["uvicorn", "geo_notes.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--reload"]
