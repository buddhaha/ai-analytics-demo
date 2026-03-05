import axios from 'axios';
import type { QueryRequest, QueryResponse, SampleQueriesResponse, HealthResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000, // 60 seconds for AI processing
});

// Add request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('[API] Request error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`[API] Response:`, response.status);
    return response;
  },
  (error) => {
    console.error('[API] Response error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

/**
 * Send a natural language query to the AI agent
 */
export const sendQuery = async (question: string, sessionId?: string): Promise<QueryResponse> => {
  const request: QueryRequest = {
    question,
    session_id: sessionId,
  };

  const response = await api.post<QueryResponse>('/api/query', request);
  return response.data;
};

/**
 * Get sample queries that users can try
 */
export const getSampleQueries = async (): Promise<string[]> => {
  const response = await api.get<SampleQueriesResponse>('/api/sample-queries');
  return response.data.queries;
};

/**
 * Get database schema information
 */
export const getSchema = async (): Promise<string> => {
  const response = await api.get<{ success: boolean; schema: string }>('/api/schema');
  return response.data.schema;
};

/**
 * Health check endpoint
 */
export const healthCheck = async (): Promise<HealthResponse> => {
  const response = await api.get<HealthResponse>('/api/health');
  return response.data;
};

export default api;

// Made with Bob
