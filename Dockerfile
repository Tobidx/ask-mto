# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    PYTHONPATH=/app/ask-mto-genai

# Set working directory
WORKDIR /app/ask-mto-genai

# Copy only what's needed
COPY ask-mto-genai/ .

# Install dependencies with explicit commands and verification
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir uvicorn fastapi && \
    pip install --no-cache-dir -r requirements.txt && \
    python -c "import uvicorn; print('✅ uvicorn installed successfully')" && \
    python -c "import fastapi; print('✅ fastapi installed successfully')" && \
    pip list | grep uvicorn && \
    pip list | grep fastapi

# Print environment info for debugging
RUN python --version && \
    echo "Current directory:" && pwd && \
    echo "Directory contents:" && ls -la && \
    echo "Python path:" && \
    python -c "import sys; print('\n'.join(sys.path))"

# The command to run when the container starts
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT --log-level debug 