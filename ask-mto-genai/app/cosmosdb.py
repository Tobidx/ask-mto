"""
Module for Cosmos DB operations.
"""
import os
from datetime import datetime
from azure.cosmos import CosmosClient
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()

# Initialize as None - will be set up only if credentials are available
cosmos_client: Optional[CosmosClient] = None
container = None

def init_cosmos():
    """Initialize Cosmos DB client if credentials are available."""
    global cosmos_client, container

    endpoint = os.getenv("COSMOS_ENDPOINT")
    key = os.getenv("COSMOS_KEY")
    db_name = os.getenv("COSMOS_DB_NAME", "ask-mto")
    container_name = os.getenv("COSMOS_CONTAINER_NAME", "sessions")

    if endpoint and key:
        try:
            cosmos_client = CosmosClient(endpoint, key)
            database = cosmos_client.get_database_client(db_name)
            container = database.get_container_client(container_name)
            print("✅ Cosmos DB connection initialized successfully")
        except Exception as e:
            print(f"⚠️ Failed to initialize Cosmos DB: {e}")
            cosmos_client = None
            container = None
    else:
        print("⚠️ Cosmos DB credentials not found - running without session storage")

def store_session(session_id: str, question: str, answer: str) -> bool:
    """Store a Q&A session in Cosmos DB if available."""
    if not container:
        print("⚠️ Cosmos DB not initialized - skipping session storage")
        return False

    try:
        container.upsert_item({
            "id": session_id,
            "question": question,
            "answer": answer,
            "timestamp": datetime.utcnow().isoformat()
        })
        return True
    except Exception as e:
        print(f"⚠️ Failed to store session: {e}")
        return False

# Initialize on module import
init_cosmos()
