"""
Configuration settings for the Ask MTO application.
"""
import os
import re
import time
import uuid
import yaml
from threading import Lock
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Simple test endpoint that should always work
@app.get("/test")
async def test():
    """A simple test endpoint that should always work."""
    return {"status": "ok", "message": "Test endpoint is working!"}

# Health check endpoint
@app.get("/")
async def root():
    return {"status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

print("✅ Basic FastAPI routes initialized successfully!")

# Now import the complex dependencies
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA, LLMChain
from langchain_core.prompts import PromptTemplate

from app.config import config
from app.cosmosdb import store_session
from app.monitoring import track_request, track_rag_performance, log_info, log_error
from app.semantic_kernel import enhance_answer, suggest_followups, store_conversation

print("✅ All dependencies imported successfully!")

# ─── Get Absolute Paths ──────────────────────────────────────────────────
# Ensures files are found regardless of where the script is run
APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(APP_DIR)
VECTORSTORE_PATH = os.path.join(PROJECT_DIR, "vectorstore")
PROMPT_PATH = os.path.join(PROJECT_DIR, "prompt.yaml")

print(f"✅ APP_DIR: {APP_DIR}")
print(f"✅ PROJECT_DIR: {PROJECT_DIR}")
print(f"✅ VECTORSTORE_PATH: {VECTORSTORE_PATH}")
print(f"✅ PROMPT_PATH: {PROMPT_PATH}")

# ─── Load environment ───────────────────────────────────────────────────────────
load_dotenv()
config.validate()
OPENAI_API_KEY = config.OPENAI_API_KEY

# ─── Lazy Loading Singleton for RAG Components ──────────────────────────
class RAGComponents:
    _instance = None
    _lock = Lock()

    def __init__(self):
        self.qa_chain = None
        self.fallback_chain = None
        self.retriever = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    print("🚀 Initializing RAG components for the first time...")
                    start_time = time.time()
                    cls._instance = cls()
                    cls._instance._load_components()
                    end_time = time.time()
                    print(f"✅ RAG components loaded in {end_time - start_time:.2f} seconds.")
        return cls._instance

    def _load_components(self):
        try:
            # 1. Load FAISS vectorstore
            print("   -> Loading FAISS vectorstore...")
            if not os.path.exists(VECTORSTORE_PATH):
                raise FileNotFoundError(f"Vectorstore not found at {VECTORSTORE_PATH}")
            embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
            vectorstore = FAISS.load_local(
                VECTORSTORE_PATH,
                embeddings,
                allow_dangerous_deserialization=True
            )
            self.retriever = vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 5}
            )
            print("   -> FAISS vectorstore loaded.")

            # 2. Build RetrievalQA chain
            print("   -> Building RetrievalQA chain...")
            if not os.path.exists(PROMPT_PATH):
                raise FileNotFoundError(f"Prompt file not found at {PROMPT_PATH}")
            with open(PROMPT_PATH, "r") as f:
                prompt_data = yaml.safe_load(f)

            template = (
                prompt_data["system_prompt"] +
                "\\n\\n" +
                prompt_data["user_prompt"]
            )
            prompt = PromptTemplate(
                template=template,
                input_variables=["context", "question"]
            )
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY),
                chain_type="stuff",
                retriever=self.retriever,
                return_source_documents=True,
                chain_type_kwargs={"prompt": prompt}
            )
            print("   -> RetrievalQA chain built.")

            # 3. Build fallback chain
            print("   -> Building fallback chain...")
            fallback_prompt = PromptTemplate(
                input_variables=["question"],
                template="""
You are the Official MTO Driver's Handbook Assistant. While I couldn't find specific information in the handbook for your question, I'll provide helpful guidance based on general Ontario driving safety principles.
Question: {question}
Please provide a comprehensive answer that includes practical advice and alternatives. If this is a follow-up question (like "what should I do then?"), interpret it in the context of safe driving practices.
"""
            )
            self.fallback_chain = LLMChain(
                llm=ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY),
                prompt=fallback_prompt
            )
            print("   -> Fallback chain built.")
        except Exception as e:
            print(f"❌ Error loading RAG components: {e}")
            log_error("Failed to load RAG components", e)
            raise

