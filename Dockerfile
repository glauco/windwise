FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Configure poetry to not create virtual environment (since container is isolated)
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --without dev --no-interaction --no-ansi

# Create non-root user
RUN useradd -m -s /bin/bash windwise

# Switch to non-root user
USER windwise

# Copy application code
COPY --chown=windwise:windwise . .

# Run the application directly since dependencies are installed in system Python
CMD ["python", "main.py"]

