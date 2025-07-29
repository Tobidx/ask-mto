# Use a slim Python base image to keep the size down
FROM python:3.11-slim

# Set environment variables to make Python run better in Docker
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the startup script and the main application directory.
# This ensures only the 'ask-mto-genai' folder and its lean 'requirements.txt' are included.
COPY start_railway.py .
COPY ask-mto-genai/ ./ask-mto-genai/

# Install dependencies from our specific, lean requirements file.
# This command is now fully controlled by us, not Railway's auto-detection.
RUN pip install --no-cache-dir -r ask-mto-genai/requirements.txt

# The command to run when the container starts.
# This executes our startup script which handles directory changes and starts the server.
CMD ["python3", "start_railway.py"] 