# ─── FastAPI setup ──────────────────────────────────────────────────────────────
# app = FastAPI(title="Ask MTO API", description="Ontario MTO Driver's Handbook Assistant")
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=config.CORS_ORIGINS,
#     allow_credentials=True,
#     allow_methods=["GET", "POST"],
#     allow_headers=["*"],
# )

# Health check endpoints
# @app.get("/")
# async def root():
#     return {"message": "Ask MTO API is running!", "status": "healthy"}

# @app.get("/health")
# async def health_check():
#     return {"status": "healthy", "service": "ask-mto-api"}

class Question(BaseModel):
    question: str

# Simple conversation context storage (in production, use a proper session store)
conversation_context = {
    "last_question": "",
    "last_answer": ""
}

@app.on_event("startup")
async def startup_event():
    print("🚀 FastAPI server is starting up...")
    # Trigger loading components in background if you want to preload
    # For now, we lazy load on first request.
    # RAGComponents.get_instance()
    print("✅ FastAPI server is ready to accept requests.")

@app.post("/ask")
@track_request("/ask", "POST")
async def ask_question(query: Question):
    start_time = time.time()
    rag = RAGComponents.get_instance()

    # 1) Check if this is a follow-up question
    enhanced_question = query.question
    if any(word in query.question.lower() for word in ["what should i do then", "what should i do", "then what", "what then", "alternatives", "instead"]):
        if conversation_context["last_question"] and conversation_context["last_answer"]:
            enhanced_question = f"Previous question: {conversation_context['last_question']}\\nPrevious answer: {conversation_context['last_answer']}\\nFollow-up question: {query.question}"

    # 2) Run RAG
    resp = rag.qa_chain({"query": enhanced_question})
    answer = resp["result"].strip()
    docs = resp["source_documents"]

    # 2) Debug log top‑3 retrieved chunks
    for i, d in enumerate(docs[:3]):
        content = d.page_content[:200].replace('\\n', ' ')
        print(f"[{i}] {content}...")

    # 3) Fallback if RAG says "I don't know"
    normalized_answer = re.sub(r'[\\s\\W_]+', '', answer.lower())
    if "idontknow" in normalized_answer or not normalized_answer:
        fallback_question = enhanced_question if enhanced_question != query.question else query.question
        answer = rag.fallback_chain.predict(question=fallback_question).strip()

    # 4) Store conversation context for follow-up questions
    conversation_context["last_question"] = query.question
    conversation_context["last_answer"] = answer

    # 5) Store Q&A in CosmosDB (if available)
    session_id = str(uuid.uuid4())
    try:
        store_session(session_id, query.question, answer)
    except Exception as e:
        print(f"⚠️ Failed to store session: {e}")
        # Continue anyway - CosmosDB storage is not critical

    # 6) Track performance
    duration = time.time() - start_time
    track_rag_performance(
        question=query.question,
        answer=answer,
        sources_count=len(docs),
        duration=duration
    )

    # 7) Return answer (and optional top‑3 sources)
    return {
        "answer": answer,
        "sources": [d.page_content for d in docs[:3]]
    }

@app.post("/clear-context")
async def clear_context():
    """Clear conversation context for fresh start"""
    conversation_context["last_question"] = ""
    conversation_context["last_answer"] = ""
    return {"message": "Conversation context cleared"}

