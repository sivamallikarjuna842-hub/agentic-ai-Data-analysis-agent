"""
Data models for the Data Analyst Agent
"""
from datetime import datetime
from typing import Optional, List, Any, Dict
from pydantic import BaseModel, Field
from enum import Enum

# ============================================================================
# Request/Response Models
# ============================================================================

class ChartType(str, Enum):
    """Supported chart types"""
    BAR = "bar"
    LINE = "line"
    PIE = "pie"
    AREA = "area"
    SCATTER = "scatter"
    HISTOGRAM = "histogram"

class QueryStatus(str, Enum):
    """Query execution status"""
    PENDING = "pending"
    EXECUTING = "executing"
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"

# ============================================================================
# Analysis Models
# ============================================================================

class AnalysisQuestion(BaseModel):
    """Natural language question about data"""
    question: str = Field(..., min_length=10, max_length=1000)
    conversation_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    user_id: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What were the total sales by product category in Q4?",
                "conversation_id": "conv_123",
                "context": {"time_period": "Q4 2024"}
            }
        }

class SQLGeneration(BaseModel):
    """Generated SQL query"""
    sql: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    pattern_type: str
    explanation: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "sql": "SELECT category, SUM(revenue) as total FROM sales GROUP BY category",
                "confidence": 0.95,
                "pattern_type": "revenue_by_category",
                "explanation": "Query groups sales by category and sums revenue"
            }
        }

class QueryResult(BaseModel):
    """Query execution result"""
    query_id: str
    status: QueryStatus
    rows: List[Dict[str, Any]]
    row_count: int
    execution_time_ms: float
    error: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "query_id": "q_123",
                "status": "success",
                "rows": [{"category": "Electronics", "total": 15000}],
                "row_count": 1,
                "execution_time_ms": 45.3
            }
        }

class Visualization(BaseModel):
    """Chart visualization"""
    type: ChartType
    title: str
    x_axis: str
    y_axis: str
    x_key: str
    y_key: str
    image_base64: Optional[str] = None
    image_url: Optional[str] = None
    interactive_html: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "type": "bar",
                "title": "Sales by Category",
                "x_axis": "Product Category",
                "y_axis": "Total Revenue",
                "x_key": "category",
                "y_key": "total_revenue"
            }
        }

class Interpretation(BaseModel):
    """AI-generated interpretation of data"""
    summary: str = Field(...)
    key_metrics: Dict[str, Any]
    patterns: List[str]
    anomalies: List[str]
    recommendations: List[str]
    next_steps: List[str]
    confidence: float = Field(..., ge=0.0, le=1.0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "summary": "Analysis reveals Electronics category dominates with 60% of total revenue...",
                "key_metrics": {
                    "total_revenue": 50000,
                    "average_transaction": 1250,
                    "top_category": "Electronics"
                },
                "patterns": ["Strong Electronics demand", "Weekend sales spike"],
                "anomalies": ["Unexpected drop on Jan 15"],
                "recommendations": ["Increase Electronics inventory", "Target SMB segment"],
                "next_steps": ["Drill into top products", "Analyze seasonal trends"]
            }
        }

class Analysis(BaseModel):
    """Complete analysis result"""
    analysis_id: str
    timestamp: datetime
    question: str
    sql_generation: SQLGeneration
    query_result: QueryResult
    visualization: Optional[Visualization] = None
    interpretation: Interpretation
    execution_time_ms: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "analysis_id": "a_123",
                "timestamp": "2024-01-15T10:30:00Z",
                "question": "What were total sales by category?",
                "sql_generation": {},
                "query_result": {},
                "visualization": {},
                "interpretation": {},
                "execution_time_ms": 250
            }
        }

# ============================================================================
# Database Schema Models
# ============================================================================

class DatabaseSchema(BaseModel):
    """Database schema information"""
    table_name: str
    columns: List[Dict[str, str]]  # {name, type, nullable}
    row_count: int
    indexes: List[str]

class SchemaInfo(BaseModel):
    """Complete schema information"""
    tables: List[DatabaseSchema]
    database_type: str
    total_tables: int

# ============================================================================
# Conversation Models
# ============================================================================

class ConversationMessage(BaseModel):
    """Message in conversation"""
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime
    analysis_id: Optional[str] = None

class Conversation(BaseModel):
    """Conversation with multiple analyses"""
    conversation_id: str
    user_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    messages: List[ConversationMessage]
    analyses: List[str]  # analysis IDs

# ============================================================================
# Statistics Models
# ============================================================================

class DataStatistics(BaseModel):
    """Data statistics"""
    total_rows: int
    column_count: int
    numeric_columns: List[str]
    categorical_columns: List[str]
    date_columns: List[str]
    null_counts: Dict[str, int]
    unique_counts: Dict[str, int]

class QueryStatistics(BaseModel):
    """Query statistics"""
    total_queries: int
    successful_queries: int
    failed_queries: int
    average_execution_time_ms: float
    most_common_pattern: str

# ============================================================================
# Health/Status Models
# ============================================================================

class HealthStatus(BaseModel):
    """API health status"""
    status: str  # "healthy", "degraded", "unhealthy"
    timestamp: datetime
    database_connection: bool
    llm_connection: bool
    message: Optional[str] = None

class APIInfo(BaseModel):
    """API information"""
    title: str
    version: str
    description: str
    health: HealthStatus

# ============================================================================
# Error Models
# ============================================================================

class ErrorDetail(BaseModel):
    """Error details"""
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime
    request_id: Optional[str] = None

class ValidationError(BaseModel):
    """Validation error"""
    field: str
    message: str
    value: Optional[Any] = None
