# Study Assistant - Architecture Documentation

## System Overview

The Study Assistant is a RAG (Retrieval-Augmented Generation) based chatbot that helps students learn from their study materials. It uses a two-tier architecture with a FastAPI backend and React frontend.

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│                    (React + TypeScript)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ FileUpload   │  │ ChatInterface│  │  StatusBar   │     │
│  │  Component   │  │   Component  │  │  Component   │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                  │                  │              │
│         └──────────────────┴──────────────────┘              │
│                            │                                 │
│                     ┌──────▼───────┐                        │
│                     │  API Service  │                        │
│                     │   (Axios)     │                        │
│                     └──────┬────────┘                        │
└────────────────────────────┼─────────────────────────────────┘
                             │ HTTP/REST
                             │
┌────────────────────────────▼─────────────────────────────────┐
│                         Backend                              │
│                        (FastAPI)                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                     API Endpoints                       │ │
│  │  /upload  /chat  /status  /clear  /health             │ │
│  └────────────────┬───────────────────────────────────────┘ │
│                   │                                          │
│  ┌────────────────▼───────────────────────────────────────┐ │
│  │              Core Processing Layer                      │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │ │
│  │  │  Document    │  │ Vector Store │  │  Gemini RAG │ │ │
│  │  │  Processor   │  │  (ChromaDB)  │  │    Engine   │ │ │
│  │  └──────────────┘  └──────────────┘  └─────────────┘ │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              External Services                          │ │
│  │  - Gemini API (Question Answering)                     │ │
│  │  - Sentence Transformers (Embeddings)                  │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend Components

#### 1. App.tsx (Main Application)
- **Purpose**: Root component that manages application state
- **Responsibilities**:
  - Layout management
  - Notification system
  - Component orchestration
  - State management for uploads and status

#### 2. FileUpload Component
- **Purpose**: Handle document uploads
- **Features**:
  - Drag-and-drop interface
  - File validation (.pdf, .pptx)
  - Upload progress indication
  - File size validation (10MB limit)
- **Props**:
  - `onUploadSuccess`: Callback for successful uploads
  - `onUploadError`: Callback for upload errors

#### 3. ChatInterface Component
- **Purpose**: Interactive chat interface
- **Features**:
  - Message display (user and assistant)
  - Input handling with Enter key support
  - Loading states
  - Source citation display
  - Auto-scroll to latest message
  - Chat history management
- **Props**:
  - `onError`: Callback for error handling

#### 4. StatusBar Component
- **Purpose**: Display system status
- **Features**:
  - Connection status indicator
  - Document count display
  - Clear all documents button
  - Auto-refresh on changes
- **Props**:
  - `refreshTrigger`: Number to trigger status refresh

#### 5. API Service (api.ts)
- **Purpose**: Centralized API communication
- **Methods**:
  - `uploadFile(file)`: Upload document
  - `chat(query, history)`: Send chat query
  - `getStatus()`: Get system status
  - `clearDocuments()`: Clear all documents
  - `healthCheck()`: Check backend health

### Backend Components

#### 1. main.py (FastAPI Application)
- **Purpose**: Main API server
- **Endpoints**:
  ```
  GET  /           - Root endpoint
  GET  /health     - Health check
  POST /upload     - Upload document
  POST /chat       - Chat with AI
  GET  /status     - System status
  DELETE /clear    - Clear documents
  ```
- **Middleware**:
  - CORS (Cross-Origin Resource Sharing)
- **Error Handling**:
  - HTTPException for client errors
  - Logging for debugging

#### 2. document_processor.py
- **Purpose**: Extract and process text from documents
- **Classes**:
  - `DocumentProcessor`: Main processing class
- **Methods**:
  - `extract_text_from_pdf(file_path)`: Extract text from PDFs
  - `extract_text_from_pptx(file_path)`: Extract text from PPTX
  - `process_document(file_path)`: Route to correct processor
  - `chunk_text(text, chunk_size, overlap)`: Split text into chunks
- **Libraries Used**:
  - PyPDF2: PDF text extraction
  - python-pptx: PPTX text extraction

#### 3. vector_store.py
- **Purpose**: Manage vector embeddings and similarity search
- **Classes**:
  - `VectorStore`: ChromaDB wrapper
- **Methods**:
  - `add_documents(chunks, metadata)`: Add document chunks
  - `search(query, n_results)`: Find similar documents
  - `clear_collection()`: Remove all documents
  - `get_collection_count()`: Get document count
- **Configuration**:
  - Embedding model: `all-MiniLM-L6-v2`
  - Distance metric: Cosine similarity
  - Persistent storage in `vector_store_dir`

#### 4. gemini_rag.py
- **Purpose**: RAG implementation with Gemini API
- **Classes**:
  - `GeminiRAG`: RAG engine
- **Methods**:
  - `generate_answer(query, context_docs)`: Generate answer from context
  - `chat(query, context_docs, chat_history)`: Chat with history support
- **Features**:
  - Context-aware prompting
  - Source citation in responses
  - Conversation history support
  - Graceful handling when no context found

#### 5. config.py
- **Purpose**: Configuration management
- **Classes**:
  - `Settings`: Pydantic settings model
