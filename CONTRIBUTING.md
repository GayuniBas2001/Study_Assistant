# Contributing to Study Assistant

Thank you for your interest in contributing to Study Assistant! This document provides guidelines and instructions for contributing.

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Making Changes](#making-changes)
5. [Submitting Changes](#submitting-changes)
6. [Coding Standards](#coding-standards)
7. [Testing](#testing)
8. [Documentation](#documentation)

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in your interactions.

### Our Standards

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- Git
- Basic understanding of FastAPI and React

### Finding Issues to Work On

1. Check the [Issues](https://github.com/GayuniBas2001/Study_Assistant/issues) page
2. Look for issues labeled `good first issue` or `help wanted`
3. Comment on the issue to let others know you're working on it

## Development Setup

1. **Fork the repository**
   - Click the "Fork" button on GitHub
   - Clone your fork locally

2. **Set up the backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Add your GEMINI_API_KEY to .env
```

3. **Set up the frontend**
```bash
cd frontend
npm install
cp .env.example .env
```

4. **Create a new branch**
```bash
git checkout -b feature/your-feature-name
```

## Making Changes

### Backend Changes

**File Structure:**
```
backend/
├── main.py              # FastAPI app and endpoints
├── config.py            # Configuration management
├── document_processor.py # Document processing
├── vector_store.py      # Vector database operations
├── gemini_rag.py        # RAG implementation
├── logger.py            # Logging setup
└── requirements.txt     # Python dependencies
```

**Adding a new endpoint:**
```python
@app.post("/your-endpoint")
async def your_endpoint(request: YourRequest):
    """Endpoint description."""
    try:
        # Your logic here
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
```

### Frontend Changes

**File Structure:**
```
frontend/src/
├── components/          # React components
│   ├── FileUpload.tsx
│   ├── ChatInterface.tsx
│   └── StatusBar.tsx
├── services/
│   └── api.ts          # API service
├── App.tsx             # Main app component
└── index.tsx           # Entry point
```

**Adding a new component:**
```typescript
import React from 'react';

interface YourComponentProps {
  // Define props
}

const YourComponent: React.FC<YourComponentProps> = (props) => {
  return (
    <div className="your-classes">
      {/* Your JSX */}
    </div>
  );
};

export default YourComponent;
```

## Submitting Changes

### Before Submitting

1. **Test your changes**
```bash
# Backend
cd backend
python test_api.py

# Frontend
cd frontend
npm test
```

2. **Format your code**
```bash
# Backend (install black first: pip install black)
black backend/*.py

# Frontend (install prettier first: npm install -g prettier)
prettier --write "frontend/src/**/*.{ts,tsx}"
```

3. **Update documentation**
   - Update README.md if needed
   - Add comments to complex code
   - Update ARCHITECTURE.md for architectural changes

### Pull Request Process

1. **Commit your changes**
```bash
git add .
git commit -m "feat: add your feature description"
```

Commit message format:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

2. **Push to your fork**
```bash
git push origin feature/your-feature-name
```

3. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill in the PR template

### Pull Request Template

```markdown
## Description
Brief description of your changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe the tests you ran

## Checklist
- [ ] My code follows the project's coding standards
- [ ] I have added tests for my changes
- [ ] I have updated the documentation
- [ ] All tests pass locally
- [ ] I have checked for security vulnerabilities
```

## Coding Standards

### Python (Backend)

**Style Guide:** Follow PEP 8

```python
# Good
def process_document(file_path: str) -> str:
    """
    Process document and extract text.
    
    Args:
        file_path: Path to the document
        
    Returns:
        Extracted text
    """
    logger.info(f"Processing {file_path}")
    # Implementation
    return text

# Bad
def processDocument(filePath):
    # No docstring, no type hints
    pass
```

**Key Points:**
- Use type hints
- Add docstrings to all functions
- Use descriptive variable names
- Keep functions focused and small
- Handle exceptions appropriately
- Log important operations

### TypeScript/React (Frontend)

**Style Guide:** Follow Airbnb React/JSX Style Guide

```typescript
// Good
interface ButtonProps {
  onClick: () => void;
  label: string;
  disabled?: boolean;
}

const Button: React.FC<ButtonProps> = ({ onClick, label, disabled = false }) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className="btn btn-primary"
    >
      {label}
    </button>
  );
};

// Bad
const Button = (props) => {
  return <button onClick={props.onClick}>{props.label}</button>
}
```

**Key Points:**
- Use TypeScript for type safety
- Define interfaces for props
- Use functional components with hooks
- Follow Tailwind CSS conventions
- Use meaningful component names
- Keep components focused

### Git Commit Messages

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Example:**
```
feat(chat): add conversation history support

- Store last 5 messages in chat history
- Pass history to Gemini API for context
- Display chat history in UI

Closes #123
```

## Testing

### Backend Tests

Create tests in `backend/tests/`:

```python
import pytest
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
```

Run tests:
```bash
cd backend
pytest
```

### Frontend Tests

Create tests alongside components:

```typescript
import { render, screen } from '@testing-library/react';
import FileUpload from './FileUpload';

test('renders file upload component', () => {
  render(<FileUpload onUploadSuccess={() => {}} onUploadError={() => {}} />);
  expect(screen.getByText(/Upload Study Materials/i)).toBeInTheDocument();
});
```

Run tests:
```bash
cd frontend
npm test
```

## Documentation

### Code Documentation

**Python:**
```python
def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Split text into overlapping chunks.
    
    Args:
        text: The text to chunk
        chunk_size: Size of each chunk in characters
        overlap: Number of characters to overlap between chunks
        
    Returns:
        List of text chunks
        
    Raises:
        ValueError: If chunk_size is less than overlap
        
    Example:
        >>> chunks = chunk_text("long text...", 100, 20)
        >>> len(chunks)
        5
    """
    # Implementation
```

**TypeScript:**
```typescript
/**
 * Upload a file to the backend
 * 
 * @param file - The file to upload
 * @returns Promise with upload response
 * @throws Error if upload fails
 * 
 * @example
 * ```typescript
 * const response = await uploadFile(myFile);
 * console.log(response.filename);
 * ```
 */
async function uploadFile(file: File): Promise<UploadResponse> {
  // Implementation
}
```

### README Updates

When adding features:
1. Update feature list in README.md
2. Add usage examples if needed
3. Update architecture diagram if structure changes

### API Documentation

Document API changes in code:
```python
@app.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """
    Upload and process a PDF or PPTX file.
    
    This endpoint:
    1. Validates the file type
    2. Extracts text from the document
    3. Chunks the text
    4. Generates embeddings
    5. Stores in vector database
    
    Args:
        file: PDF or PPTX file to upload
        
    Returns:
        UploadResponse with status and metadata
        
    Raises:
        HTTPException: 400 if file type invalid
        HTTPException: 500 if processing fails
    """
```

## Feature Requests

### Proposing New Features

1. Open an issue with the `feature request` label
2. Describe the feature and use case
3. Explain why it's valuable
4. Provide examples if possible

### Feature Development Process

1. Discussion in issue
2. Design review if needed
3. Implementation
4. Testing
5. Documentation
6. Pull request

## Security

### Reporting Security Issues

**DO NOT** create public issues for security vulnerabilities.

Email security concerns to: [Create a SECURITY.md]

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Security Best Practices

- Validate all user inputs
- Never commit API keys or secrets
- Use parameterized queries
- Sanitize file uploads
- Keep dependencies updated
- Follow OWASP guidelines

## Release Process

1. Version bump in package.json and appropriate files
2. Update CHANGELOG.md
3. Create release notes
4. Tag the release
5. Deploy to production

## Getting Help

- **Questions:** Open a GitHub issue with the `question` label
- **Bugs:** Open a GitHub issue with the `bug` label
- **Features:** Open a GitHub issue with the `feature request` label
- **Security:** Email (see Security section)

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in commit history

Thank you for contributing to Study Assistant! 🎉
