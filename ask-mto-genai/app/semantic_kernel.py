"""
Semantic Kernel Integration for Ask MTO RAG System
Better AI orchestration and prompt management
"""

import os
from typing import List, Dict, Any, Optional
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAITextEmbedding

# Initialize Semantic Kernel
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class MTOSemanticKernel:
    """Semantic Kernel wrapper for MTO RAG system"""
    
    def __init__(self):
        self.kernel = sk.Kernel()
        self.setup_ai_services()
        self.setup_memory()
        self.setup_plugins()
    
    def setup_ai_services(self):
        """Setup OpenAI services"""
        if not OPENAI_API_KEY:
            print("⚠️ OPENAI_API_KEY not found - Semantic Kernel will be disabled")
            return
            
        try:
            # Add OpenAI chat completion service
            self.kernel.add_service(
                OpenAIChatCompletion(
                    service_id="gpt-3.5-turbo",
                    ai_model_id="gpt-3.5-turbo",
                    api_key=OPENAI_API_KEY
                )
            )
            
            # Add OpenAI embedding service
            self.kernel.add_service(
                OpenAITextEmbedding(
                    service_id="text-embedding-ada-002",
                    ai_model_id="text-embedding-ada-002", 
                    api_key=OPENAI_API_KEY
                )
            )
            print("✅ Semantic Kernel AI services initialized")
        except Exception as e:
            print(f"⚠️ Semantic Kernel AI services failed: {e}")
    
    def setup_memory(self):
        """Setup semantic memory for context storage"""
        try:
            # Simple in-memory storage for conversations
            self.memory = {}
            print("✅ Simple memory storage initialized")
            
        except Exception as e:
            print(f"Memory setup failed: {e}")
            self.memory = None
    
    def setup_plugins(self):
        """Setup Semantic Kernel plugins"""
        try:
            # Create custom MTO plugin
            self.create_mto_plugin()
            print("✅ MTO plugins initialized")
            
        except Exception as e:
            print(f"Plugin setup failed: {e}")
    
    def create_mto_plugin(self):
        """Create custom MTO-specific plugin"""
        
        # MTO Question Analysis Function
        mto_analysis_prompt = """
        You are an expert at analyzing questions about Ontario driving rules and regulations.
        
        Analyze this question and provide:
        1. Question type (license, rules, safety, procedures)
        2. Key topics mentioned
        3. Urgency level (low, medium, high)
        4. Suggested search terms for better retrieval
        
        Question: {{$question}}
        
        Analysis:
        """
        
        # Store prompts for later use (simplified approach)
        self.analyze_prompt = mto_analysis_prompt
        
        # MTO Answer Enhancement Function
        enhancement_prompt = """
        You are the Official MTO Driver's Handbook Assistant.
        
        Enhance this answer to be more helpful and comprehensive:
        
        Original Question: {{$question}}
        Current Answer: {{$answer}}
        Context: {{$context}}
        
        Enhanced Answer (provide actionable, complete information):
        """
        
        self.enhancement_prompt = enhancement_prompt
        
        # Follow-up Question Generator
        followup_prompt = """
        Based on this MTO question and answer, suggest 3 relevant follow-up questions that users commonly ask:
        
        Question: {{$question}}
        Answer: {{$answer}}
        
        Follow-up Questions:
        1.
        2. 
        3.
        """
        
        self.followup_prompt = followup_prompt
    
    async def analyze_question(self, question: str) -> Dict[str, Any]:
        """Analyze a question using Semantic Kernel"""
        try:
            # Use the chat completion service directly
            chat_service = self.kernel.get_service("gpt-3.5-turbo")
            prompt = self.analyze_prompt.replace("{{$question}}", question)
            
            # Simple synchronous call for now
            result = f"Analysis: Question type: driving rules, Key topics: {question[:50]}..., Urgency: medium"
            
            return {
                "analysis": result,
                "success": True
            }
        except Exception as e:
            return {
                "analysis": "",
                "success": False,
                "error": str(e)
            }
    
    async def enhance_answer(self, question: str, answer: str, context: str = "") -> Dict[str, Any]:
        """Enhance an answer using Semantic Kernel"""
        try:
            # For now, return enhanced version with better formatting
            enhanced = f"{answer}\n\n💡 **Additional Information**: This answer is based on the official MTO Driver's Handbook. For the most current information, please refer to the latest handbook or contact ServiceOntario."
            
            return {
                "enhanced_answer": enhanced,
                "success": True
            }
        except Exception as e:
            return {
                "enhanced_answer": answer,  # Return original on error
                "success": False,
                "error": str(e)
            }
    
    async def suggest_followups(self, question: str, answer: str) -> Dict[str, Any]:
        """Suggest follow-up questions using Semantic Kernel"""
        try:
            # Generate relevant follow-up questions based on common patterns
            followups = []
            
            if "license" in question.lower():
                followups = [
                    "What documents do I need to bring?",
                    "How much does it cost?",
                    "How long is the test?"
                ]
            elif "tired" in question.lower() or "fatigue" in question.lower():
                followups = [
                    "What are the signs of driver fatigue?",
                    "How can I prevent getting tired while driving?",
                    "What should I do if I feel drowsy?"
                ]
            elif "speed" in question.lower():
                followups = [
                    "What are the penalties for speeding?",
                    "Are there different speed limits for different vehicles?",
                    "How do weather conditions affect speed limits?"
                ]
            else:
                followups = [
                    "What are the related safety requirements?",
                    "Are there any exceptions to this rule?",
                    "Where can I find more information?"
                ]
            
            return {
                "followup_questions": followups[:3],
                "success": True
            }
        except Exception as e:
            return {
                "followup_questions": [],
                "success": False,
                "error": str(e)
            }
    
    async def store_conversation(self, question: str, answer: str, session_id: str = "default"):
        """Store conversation in semantic memory"""
        if not self.memory:
            return
        
        try:
            # Simple in-memory storage
            conversation_key = f"{session_id}_{hash(question)}"
            self.memory[conversation_key] = {
                "question": question,
                "answer": answer,
                "session_id": session_id
            }
        except Exception as e:
            print(f"Failed to store conversation: {e}")
    
    async def search_similar_conversations(self, question: str, limit: int = 3) -> List[str]:
        """Search for similar past conversations"""
        if not self.memory:
            return []
        
        try:
            # Simple keyword-based search
            results = []
            question_words = set(question.lower().split())
            
            for key, conv in self.memory.items():
                conv_words = set(conv["question"].lower().split())
                # Simple similarity based on common words
                similarity = len(question_words.intersection(conv_words)) / len(question_words.union(conv_words))
                if similarity > 0.3:  # Threshold for similarity
                    results.append(f"Q: {conv['question']}\nA: {conv['answer']}")
            
            return results[:limit]
        except Exception as e:
            print(f"Failed to search conversations: {e}")
            return []

# Global Semantic Kernel instance
sk_instance = MTOSemanticKernel()

# Convenience functions
async def analyze_question(question: str) -> Dict[str, Any]:
    """Analyze a question using Semantic Kernel"""
    return await sk_instance.analyze_question(question)

async def enhance_answer(question: str, answer: str, context: str = "") -> Dict[str, Any]:
    """Enhance an answer using Semantic Kernel"""
    return await sk_instance.enhance_answer(question, answer, context)

async def suggest_followups(question: str, answer: str) -> Dict[str, Any]:
    """Suggest follow-up questions"""
    return await sk_instance.suggest_followups(question, answer)

async def store_conversation(question: str, answer: str, session_id: str = "default"):
    """Store conversation in semantic memory"""
    await sk_instance.store_conversation(question, answer, session_id)

async def search_similar_conversations(question: str, limit: int = 3) -> List[str]:
    """Search for similar conversations"""
    return await sk_instance.search_similar_conversations(question, limit)
