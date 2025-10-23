import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatResponse {
  answer: string;
  sources: string[];
}

export interface UploadResponse {
  status: string;
  message: string;
  filename: string;
  chunks_added: number;
}

export interface StatusResponse {
  status: string;
  message: string;
  document_count: number;
}

class ApiService {
  private baseURL: string;

  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async uploadFile(file: File): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(`${this.baseURL}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  }

  async chat(query: string, chatHistory?: ChatMessage[]): Promise<ChatResponse> {
    const response = await axios.post(`${this.baseURL}/chat`, {
      query,
      chat_history: chatHistory,
    });

    return response.data;
  }

  async getStatus(): Promise<StatusResponse> {
    const response = await axios.get(`${this.baseURL}/status`);
    return response.data;
  }

  async clearDocuments(): Promise<{ status: string; message: string }> {
    const response = await axios.delete(`${this.baseURL}/clear`);
    return response.data;
  }

  async healthCheck(): Promise<{ status: string; documents_indexed: number }> {
    const response = await axios.get(`${this.baseURL}/health`);
    return response.data;
  }
}

export const apiService = new ApiService();
