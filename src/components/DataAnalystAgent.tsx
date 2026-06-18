/**
 * Data Analyst Agent - connects to the backend FastAPI server
 */
import { analyzeQuestion, BackendAnalysis } from '../utils/api';

export interface AnalysisResult {
  question: string;
  sql: string;
  results: any[];
  interpretation: string;
  visualization: {
    type: 'bar' | 'line' | 'pie' | 'area';
    xKey: string;
    yKey: string;
  } | null;
  timestamp: Date;
  status: 'success' | 'error';
  error?: string;
}

function mapBackendResponse(response: BackendAnalysis): AnalysisResult {
  // Map backend visualization type to frontend format
  let visualization: AnalysisResult['visualization'] = null;
  if (response.visualization) {
    const typeMap: Record<string, 'bar' | 'line' | 'pie' | 'area'> = {
      bar: 'bar',
      line: 'line',
      pie: 'pie',
      area: 'area',
      scatter: 'bar', // fallback
      histogram: 'bar', // fallback
    };

    visualization = {
      type: typeMap[response.visualization.type] || 'bar',
      xKey: response.visualization.x_key,
      yKey: response.visualization.y_key,
    };
  }

  // Build a rich interpretation from the backend's structured interpretation
  const interp = response.interpretation;
  let interpretation = interp.summary;

  // Add patterns if available
  if (interp.patterns && interp.patterns.length > 0) {
    interpretation += '\n\nPatterns detected:\n• ' + interp.patterns.join('\n• ');
  }

  // Add anomalies if available
  if (interp.anomalies && interp.anomalies.length > 0) {
    interpretation += '\n\nAnomalies found:\n• ' + interp.anomalies.join('\n• ');
  }

  // Add recommendations if available
  if (interp.recommendations && interp.recommendations.length > 0) {
    interpretation += '\n\nRecommendations:\n• ' + interp.recommendations.join('\n• ');
  }

  return {
    question: response.question,
    sql: response.sql_generation.sql,
    results: response.query_result.rows,
    interpretation,
    visualization,
    timestamp: new Date(response.timestamp),
    status: 'success',
  };
}

export class DataAnalystAgent {
  async analyze(question: string): Promise<AnalysisResult> {
    try {
      const backendResponse = await analyzeQuestion(question);
      return mapBackendResponse(backendResponse);
    } catch (error: any) {
      // If the backend is unavailable, provide a clear error
      if (error.code === 'ERR_NETWORK' || error.message?.includes('Network Error')) {
        throw new Error(
          'Cannot connect to the backend server. ' +
          'Please ensure the backend is running (see backend/README_BACKEND.md).'
        );
      }

      // Pass through API errors
      if (error.response?.data?.detail) {
        throw new Error(error.response.data.detail);
      }

      // Generic error
      throw new Error(
        error instanceof Error
          ? error.message
          : 'An unexpected error occurred while analyzing your question.'
      );
    }
  }
}
