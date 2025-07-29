import os
import re
import time
import uuid
import yaml
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA, LLMChain
from langchain_core.prompts import PromptTemplate

from app.config import config
from app.cosmosdb import store_session
from app.eval_ragas import evaluate_single_qa
from app.monitoring import track_request, track_rag_performance, log_info, log_error
from app.semantic_kernel import enhance_answer, suggest_followups, store_conversation

# ─── Load environment ───────────────────────────────────────────────────────────
load_dotenv()
config.validate()
OPENAI_API_KEY = config.OPENAI_API_KEY

# ─── Load FAISS vectorstore ─────────────────────────────────────────────────────
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
vectorstore = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)

# ─── Build RetrievalQA chain (with source docs) ────────────────────────────────
with open("prompt.yaml", "r") as f:
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
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY),
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt}
)

# ─── Build fallback general‑knowledge chain ────────────────────────────────────
fallback_prompt = PromptTemplate(
    input_variables=["question"],
    template="""
You are the Official MTO Driver's Handbook Assistant. While I couldn't find specific information in the handbook for your question, I'll provide helpful guidance based on general Ontario driving safety principles.

Question: {question}

Please provide a comprehensive answer that includes practical advice and alternatives. If this is a follow-up question (like "what should I do then?"), interpret it in the context of safe driving practices.
"""
)
fallback_chain = LLMChain(
    llm=ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY),
    prompt=fallback_prompt
)

# ─── FastAPI setup ──────────────────────────────────────────────────────────────
app = FastAPI(title="Ask MTO API", description="Ontario MTO Driver's Handbook Assistant")
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Health check endpoints
@app.get("/")
async def root():
    return {"message": "Ask MTO API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ask-mto-api"}

class Question(BaseModel):
    question: str

# Simple conversation context storage (in production, use a proper session store)
conversation_context = {
    "last_question": "",
    "last_answer": ""
}

@app.post("/ask")
@track_request("/ask", "POST")
async def ask_question(query: Question):
    start_time = time.time()
    
    # 1) Check if this is a follow-up question
    enhanced_question = query.question
    if any(word in query.question.lower() for word in ["what should i do then", "what should i do", "then what", "what then", "alternatives", "instead"]):
        if conversation_context["last_question"] and conversation_context["last_answer"]:
            enhanced_question = f"Previous question: {conversation_context['last_question']}\nPrevious answer: {conversation_context['last_answer']}\nFollow-up question: {query.question}"
    
    # 2) Run RAG
    resp = qa_chain({"query": enhanced_question})
    answer = resp["result"].strip()
    docs   = resp["source_documents"]

    # 2) Debug log top‑3 retrieved chunks
    for i, d in enumerate(docs[:3]):
        content = d.page_content[:200].replace('\n', ' ')
        print(f"[{i}] {content}...")

    # 3) Fallback if RAG says "I don't know"
    normalized_answer = re.sub(r'[\\s\\W_]+', '', answer.lower())
    if "idontknow" in normalized_answer or not normalized_answer:
        # Use enhanced question for fallback too
        fallback_question = enhanced_question if enhanced_question != query.question else query.question
        answer = fallback_chain.predict(question=fallback_question).strip()

    # 4) Store conversation context for follow-up questions
    conversation_context["last_question"] = query.question
    conversation_context["last_answer"] = answer

    # 5) Store Q&A in CosmosDB
    session_id = str(uuid.uuid4())
    store_session(session_id, query.question, answer)

    # 6) Track performance
    duration = time.time() - start_time if 'start_time' in locals() else 0
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

@app.post("/evaluate")
@track_request("/evaluate", "POST")
async def evaluate_answer(query: Question):
    """Evaluate the RAG system's answer using RAGAS metrics"""
    try:
        # Get answer from RAG system
        enhanced_question = query.question
        if any(word in query.question.lower() for word in ["what should i do then", "what should i do", "then what", "what then", "alternatives", "instead"]):
            if conversation_context["last_question"] and conversation_context["last_answer"]:
                enhanced_question = f"Previous question: {conversation_context['last_question']}\\nPrevious answer: {conversation_context['last_answer']}\\nFollow-up question: {query.question}"
        
        resp = qa_chain({"query": enhanced_question})
        answer = resp["result"].strip()
        docs = resp["source_documents"]
        
        # Prepare contexts for evaluation
        contexts = [d.page_content for d in docs[:3]]
        
        # Run RAGAS evaluation
        evaluation = evaluate_single_qa(
            question=query.question,
            answer=answer,
            contexts=contexts
        )
        
        return {
            "question": query.question,
            "answer": answer,
            "sources": contexts,
            "evaluation": evaluation
        }
    
    except Exception as e:
        return {
            "error": f"Evaluation failed: {str(e)}",
            "question": query.question,
            "answer": "",
            "sources": [],
            "evaluation": {
                "context_relevancy": 0.0,
                "answer_relevancy": 0.0,
                "faithfulness": 0.0,
                "context_recall": 0.0,
                "overall_score": 0.0
                         }
         }

@app.post("/ask-enhanced")
@track_request("/ask-enhanced", "POST")
async def ask_question_enhanced(query: Question):
    """Enhanced ask endpoint with Semantic Kernel orchestration"""
    start_time = time.time()
    
    try:
        # 1) Get basic RAG answer (reuse existing logic)
        enhanced_question = query.question
        if any(word in query.question.lower() for word in ["what should i do then", "what should i do", "then what", "what then", "alternatives", "instead"]):
            if conversation_context["last_question"] and conversation_context["last_answer"]:
                enhanced_question = f"Previous question: {conversation_context['last_question']}\nPrevious answer: {conversation_context['last_answer']}\nFollow-up question: {query.question}"
        
        resp = qa_chain({"query": enhanced_question})
        base_answer = resp["result"].strip()
        docs = resp["source_documents"]
        
        # Fallback if needed
        normalized_answer = re.sub(r'[\\s\\W_]+', '', base_answer.lower())
        if "idontknow" in normalized_answer or not normalized_answer:
            fallback_question = enhanced_question if enhanced_question != query.question else query.question
            base_answer = fallback_chain.predict(question=fallback_question).strip()
        
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
