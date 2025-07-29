#!/usr/bin/env python3
import os
import subprocess
import sys

# Change to the correct directory
os.chdir('ask-mto-genai')

# Set up the Python path
sys.path.insert(0, os.getcwd())

# Get the port from environment variable
port = os.environ.get('PORT', '8000')

# Start uvicorn
cmd = [sys.executable, '-m', 'uvicorn', 'app.main:app', '--host', '0.0.0.0', '--port', str(port)]

print(f"Starting server with command: {' '.join(cmd)}")
print(f"Current directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

# Execute the command
subprocess.run(cmd) 