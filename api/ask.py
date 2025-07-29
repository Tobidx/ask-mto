import os
import re
import time
import uuid
import yaml
import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs

# Import the main modules from ask-mto-genai
import sys
sys.path.append('../ask-mto-genai')

from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA, LLMChain
from langchain_core.prompts import PromptTemplate

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Parse request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            question = data.get('question', '')
            if not question:
                self.send_error(400, "Question is required")
                return
            
            # Initialize OpenAI and vector store
            OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
            if not OPENAI_API_KEY:
                self.send_error(500, "OpenAI API key not configured")
                return
            
            # For now, return a simple response
            # TODO: Implement full RAG pipeline
            response = {
                "answer": f"I received your question: '{question}'. This is a demo response from Vercel serverless function.",
                "sources": ["Demo source 1", "Demo source 2"]
            }
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")
    
    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers() 