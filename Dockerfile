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

# Install critical dependencies first with verification
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
        uvicorn \
        fastapi \
        PyYAML \
        python-dotenv \
        pydantic && \
    # Verify critical dependencies
    python -c "import uvicorn; print('✅ uvicorn installed')" && \
    python -c "import fastapi; print('✅ fastapi installed')" && \
    python -c "import yaml; print('✅ PyYAML installed')" && \
    python -c "import dotenv; print('✅ python-dotenv installed')" && \
    python -c "import pydantic; print('✅ pydantic installed')"

# Now install the rest of the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Print environment info for debugging
RUN echo "=== Python Environment ===" && \
    python --version && \
    echo "\n=== Installed Packages ===" && \
    pip list && \
    echo "\n=== Working Directory ===" && \
    pwd && ls -la && \
    echo "\n=== Python Path ===" && \
    python -c "import sys; print('\n'.join(sys.path))" && \
    echo "\n=== Contents of requirements.txt ===" && \
    cat requirements.txt

# The command to run when the container starts
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT --log-level debug 