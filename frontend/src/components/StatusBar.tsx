import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';

interface StatusBarProps {
  refreshTrigger: number;
}

const StatusBar: React.FC<StatusBarProps> = ({ refreshTrigger }) => {
  const [documentCount, setDocumentCount] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await apiService.getStatus();
        setDocumentCount(response.document_count);
      } catch (error) {
        console.error('Failed to fetch status', error);
      } finally {
        setLoading(false);
      }
    };

    fetchStatus();
  }, [refreshTrigger]);

  const handleClearDocuments = async () => {
    if (window.confirm('Are you sure you want to clear all documents? This action cannot be undone.')) {
      try {
        await apiService.clearDocuments();
        setDocumentCount(0);
        window.location.reload();
      } catch (error) {
        console.error('Failed to clear documents', error);
      }
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-4 flex items-center justify-between">
      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-2">
          <div className={`w-3 h-3 rounded-full ${loading ? 'bg-yellow-500' : 'bg-green-500'}`}></div>
          <span className="text-sm font-medium text-gray-700">
            {loading ? 'Connecting...' : 'Connected'}
          </span>
        </div>
        <div className="h-6 w-px bg-gray-300"></div>
        <div className="flex items-center space-x-2">
          <svg className="h-5 w-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <span className="text-sm text-gray-700">
            <span className="font-semibold">{documentCount}</span> document chunks indexed
          </span>
        </div>
      </div>
      
      {documentCount > 0 && (
        <button
          onClick={handleClearDocuments}
          className="text-sm text-red-600 hover:text-red-700 px-3 py-1 rounded hover:bg-red-50 transition-colors"
        >
          Clear All Documents
        </button>
      )}
    </div>
  );
};

export default StatusBar;
