"""
RAGAS Evaluation for Ask MTO RAG System
Simple implementation to measure RAG quality metrics
"""

import os
from typing import List, Dict, Any
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    answer_relevancy,
    context_relevancy, 
    faithfulness,
    context_recall
)
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Initialize OpenAI components for RAGAS
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize components only if API key is available
if OPENAI_API_KEY:
    try:
        llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        print("✅ RAGAS OpenAI components initialized")
    except Exception as e:
        print(f"⚠️ RAGAS OpenAI initialization failed: {e}")
        llm = None
        embeddings = None
else:
    print("⚠️ OPENAI_API_KEY not found - RAGAS evaluation will be disabled")
    llm = None
    embeddings = None

def create_evaluation_dataset(questions: List[str], answers: List[str], 
                            contexts: List[List[str]], ground_truths: List[str] = None) -> Dataset:
    """Create a dataset for RAGAS evaluation"""
    
    # If no ground truths provided, use the answers as ground truths for basic evaluation
    if ground_truths is None:
        ground_truths = answers
    
    eval_data = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    }
    
    return Dataset.from_dict(eval_data)

def evaluate_rag_system(questions: List[str], answers: List[str], 
                       contexts: List[List[str]], ground_truths: List[str] = None) -> Dict[str, Any]:
    """
    Evaluate RAG system using RAGAS metrics
    
    Args:
        questions: List of questions asked
        answers: List of generated answers
        contexts: List of retrieved contexts for each question
        ground_truths: Optional list of ground truth answers
    
    Returns:
        Dictionary with evaluation scores
    """
    
    # Check if components are available
    if not llm or not embeddings:
        return {
            "error": "RAGAS evaluation disabled - OpenAI API key not configured",
            "context_relevancy": 0.0,
            "answer_relevancy": 0.0,
            "faithfulness": 0.0,
            "context_recall": 0.0,
            "overall_score": 0.0
        }
    
    # Create evaluation dataset
    dataset = create_evaluation_dataset(questions, answers, contexts, ground_truths)
    
    # Define metrics to evaluate
    metrics = [
        context_relevancy,    # How relevant are the retrieved contexts
        answer_relevancy,     # How relevant is the answer to the question
        faithfulness,         # How faithful is the answer to the context
        context_recall        # How much of the ground truth is captured in contexts
    ]
    
    try:
        # Run evaluation
        result = evaluate(
            dataset=dataset,
            metrics=metrics,
            llm=llm,
            embeddings=embeddings
        )
        
        return {
            "context_relevancy": float(result["context_relevancy"]),
            "answer_relevancy": float(result["answer_relevancy"]),
            "faithfulness": float(result["faithfulness"]),
            "context_recall": float(result["context_recall"]),
            "overall_score": float(
                (result["context_relevancy"] + result["answer_relevancy"] + 
                 result["faithfulness"] + result["context_recall"]) / 4
            )
        }
    
    except Exception as e:
        print(f"RAGAS evaluation error: {e}")
        return {
            "error": str(e),
            "context_relevancy": 0.0,
            "answer_relevancy": 0.0,
            "faithfulness": 0.0,
            "context_recall": 0.0,
            "overall_score": 0.0
        }

def evaluate_single_qa(question: str, answer: str, contexts: List[str], ground_truth: str = None):
    """Evaluate a single Q&A pair"""
    return evaluate_rag_system([question], [answer], [contexts], [ground_truth] if ground_truth else None)

# Sample test data for MTO questions
SAMPLE_TEST_DATA = {
    "questions": [
        "How do I get my G1 license?",
        "What should I do when I am tired while driving?",
        "What are the speed limits in Ontario?",
        "How long is the G1 license valid?"
    ],
    "ground_truths": [
        "To get your G1 license, you must be at least 16 years old, pass a vision test, and pass a written knowledge test.",
        "Don't drive when you are tired. Pull over safely and rest, take a break, or have someone else drive.",
        "Speed limits are 50 km/h in cities, towns and villages, and 80 km/h elsewhere unless posted otherwise.",
        "The G1 license is valid for 5 years from the date it was issued."
    ]
}

def run_sample_evaluation():
    """Run a sample evaluation with test data"""
    print("Running sample RAGAS evaluation...")
    
    # This would normally come from your RAG system
    sample_answers = [
        "You need to be 16, pass vision and knowledge tests to get G1.",
        "Don't drive tired. Rest or get someone else to drive.",
        "50 km/h in cities, 80 km/h elsewhere unless posted.",
        "G1 license is valid for 5 years."
    ]
    
    sample_contexts = [
        ["To apply for a licence, you must be at least 16 years old, pass a vision test and pass a written knowledge test."],
        ["Don't drive when you are tired. You might fall asleep at the wheel, risking lives."],
        ["Maximum speed is 50 km/h in cities, towns and villages, and 80 km/h elsewhere."],
        ["Your G1 licence is valid for five years from the date it was issued."]
    ]
    
    results = evaluate_rag_system(
        SAMPLE_TEST_DATA["questions"],
        sample_answers,
        sample_contexts,
        SAMPLE_TEST_DATA["ground_truths"]
    )
    
    print("\n=== RAGAS Evaluation Results ===")
    for metric, score in results.items():
        if metric != "error":
            print(f"{metric.replace('_', ' ').title()}: {score:.3f}")
    
    return results

if __name__ == "__main__":
    run_sample_evaluation()
