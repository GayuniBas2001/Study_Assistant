# Quick Start Guide

Get your Study Assistant up and running in 5 minutes!

## Prerequisites

✅ Python 3.8+  
✅ Node.js 16+  
✅ Gemini API key ([Get one free](https://makersuite.google.com/app/apikey))

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/GayuniBas2001/Study_Assistant.git
cd Study_Assistant
```

### 2. Set up Backend (Terminal 1)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Start backend server
python main.py
```

✅ Backend should now be running at `http://localhost:8000`

### 3. Set up Frontend (Terminal 2)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

✅ Frontend should open automatically at `http://localhost:3000`

## First Steps

### 1. Upload a Study Material
- Drag and drop a PDF or PPTX file onto the upload area
- Or click to select a file
- Wait for the upload to complete (you'll see a success message)

### 2. Ask Questions
- Type your question in the chat input box
- Press Enter or click Send
- The AI will search your materials and provide an answer
- Sources will be shown below the answer

### 3. Continue Learning
- Ask follow-up questions
- Upload more materials as needed
- Clear all documents to start fresh

## Example Questions to Try

After uploading a programming textbook:
- "What are the key concepts in Chapter 1?"
- "Explain recursion with an example"
- "What are the differences between lists and tuples?"

After uploading lecture slides:
- "Summarize the main points from Slide 5"
- "What formulas were discussed?"
- "Explain the concept presented in the introduction"

## Troubleshooting

### Backend won't start?
```bash
# Check if Python is installed
python --version

# Check if dependencies are installed
pip list

# Verify .env file exists and has GEMINI_API_KEY
cat .env
```

### Frontend won't start?
```bash
# Check if Node is installed
node --version

# Clear cache and reinstall
rm -rf node_modules
npm install
```

### Can't upload files?
- Ensure backend is running at http://localhost:8000
- Check file format (only PDF and PPTX supported)
- Check file size (max 10MB)

### Not getting good answers?
- Make sure the information is in your uploaded materials
- Try rephrasing your question
- Upload more comprehensive materials

## What's Next?

📖 Read the full [README.md](README.md) for features and details  
🔧 Check [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed setup  
🏗️ See [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system  
🚀 View [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment  

## Need Help?

- Check the [documentation](README.md)
- Look at [issues](https://github.com/GayuniBas2001/Study_Assistant/issues)
- Create a new issue if you find a bug

Happy studying! 📚✨
