from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import shutil
from pathlib import Path

from config import settings
from logger import logger
from document_processor import DocumentProcessor
from vector_store import VectorStore
from gemini_rag import GeminiRAG

# Initialize FastAPI app
app = FastAPI(
    title="Study Assistant API",
    description="RAG-based Study Support Chatbot API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
vector_store = VectorStore()
gemini_rag = GeminiRAG()
document_processor = DocumentProcessor()

# Pydantic models
class ChatRequest(BaseModel):
    query: str
    chat_history: Optional[List[Dict[str, str]]] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]

class StatusResponse(BaseModel):
    status: str
    message: str
    document_count: int

class UploadResponse(BaseModel):
    status: str
    message: str
    filename: str
    chunks_added: int

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Study Assistant API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        doc_count = vector_store.get_collection_count()
        return {
            "status": "healthy",
            "documents_indexed": doc_count
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """Upload and process a PDF or PPTX file."""
    try:
        logger.info(f"Received file upload: {file.filename}")
        
        # Validate file type
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ['.pdf', '.pptx']:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_ext}. Only PDF and PPTX files are supported."
            )
        
        # Save uploaded file
        file_path = os.path.join(settings.upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"File saved to: {file_path}")
        
        # Process document
        text = document_processor.process_document(file_path)
        
        if not text or len(text.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="No text could be extracted from the document"
            )
        
        # Chunk text
        chunks = document_processor.chunk_text(
            text,
            chunk_size=settings.chunk_size,
            overlap=settings.chunk_overlap
        )
        
        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="Failed to create chunks from the document"
            )
        
        # Add to vector store
        metadata = [{"filename": file.filename, "chunk_id": i} for i in range(len(chunks))]
        vector_store.add_documents(chunks, metadata)
        
        logger.info(f"Successfully processed {file.filename}: {len(chunks)} chunks added")
        
        return UploadResponse(
            status="success",
            message=f"File processed successfully",
            filename=file.filename,
            chunks_added=len(chunks)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with the study assistant."""
    try:
        logger.info(f"Received chat request: {request.query}")
        
        if not request.query or len(request.query.strip()) == 0:
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Check if there are any documents
        doc_count = vector_store.get_collection_count()
        if doc_count == 0:
            return ChatResponse(
                answer="Please upload some study materials (PDF or PPTX files) first before asking questions.",
                sources=[]
            )
        
        # Search for relevant documents
        search_results = vector_store.search(request.query, n_results=3)
        
        # Extract documents and metadata
        documents = search_results.get('documents', [[]])[0]
        metadatas = search_results.get('metadatas', [[]])[0]
        
        if not documents:
            return ChatResponse(
                answer="I couldn't find relevant information in the uploaded materials to answer your question.",
                sources=[]
            )
        
        # Generate answer using Gemini
        if request.chat_history:
            answer = gemini_rag.chat(request.query, documents, request.chat_history)
        else:
            answer = gemini_rag.generate_answer(request.query, documents)
        
        # Prepare sources
        sources = []
        for meta in metadatas:
            if meta:
                source = f"{meta.get('filename', 'Unknown')} (Chunk {meta.get('chunk_id', 'N/A')})"
                if source not in sources:
                    sources.append(source)
        
        logger.info(f"Successfully generated answer for query")
        
        return ChatResponse(
            answer=answer,
            sources=sources
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.get("/status", response_model=StatusResponse)
async def get_status():
    """Get system status."""
    try:
        doc_count = vector_store.get_collection_count()
        return StatusResponse(
            status="active",
            message=f"System is running with {doc_count} document chunks indexed",
            document_count=doc_count
        )
    except Exception as e:
        logger.error(f"Error getting status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/clear")
async def clear_documents():
    """Clear all uploaded documents and vector store."""
    try:
        logger.info("Clearing all documents")
        
        # Clear vector store
        vector_store.clear_collection()
        
        # Clear uploaded files
        upload_dir = Path(settings.upload_dir)
        for file_path in upload_dir.glob("*"):
            if file_path.is_file():
                file_path.unlink()
        
        logger.info("Successfully cleared all documents")
        
        return {
            "status": "success",
            "message": "All documents cleared successfully"
        }
        
    except Exception as e:
        logger.error(f"Error clearing documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
