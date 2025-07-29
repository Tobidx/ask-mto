#!/bin/bash

# Ask MTO Backend Startup Script
# This script starts the FastAPI backend with production settings

echo "🚀 Starting Ask MTO Backend..."

# Check if environment variables are set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ Error: OPENAI_API_KEY environment variable is not set"
    exit 1
fi

# Set default values
export HOST=${HOST:-"0.0.0.0"}
export PORT=${PORT:-"8000"}
export WORKERS=${WORKERS:-"1"}

echo "📡 Server will start on $HOST:$PORT with $WORKERS workers"

# Start the server
if [ "$ENVIRONMENT" = "development" ]; then
    echo "🔧 Starting in development mode with auto-reload..."
    python -m uvicorn app.main:app --host $HOST --port $PORT --reload
else
    echo "🏭 Starting in production mode..."
    python -m uvicorn app.main:app --host $HOST --port $PORT --workers $WORKERS
fi 