# NOTE: /evaluate endpoint removed to reduce production image size.
# This endpoint relies on heavy dependencies (ragas, datasets) that are not
# suitable for a lean production environment. This functionality should be
# run in a separate development/evaluation environment.
# @app.post("/evaluate")
# @track_request("/evaluate", "POST")
# async def evaluate_answer(query: Question):
#     """Evaluate the RAG system's answer using RAGAS metrics"""
#     try:
#         rag = RAGComponents.get_instance()
#         # Get answer from RAG system
#         enhanced_question = query.question
#         if any(word in query.question.lower() for word in ["what should i do then", "what should i do", "then what", "what then", "alternatives", "instead"]):
#             if conversation_context["last_question"] and conversation_context["last_answer"]:
#                 enhanced_question = f"Previous question: {conversation_context['last_question']}\\nPrevious answer: {conversation_context['last_answer']}\\nFollow-up question: {query.question}"
#
#         resp = rag.qa_chain({"query": enhanced_question})
#         answer = resp["result"].strip()
#         docs = resp["source_documents"]
#
#         # Prepare contexts for evaluation
#         contexts = [d.page_content for d in docs[:3]]
#
#         # Run RAGAS evaluation
#         evaluation = evaluate_single_qa(
#             question=query.question,
#             answer=answer,
#             contexts=contexts
#         )
#
#         return {
#             "question": query.question,
#             "answer": answer,
#             "sources": contexts,
#             "evaluation": evaluation
#         }
#
#     except Exception as e:
#         return {
#             "error": f"Evaluation failed: {str(e)}",
#             "question": query.question,
#             "answer": "",
#             "sources": [],
#             "evaluation": {
#                 "context_relevancy": 0.0,
#                 "answer_relevancy": 0.0,
#                 "faithfulness": 0.0,
#                 "context_recall": 0.0,
#                 "overall_score": 0.0
#                          }
#          }

@app.post("/ask-enhanced")
@track_request("/ask-enhanced", "POST")
async def ask_question_enhanced(query: Question):
    """Enhanced ask endpoint with Semantic Kernel orchestration"""
    start_time = time.time()
    rag = RAGComponents.get_instance()

    try:
        # 1) Get basic RAG answer (reuse existing logic)
        enhanced_question = query.question
        if any(word in query.question.lower() for word in ["what should i do then", "what should i do", "then what", "what then", "alternatives", "instead"]):
            if conversation_context["last_question"] and conversation_context["last_answer"]:
                enhanced_question = f"Previous question: {conversation_context['last_question']}\\nPrevious answer: {conversation_context['last_answer']}\\nFollow-up question: {query.question}"

        resp = rag.qa_chain({"query": enhanced_question})
        base_answer = resp["result"].strip()
        docs = resp["source_documents"]

        # Fallback if needed
        normalized_answer = re.sub(r'[\\s\\W_]+', '', base_answer.lower())
        if "idontknow" in normalized_answer or not normalized_answer:
            fallback_question = enhanced_question if enhanced_question != query.question else query.question
            base_answer = rag.fallback_chain.predict(question=fallback_question).strip()

        # 2) Enhance answer using Semantic Kernel
        context_text = " ".join([d.page_content[:200] for d in docs[:3]])
        enhancement_result = await enhance_answer(query.question, base_answer, context_text)

        final_answer = enhancement_result.get("enhanced_answer", base_answer)

        # 3) Generate follow-up questions
        followup_result = await suggest_followups(query.question, final_answer)
        followup_questions = followup_result.get("followup_questions", [])

        # 4) Store conversation in Semantic Kernel memory
        session_id = str(uuid.uuid4())
        await store_conversation(query.question, final_answer, session_id)

        # 5) Store in traditional storage
        store_session(session_id, query.question, final_answer)

        # 6) Update conversation context
        conversation_context["last_question"] = query.question
        conversation_context["last_answer"] = final_answer

        # 7) Track performance
        duration = time.time() - start_time
        track_rag_performance(
            question=query.question,
            answer=final_answer,
            sources_count=len(docs),
            duration=duration
        )

        return {
            "answer": final_answer,
            "sources": [d.page_content for d in docs[:3]],
            "followup_questions": followup_questions,
            "enhanced": enhancement_result.get("success", False),
            "session_id": session_id
        }

    except Exception as e:
        log_error("Enhanced ask endpoint failed", e)
        # Fallback to basic response
        return {
            "answer": "Sorry, I encountered an error processing your enhanced request. Please try the basic /ask endpoint.",
            "sources": [],
            "followup_questions": [],
            "enhanced": False,
            "error": str(e)
        }
