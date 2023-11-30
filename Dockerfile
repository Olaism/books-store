# Pull Base Image
FROM python:3.12.0-slim-bullseye

# Set environment variable
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set work directory
WORKDIR /code

# Copy requirement file
COPY requirements.txt .

# Install dependencies
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . .