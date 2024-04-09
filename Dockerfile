# Dockerfile

# Use the official Python image
FROM python:3.11

# Set environment variables
ENV POETRY_VERSION=1.8.2 \
    POETRY_HOME="/opt/poetry" \
    PATH="/opt/poetry/bin:$PATH"

# Install dependencies
RUN DEBIAN_FRONTEND=noninteractive \
  apt-get update \
  && apt-get install -y python3 \
  && rm -rf /var/lib/apt/lists/* && \
  curl -sSL https://install.python-poetry.org | python3 -

COPY . /code

# Set the working directory
WORKDIR /code

# Install dependencies using Poetry
RUN poetry install --no-root --no-interaction --no-ansi


# Expose port 8000
EXPOSE 8000

CMD . ./setup-populate.sh; poetry run python manage.py runserver 0.0.0.0:8000