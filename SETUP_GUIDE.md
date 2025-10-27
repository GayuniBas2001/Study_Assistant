# Study Assistant - Setup Guide

This guide will help you set up and run the Study Assistant application on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher**: [Download Python](https://www.python.org/downloads/)
- **Node.js 16 or higher**: [Download Node.js](https://nodejs.org/)
- **Gemini API Key**: Get your free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Quick Start

### Step 1: Clone the Repository

```bash
git clone https://github.com/GayuniBas2001/Study_Assistant.git
cd Study_Assistant
```

### Step 2: Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

This will install all necessary packages including:
- FastAPI (web framework)
- Uvicorn (ASGI server)
- Google Generative AI (Gemini API)
- ChromaDB (vector database)
- Sentence Transformers (embeddings)
- PyPDF2 (PDF processing)
- python-pptx (PPTX processing)

4. Configure environment variables:
```bash
cp .env.example .env
```

5. Edit the `.env` file and add your Gemini API key:
```
GEMINI_API_KEY=your_actual_gemini_api_key_here
UPLOAD_DIR=./uploads
VECTOR_STORE_DIR=./vector_store
LOG_LEVEL=INFO
```

6. Start the backend server:
```bash
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

The backend API is now running at `http://localhost:8000`

### Step 3: Frontend Setup

Open a new terminal window and:

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

This will install:
- React (UI framework)
- TypeScript (type safety)
- Tailwind CSS (styling)
- Axios (HTTP client)

3. Configure environment variables:
```bash
cp .env.example .env
```

The default configuration points to `http://localhost:8000` for the backend.

4. Start the frontend development server:
```bash
npm start
```

The browser will automatically open to `http://localhost:3000`

## Using the Application

### 1. Upload Study Materials

- Click the upload area or drag and drop a PDF or PPTX file
- Supported file types: `.pdf` and `.pptx`
- Maximum file size: 10MB
- Wait for the file to be processed (you'll see a success message)

### 2. Ask Questions

- Type your question in the chat input box
- Press Enter or click Send
- The AI will search through your uploaded materials and provide an answer
- Sources will be shown below the answer

### 3. Manage Documents

- View the number of indexed document chunks in the status bar
- Click "Clear All Documents" to remove all uploaded materials and start fresh

## API Documentation

Once the backend is running, you can access the interactive API documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Available Endpoints

**GET /**
- Root endpoint, returns API information

**GET /health**
- Health check endpoint
- Returns system status and document count

**POST /upload**
- Upload a PDF or PPTX file
- Form data: `file` (multipart/form-data)
- Returns: Upload status and number of chunks added

**POST /chat**
- Ask a question about uploaded materials
- Request body:
  ```json
  {
    "query": "Your question here",
    "chat_history": [
      {"role": "user", "content": "Previous question"},
      {"role": "assistant", "content": "Previous answer"}
    ]
  }
  ```
- Returns: Answer and source documents

**GET /status**
- Get system status
- Returns: Status message and document count

**DELETE /clear**
- Clear all uploaded documents and vector store
- Returns: Success message

## Troubleshooting

### Backend Issues

**Problem**: `ImportError` or missing modules
```bash
# Solution: Reinstall dependencies
pip install --upgrade -r requirements.txt
```

**Problem**: "API key not found" error
```bash
# Solution: Check your .env file
cat .env  # Should show GEMINI_API_KEY=your_key
```

**Problem**: Port 8000 already in use
```bash
# Solution: Kill the process or use a different port
# In main.py, change: uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Frontend Issues

**Problem**: `npm install` fails
```bash
# Solution: Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Problem**: "Cannot connect to backend"
```bash
# Solution: Check if backend is running and .env file is correct
# Verify REACT_APP_API_URL in frontend/.env matches backend URL
```

**Problem**: Port 3000 already in use
```bash
# Solution: Use a different port
# When prompted, type 'y' to use a different port
```

### Common Issues

**Problem**: Slow response times
- Large PDF files may take longer to process
- First query may be slower (model initialization)
- Consider chunking very large documents externally

**Problem**: Poor answer quality
- Ensure uploaded documents contain the relevant information
- Try rephrasing your question
- Upload more comprehensive study materials

**Problem**: Out of memory errors
- Too many documents uploaded
- Clear documents and upload fewer files
- Adjust chunk size in backend/config.py

## Development

### Running Tests

Backend tests:
```bash
cd backend
pytest
```

Frontend tests:
```bash
cd frontend
npm test
```

### Building for Production

Frontend production build:
```bash
cd frontend
npm run build
```

The optimized build will be in `frontend/build/`

### Docker Deployment (Optional)

Create a `Dockerfile` for the backend:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

Build and run:
```bash
docker build -t study-assistant-backend .
docker run -p 8000:8000 --env-file .env study-assistant-backend
```

## Security Notes

- Never commit your `.env` file or API keys to version control
- The `.gitignore` file is configured to exclude sensitive files
- For production deployment, use proper authentication and HTTPS
- Regularly update dependencies to patch security vulnerabilities

## Performance Tips

1. **Optimize Chunk Size**: Adjust `chunk_size` and `chunk_overlap` in `backend/config.py`
2. **Use SSD Storage**: For better vector store performance
3. **Enable Caching**: Consider implementing response caching for common queries
4. **Load Balancing**: For production, use multiple backend instances with a load balancer

## Getting Help

- Check the [README.md](README.md) for overview and features
- Review API docs at `http://localhost:8000/docs`
- Check browser console for frontend errors (F12)
- Review backend logs in the terminal

## Next Steps

- Upload your study materials (PDFs or PPTX files)
- Start asking questions about the content
- Explore the chat history feature
- Check out the planned features in README.md for upcoming enhancements

Happy studying! 📚🎓
