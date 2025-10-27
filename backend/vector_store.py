import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
from config import settings
from logger import logger

class VectorStore:
    """Manage vector embeddings and similarity search using ChromaDB."""
    
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = chromadb.PersistentClient(
            path=settings.vector_store_dir,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        self.collection_name = "study_documents"
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        logger.info(f"Initialized VectorStore with collection: {self.collection_name}")
    
    def add_documents(self, chunks: List[str], metadata: List[Dict[str, Any]] = None):
        """Add document chunks to the vector store."""
        try:
            logger.info(f"Adding {len(chunks)} documents to vector store")
            
            if not chunks:
                logger.warning("No chunks to add")
                return
            
            # Generate embeddings
            embeddings = self.embedding_model.encode(chunks).tolist()
            
            # Generate IDs
            existing_count = self.collection.count()
            ids = [f"doc_{existing_count + i}" for i in range(len(chunks))]
            
            # Prepare metadata
            if metadata is None:
                metadata = [{"chunk_id": i} for i in range(len(chunks))]
            
            # Add to collection
            self.collection.add(
                embeddings=embeddings,
                documents=chunks,
                metadatas=metadata,
                ids=ids
            )
            
            logger.info(f"Successfully added {len(chunks)} documents to vector store")
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {str(e)}")
            raise
    
    def search(self, query: str, n_results: int = 3) -> Dict[str, Any]:
        """Search for similar documents."""
        try:
            logger.info(f"Searching for: {query}")
            
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query]).tolist()
            
            # Search in collection
            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=n_results
            )
            
            logger.info(f"Found {len(results.get('documents', [[]])[0])} results")
            return results
        except Exception as e:
            logger.error(f"Error searching vector store: {str(e)}")
            raise
    
    def clear_collection(self):
        """Clear all documents from the collection."""
        try:
            logger.info("Clearing vector store collection")
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("Vector store cleared successfully")
        except Exception as e:
            logger.error(f"Error clearing vector store: {str(e)}")
            raise
    
    def get_collection_count(self) -> int:
        """Get the number of documents in the collection."""
        return self.collection.count()
