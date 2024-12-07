# Stage 1: Build the frontend
FROM node:20 AS frontend-builder

# Set the working directory
WORKDIR /app

# Copy frontend files
COPY src/ui/ .
RUN npm ci

# Build the frontend
RUN npm run build

# Stage 2: Build the backend
FROM python:3.9

# Set the working directory
WORKDIR /app

# Poetry configuration files
COPY pyproject.toml poetry.lock* ./

# Install Poetry and dependencies
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Install Gunicorn
RUN pip install gunicorn

# Copy backend files
COPY prompts.json ./
COPY src/backend ./src/backend

# Copy the built frontend files from the frontend-builder stage
COPY --from=frontend-builder /app/build ./src/ui/build

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/app/src/backend

# Expose port and start the application in src/backend/main.py
EXPOSE 8000
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "main:app"]