import google.generativeai as genai
from typing import List, Dict, Any
from config import settings
from logger import logger

class GeminiRAG:
    """RAG system using Gemini API for question answering."""
    
    def __init__(self):
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        logger.info("Initialized Gemini RAG system")
    
    def generate_answer(self, query: str, context_docs: List[str]) -> str:
        """Generate answer using Gemini based on retrieved context."""
        try:
            logger.info(f"Generating answer for query: {query}")
            
            # Prepare context from retrieved documents
            context = "\n\n".join([f"Document {i+1}:\n{doc}" for i, doc in enumerate(context_docs)])
            
            # Create prompt
            prompt = f"""You are a helpful study assistant. Answer the question based on the provided context from study materials.

Context from study materials:
{context}

Question: {query}

Instructions:
1. Answer based solely on the provided context
2. If the answer is not in the context, say "I don't have enough information in the provided materials to answer this question."
3. Be clear and concise
4. If relevant, mention which document/page the information comes from

Answer:"""
            
            # Generate response
            response = self.model.generate_content(prompt)
            answer = response.text
            
            logger.info(f"Successfully generated answer of length {len(answer)}")
            return answer
            
        except Exception as e:
            logger.error(f"Error generating answer with Gemini: {str(e)}")
            raise
    
    def chat(self, query: str, context_docs: List[str], chat_history: List[Dict[str, str]] = None) -> str:
        """Chat with context and history support."""
        try:
            # Build conversation history
            conversation = ""
            if chat_history:
                for msg in chat_history[-5:]:  # Keep last 5 exchanges
                    role = msg.get("role", "user")
                    content = msg.get("content", "")
                    conversation += f"{role.capitalize()}: {content}\n"
            
            # Add context
            context = "\n\n".join([f"Document {i+1}:\n{doc}" for i, doc in enumerate(context_docs)])
            
            prompt = f"""You are a helpful study assistant. Use the provided study materials and conversation history to answer questions.

Study Materials:
{context}

Previous Conversation:
{conversation}

Current Question: {query}

Provide a helpful, accurate answer based on the study materials. If you don't know or the information isn't in the materials, say so.

Answer:"""
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error in chat: {str(e)}")
            raise
