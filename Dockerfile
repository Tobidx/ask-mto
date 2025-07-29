# Use the standard Python base image, which includes more system libraries
# required by complex packages like faiss-cpu and numpy. This solves silent crashes.
FROM python:3.11

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
# We use shell form to allow environment variable expansion for $PORT.
# We run uvicorn directly from the correct working directory.
CMD sh -c "python3 -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}" 