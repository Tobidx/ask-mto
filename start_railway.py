#!/usr/bin/env python3
import os
import subprocess
import sys
import traceback

def main():
    try:
        print("=== Railway Startup Script ===")
        print(f"Python version: {sys.version}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Environment PORT: {os.environ.get('PORT', 'Not set')}")
        print(f"Environment OPENAI_API_KEY: {'Set' if os.environ.get('OPENAI_API_KEY') else 'Not set'}")
        
        # Change to the correct directory
        print("Changing to ask-mto-genai directory...")
        os.chdir('ask-mto-genai')
        print(f"New working directory: {os.getcwd()}")
        
        # List files to verify structure
        print("Files in current directory:")
        for item in os.listdir('.'):
            print(f"  {item}")
        
        # Check if required files exist
        required_files = ['app', 'vectorstore', 'prompt.yaml']
        for file in required_files:
            if os.path.exists(file):
                print(f"✓ {file} exists")
            else:
                print(f"✗ {file} missing")
        
        # Set up the Python path
        sys.path.insert(0, os.getcwd())
        print(f"Python path: {sys.path[:3]}...")  # Show first 3 entries
        
        # Test import of main app
        print("Testing imports...")
        try:
            from app.main import app
            print("✓ Successfully imported FastAPI app")
        except Exception as e:
            print(f"✗ Failed to import app: {e}")
            print("Traceback:")
            traceback.print_exc()
            return 1
        
        # Get the port from environment variable
        port = os.environ.get('PORT', '8000')
        print(f"Starting server on port {port}")
        
        # Start uvicorn
        cmd = [sys.executable, '-m', 'uvicorn', 'app.main:app', '--host', '0.0.0.0', '--port', str(port)]
        
        print(f"Executing command: {' '.join(cmd)}")
        print("=" * 50)
        
        # Execute the command
        subprocess.run(cmd)
        
    except Exception as e:
        print(f"FATAL ERROR in startup script: {e}")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main()) 