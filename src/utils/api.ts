/**
 * API client for the Data Analyst Agent backend
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 seconds for analysis requests
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface BackendAnalysisQuestion {
  question: string;
  conversation_id?: string;
  context?: Record<string, any>;
  user_id?: string;
}

export interface BackendSQLGeneration {
  sql: string;
  confidence: number;
  pattern_type: string;
  explanation: string;
}

export interface BackendQueryResult {
  query_id: string;
  status: string;
  rows: Record<string, any>[];
  row_count: number;
  execution_time_ms: number;
  error?: string;
}

export interface BackendVisualization {
  type: string;
  title: string;
  x_axis: string;
  y_axis: string;
  x_key: string;
  y_key: string;
  image_base64?: string;
  image_url?: string;
  interactive_html?: string;
}

export interface BackendInterpretation {
  summary: string;
  key_metrics: Record<string, any>;
  patterns: string[];
  anomalies: string[];
  recommendations: string[];
  next_steps: string[];
  confidence: number;
}

export interface BackendAnalysis {
  analysis_id: string;
  timestamp: string;
  question: string;
  sql_generation: BackendSQLGeneration;
  query_result: BackendQueryResult;
  visualization?: BackendVisualization;
  interpretation: BackendInterpretation;
  execution_time_ms: number;
}

export interface BackendSchema {
  tables: {
    table_name: string;
    columns: { name: string; type: string; nullable: boolean }[];
    row_count: number;
  }[];
  database_type: string;
  total_tables: number;
}

export interface HealthStatus {
  status: string;
  timestamp: string;
  database_connection: boolean;
  llm_connection: boolean;
  message?: string;
}

/**
 * Analyze a natural language question
 */
export async function analyzeQuestion(question: string, userId?: string): Promise<BackendAnalysis> {
  const payload: BackendAnalysisQuestion = {
    question,
    user_id: userId || 'web-user',
  };

  const response = await apiClient.post<BackendAnalysis>('/analyze', payload);
  return response.data;
}

/**
 * Execute a raw SQL query
 */
export async function executeQuery(sql: string): Promise<{
  success: boolean;
  data: Record<string, any>[];
  row_count: number;
  columns: string[];
}> {
  const response = await apiClient.post('/query/execute', { sql });
  return response.data;
}

/**
 * Get database schema
 */
export async function getSchema(): Promise<BackendSchema> {
  const response = await apiClient.get<BackendSchema>('/schema');
  return response.data;
}

/**
 * Check API health
 */
export async function checkHealth(): Promise<HealthStatus> {
  const response = await apiClient.get<HealthStatus>('/health');
  return response.data;
}

/**
 * Get API info
 */
export async function getApiInfo(): Promise<{
  title: string;
  version: string;
  description: string;
  health: HealthStatus;
}> {
  const response = await apiClient.get('/info');
  return response.data;
}

export default apiClient;
