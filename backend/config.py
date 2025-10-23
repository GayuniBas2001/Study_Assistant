import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application configuration settings."""
    
    gemini_api_key: str
    upload_dir: str = "./uploads"
    vector_store_dir: str = "./vector_store"
    log_level: str = "INFO"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create necessary directories
        Path(self.upload_dir).mkdir(parents=True, exist_ok=True)
        Path(self.vector_store_dir).mkdir(parents=True, exist_ok=True)

settings = Settings()
