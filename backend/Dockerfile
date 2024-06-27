# Use the latest Bitnami Python image as the base image.
FROM bitnami/python:latest

# Set the working directory to /backend.
WORKDIR /backend

# Environment variable to prevent Python from writing .pyc files to disk.
ENV PYTHONDONTWRITEBYTECODE 1

# Environment variable to ensure stdout and stderr are unbuffered.
ENV PYTHONUNBUFFERED 1

# Environment variable to specify the Flask application entry point.
ENV FLASK_APP=run.py

# Environment variable to set the host for Flask to listen on all interfaces.
ENV FLASK_RUN_HOST=0.0.0.0

# Copy the requirements.txt file into the container at /backend.
COPY ./requirements.txt ./requirements.txt

# Install the Python dependencies from the requirements.txt file without using cache.
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# Copy all the files from the current directory into the container at /backend.
COPY . .

# Set the default command to run the Flask application.
CMD ["flask", "run"]
