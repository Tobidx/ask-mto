# Use the standard Python base image.
FROM python:3.11

# Install critical system-level dependencies required for ML libraries like FAISS.
# This is the definitive fix for the silent crash during startup.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables to make Python run better in Docker
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory directly to the application's subdirectory
WORKDIR /app/ask-mto-genai

# Copy the application source code into the working directory
COPY ask-mto-genai/ .

# Install dependencies from our specific, lean requirements file.
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app will run on. The $PORT variable is supplied by Railway.
EXPOSE 8000

# The command to run when the container starts.
# We add --log-level debug to get maximum visibility during startup.
CMD sh -c "python3 -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --log-level debug" 