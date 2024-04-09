# Dockerfile

# Use the official Python image
FROM python:3.11

# Set environment variables
ENV POETRY_VERSION=1.1.10 \
    POETRY_HOME="/opt/poetry" \
    PATH="/opt/poetry/bin:$PATH"

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy only the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock /code/

# Set the working directory
WORKDIR /code

# Install dependencies using Poetry
RUN poetry install --no-root --no-interaction --no-ansi

# Copy the rest of the application code
COPY . /code

# Expose port 8000
EXPOSE 8000

# Define the command to run the application
CMD . ./setup-populate.sh; poetry run python manage.py runserver 0.0.0.0:8000
