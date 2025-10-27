# Study Assistant

A RAG-based Study Support Chatbot powered by Gemini AI. Upload PDF or PPTX study materials and ask questions to get AI-generated answers based on your documents.

## Features

- 📄 **Document Upload**: Support for PDF and PPTX files
- 🤖 **AI-Powered Chat**: Get answers from your study materials using Gemini AI
- 🔍 **Vector Search**: Fast and accurate retrieval using ChromaDB
- 💬 **Interactive Chat**: Clean and intuitive chat interface
- 📊 **Source Citations**: See which documents were used to generate answers
- 🎨 **Modern UI**: Built with React and Tailwind CSS

## Architecture

### Backend (FastAPI)
- **File Processing**: Extract text from PDF and PPTX files
- **Text Chunking**: Split documents into manageable chunks with overlap
- **Vector Embeddings**: Generate embeddings using Sentence Transformers
- **Vector Storage**: Store and search embeddings with ChromaDB
- **RAG System**: Generate answers using Gemini API with retrieved context
- **API Endpoints**: RESTful API for upload, chat, and status

### Frontend (React + Tailwind)
- **File Upload**: Drag-and-drop interface for uploading documents
- **Chat Interface**: Real-time chat with message history
- **Status Dashboard**: Monitor indexed documents
- **Responsive Design**: Works on desktop and mobile

## Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- Gemini API key (get from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file from the example:
```bash
cp .env.example .env
```

5. Edit `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your_actual_api_key_here
```

6. Run the backend server:
```bash
python main.py
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file from the example:
```bash
cp .env.example .env
```

4. Run the frontend development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## Usage

1. **Start both servers** (backend and frontend)
2. **Open your browser** to `http://localhost:3000`
3. **Upload study materials**: Drag and drop or click to upload PDF or PPTX files
4. **Ask questions**: Type your questions in the chat interface
5. **Get answers**: The AI will respond based on your uploaded materials

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

### Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /upload` - Upload a PDF or PPTX file
- `POST /chat` - Ask a question
- `GET /status` - Get system status
- `DELETE /clear` - Clear all documents

## Configuration

### Backend Environment Variables
- `GEMINI_API_KEY` - Your Gemini API key (required)
- `UPLOAD_DIR` - Directory for uploaded files (default: `./uploads`)
- `VECTOR_STORE_DIR` - Directory for vector store (default: `./vector_store`)
- `LOG_LEVEL` - Logging level (default: `INFO`)

### Frontend Environment Variables
- `REACT_APP_API_URL` - Backend API URL (default: `http://localhost:8000`)

## Documentation

- 📖 **[Quick Start Guide](QUICK_START.md)** - Get running in 5 minutes
- 🔧 **[Setup Guide](SETUP_GUIDE.md)** - Detailed installation instructions
- 🏗️ **[Architecture](ARCHITECTURE.md)** - System design and components
- 🚀 **[Deployment Guide](DEPLOYMENT.md)** - Production deployment options
- 🤝 **[Contributing](CONTRIBUTING.md)** - How to contribute to the project
- 📊 **[Project Summary](PROJECT_SUMMARY.md)** - Complete project overview

## Future Enhancements

- 🌐 **Sinhala Translation**: Support for Sinhala language queries and responses
- 📚 **Citation Details**: More detailed source citations with page numbers
- 💾 **Session Memory**: Persistent chat history across sessions
- 🔐 **User Authentication**: Multi-user support with authentication
- 📱 **Mobile App**: Native mobile applications
- 🎯 **Advanced Search**: More sophisticated retrieval strategies

## Technology Stack

### Backend
- FastAPI - Web framework
- Gemini API - Language model
- ChromaDB - Vector database
- Sentence Transformers - Embeddings
- PyPDF2 - PDF processing
- python-pptx - PPTX processing

### Frontend
- React - UI framework
- TypeScript - Type safety
- Tailwind CSS - Styling
- Axios - HTTP client

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
