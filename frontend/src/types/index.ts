// API Types

export interface QueryRequest {
  question: string;
  session_id?: string;
}

export interface QueryResponse {
  success: boolean;
  question: string;
  sql: string | null;
  results: Record<string, any>[];
  analysis: string;
  visualization: VisualizationConfig;
  row_count: number;
  error?: string;
}

export interface VisualizationConfig {
  type: 'bar' | 'line' | 'pie' | 'table' | 'none';
  data?: Record<string, any>[];
  columns?: string[];
  xAxis?: string;
  yAxis?: string;
  nameKey?: string;
  valueKey?: string;
}

export interface SampleQueriesResponse {
  success: boolean;
  queries: string[];
}

export interface HealthResponse {
  status: string;
  service: string;
  version: string;
}

// UI State Types

export interface QueryHistoryItem {
  id: string;
  question: string;
  timestamp: Date;
  response: QueryResponse;
}

export interface AppState {
  isLoading: boolean;
  error: string | null;
  currentQuery: string;
  currentResponse: QueryResponse | null;
  history: QueryHistoryItem[];
  sampleQueries: string[];
}

// Made with Bob
