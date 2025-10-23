"""
Tests for document processor module
"""
import pytest
from document_processor import DocumentProcessor


class TestDocumentProcessor:
    """Test cases for DocumentProcessor class"""
    
    def test_chunk_text_basic(self):
        """Test basic text chunking"""
        text = "A" * 1500
        chunks = DocumentProcessor.chunk_text(text, chunk_size=500, overlap=100)
        
        assert len(chunks) > 0
        assert len(chunks) == 4  # 1500 chars with 500 chunk size and 100 overlap
    
    def test_chunk_text_empty(self):
        """Test chunking empty text"""
        text = ""
        chunks = DocumentProcessor.chunk_text(text, chunk_size=100, overlap=20)
        
        assert len(chunks) == 0
    
    def test_chunk_text_small(self):
        """Test chunking text smaller than chunk size"""
        text = "Small text"
        chunks = DocumentProcessor.chunk_text(text, chunk_size=100, overlap=20)
        
        assert len(chunks) == 1
        assert chunks[0] == text
    
    def test_chunk_text_overlap(self):
        """Test that chunks have proper overlap"""
        text = "0123456789" * 20  # 200 chars
        chunks = DocumentProcessor.chunk_text(text, chunk_size=50, overlap=10)
        
        # Each chunk should be 50 chars (except possibly last)
        for i, chunk in enumerate(chunks[:-1]):
            assert len(chunk) == 50
    
    def test_process_document_unsupported_format(self):
        """Test that unsupported formats raise ValueError"""
        with pytest.raises(ValueError, match="Unsupported file format"):
            DocumentProcessor.process_document("test.txt")
