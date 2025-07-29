import os
import uuid
from datetime import datetime
from azure.cosmos import CosmosClient, PartitionKey
from dotenv import load_dotenv

# ✅ Load environment variables from .env file
load_dotenv()

# Fetch values
COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("COSMOS_KEY")
COSMOS_DB_NAME = os.getenv("COSMOS_DB_NAME", "ask-mto-db")
COSMOS_CONTAINER_NAME = os.getenv("COSMOS_CONTAINER_NAME", "session-history")

if not COSMOS_ENDPOINT or not COSMOS_KEY:
    raise ValueError("❌ Cosmos DB credentials not found in environment variables.")

# ✅ Ensure COSMOS_KEY is string (required by CosmosClient)
COSMOS_KEY = str(COSMOS_KEY)

# Initialize Cosmos client
client = CosmosClient(COSMOS_ENDPOINT, credential=COSMOS_KEY)

# Create or connect to database
database = client.create_database_if_not_exists(id=COSMOS_DB_NAME)

# Create or connect to container
container = database.create_container_if_not_exists(
    id=COSMOS_CONTAINER_NAME,
    partition_key=PartitionKey(path="/session_id"),
    offer_throughput=400
)

def store_session(session_id: str, question: str, answer: str):
    item = {
        "id": str(uuid.uuid4()),  # unique, safe ID
        "session_id": session_id,
        "question": question,
        "answer": answer,
        "timestamp": datetime.utcnow().isoformat()
    }
    container.upsert_item(item)