- **Configuration Variables**:
  - `gemini_api_key`: Gemini API key (required)
  - `upload_dir`: Upload directory path
  - `vector_store_dir`: Vector store path
  - `log_level`: Logging level
  - `max_file_size`: Maximum upload size
  - `chunk_size`: Text chunk size
  - `chunk_overlap`: Chunk overlap size

#### 6. logger.py
- **Purpose**: Centralized logging
- **Functions**:
  - `setup_logger(name)`: Create configured logger
- **Features**:
  - Timestamp formatting
  - Console output
  - Configurable log levels

## Data Flow

### Document Upload Flow

```
1. User drops file in FileUpload component
2. Component validates file type and size
3. File sent to backend via POST /upload
4. Backend saves file to upload_dir
5. DocumentProcessor extracts text
6. Text split into chunks with overlap
7. Chunks embedded using Sentence Transformers
8. Embeddings stored in ChromaDB
9. Success response sent to frontend
10. StatusBar updates document count
```

### Chat Query Flow

```
1. User types question in ChatInterface
2. Question sent to backend via POST /chat
3. Backend generates query embedding
4. VectorStore searches for similar chunks (top 3)
5. Retrieved chunks sent to Gemini API with query
6. Gemini generates contextualized answer
7. Answer and sources returned to frontend
8. ChatInterface displays answer and sources
```

## Storage

### File Storage
- **Location**: `backend/uploads/`
- **Contents**: Original uploaded PDFs and PPTX files
- **Purpose**: Archive of uploaded documents

### Vector Store
- **Technology**: ChromaDB (persistent)
- **Location**: `backend/vector_store/`
- **Contents**: 
  - Document embeddings (384-dimensional vectors)
  - Document text chunks
  - Metadata (filename, chunk_id)
- **Index**: HNSW (Hierarchical Navigable Small World)

## Security Considerations

### Current Implementation
- CORS enabled for all origins (development mode)
- No authentication/authorization
- API key stored in .env file
- File type validation on upload
- File size limits enforced

### Production Recommendations
1. **Authentication**: Add JWT-based authentication
2. **CORS**: Restrict to specific origins
3. **Rate Limiting**: Implement request rate limiting
4. **Input Validation**: Enhanced input sanitization
5. **HTTPS**: Use TLS/SSL for all connections
6. **API Key Management**: Use secret management service
7. **File Scanning**: Add virus/malware scanning

## Scalability Considerations

### Current Limitations
- Single instance (no horizontal scaling)
- In-memory chat history
- Local file storage
- Single vector store instance

### Scaling Strategies
1. **Load Balancing**: Multiple backend instances with load balancer
2. **Distributed Storage**: Use S3/GCS for uploaded files
3. **Database**: PostgreSQL for metadata and chat history
4. **Vector Store**: Distributed ChromaDB or Pinecone
5. **Caching**: Redis for frequently accessed data
6. **Message Queue**: RabbitMQ/Kafka for async processing
7. **CDN**: CloudFront/Cloudflare for frontend assets

## Performance Optimization

### Current Implementation
- Chunking with overlap for context preservation
- Top-3 retrieval for context relevance
- Sentence Transformers for fast embeddings
- ChromaDB for efficient similarity search

### Optimization Opportunities
1. **Batch Processing**: Process multiple files concurrently
2. **Async I/O**: Use async file operations
3. **Caching**: Cache embeddings and responses
4. **Model Quantization**: Reduce embedding model size
5. **Connection Pooling**: Reuse HTTP connections
6. **Streaming**: Stream Gemini responses for faster UX

## Technology Stack

### Backend
- **Framework**: FastAPI 0.110.0+
- **Server**: Uvicorn (ASGI)
- **AI/ML**:
  - Google Generative AI (Gemini)
  - Sentence Transformers (embeddings)
- **Vector Database**: ChromaDB 0.4.18+
- **Document Processing**:
  - PyPDF2 (PDF)
  - python-pptx (PPTX)
- **Configuration**: Pydantic Settings
- **Environment**: python-dotenv

### Frontend
- **Framework**: React 18
- **Language**: TypeScript
- **Styling**: Tailwind CSS 3
- **HTTP Client**: Axios
- **Build Tool**: Create React App

### Development Tools
- **Version Control**: Git
- **Package Managers**: pip, npm
- **Testing**: pytest (backend), Jest (frontend)

## Future Enhancements

### Planned Features
1. **Sinhala Translation**: Multilingual support
2. **Session Management**: Persistent chat sessions
3. **Advanced Citations**: Page-level citations
4. **User Authentication**: Multi-user support
5. **Document Versioning**: Track document updates
6. **Export Functionality**: Export chat history
7. **Advanced Search**: Filtered and faceted search
8. **Analytics**: Usage statistics and insights

### Technical Improvements
1. **WebSocket Support**: Real-time updates
2. **Progressive Web App**: Offline capability
3. **Docker Compose**: Containerized deployment
4. **CI/CD Pipeline**: Automated testing and deployment
5. **Monitoring**: Prometheus + Grafana
6. **Documentation**: OpenAPI spec generation
7. **Testing**: Comprehensive test coverage
8. **Performance**: Response time optimization
