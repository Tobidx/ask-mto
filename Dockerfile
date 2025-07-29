# Use a simpler Python image for testing
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Set working directory
WORKDIR /app/ask-mto-genai

# Copy only what's needed
COPY ask-mto-genai/ .

# Install dependencies with verbose output
RUN pip install --no-cache-dir -v -r requirements.txt

# Print environment info for debugging
RUN python --version && \
    pip list && \
    pwd && \
    ls -la

# The command to run when the container starts
CMD echo "Starting server on port $PORT" && \
    python -c "import sys; print(f'Python path: {sys.path}')" && \
    python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT --log-level debug 