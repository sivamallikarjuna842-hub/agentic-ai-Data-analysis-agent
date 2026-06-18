"""
FastAPI application for Data Analyst Agent
"""
import logging
import time
from datetime import datetime
from typing import Dict, Any, List
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from config import config
from models import (
    AnalysisQuestion, Analysis, HealthStatus, APIInfo, ErrorDetail,
    SchemaInfo, QueryResult
)
from database import get_db_manager, get_db_session
from agent import get_agent

# Configure logging
logging.basicConfig(
    level=config.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# Startup/Shutdown Events
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    # Startup
    logger.info("Starting Data Analyst Agent API...")
    
    # Test database connection
    db_manager = get_db_manager()
    if db_manager.test_connection():
        logger.info("✓ Database connected successfully")
    else:
        logger.warning("⚠ Database connection test failed")
    
    # Initialize agent
    try:
        agent = get_agent()
        logger.info("✓ Agent initialized successfully")
    except Exception as e:
        logger.error(f"✗ Agent initialization failed: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Data Analyst Agent API...")

# ============================================================================
# Create FastAPI App
# ============================================================================

app = FastAPI(
    title=config.API_TITLE,
    description=config.API_DESCRIPTION,
    version=config.API_VERSION,
    lifespan=lifespan
)

# ============================================================================
# Middleware
# ============================================================================

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Request ID middleware
@app.middleware("http")
async def add_request_id(request, call_next):
    """Add request ID for tracing"""
    request_id = f"req_{int(time.time() * 1000)}"
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Handle validation errors"""
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": [
                {
                    "field": str(error["loc"]),
                    "message": error["msg"],
                    "type": error["type"]
                }
                for error in exc.errors()
            ]
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error_code": "INTERNAL_ERROR",
            "message": "An unexpected error occurred",
            "timestamp": datetime.now().isoformat()
        }
    )

# ============================================================================
# Health & Status Endpoints
# ============================================================================

@app.get("/health", response_model=HealthStatus)
async def health_check():
    """Check API health status"""
    db_manager = get_db_manager()
    
    return HealthStatus(
        status="healthy",
        timestamp=datetime.now(),
        database_connection=db_manager.test_connection(),
        llm_connection=True,  # Would test LLM connection in production
        message="All systems operational"
    )

@app.get("/info", response_model=APIInfo)
async def api_info():
    """Get API information"""
    health = await health_check()
    
    return APIInfo(
        title=config.API_TITLE,
        version=config.API_VERSION,
        description=config.API_DESCRIPTION,
        health=health
    )

# ============================================================================
# Database Endpoints
# ============================================================================

@app.get("/schema", response_model=SchemaInfo)
async def get_schema():
    """Get database schema information"""
    try:
        db_manager = get_db_manager()
        schema = db_manager.get_schema()
        
        return SchemaInfo(
            tables=[
                {
                    "table_name": t["name"],
                    "columns": t["columns"],
                    "row_count": t["row_count"],
                    "indexes": []
                }
                for t in schema.get("tables", [])
            ],
            database_type=schema.get("database_type", "unknown"),
            total_tables=len(schema.get("tables", []))
        )
    except Exception as e:
        logger.error(f"Schema retrieval error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query/execute")
async def execute_query(request: Dict[str, Any]):
    """Execute raw SQL query"""
    try:
        sql = request.get("sql", "").strip()
        
        if not sql:
            raise HTTPException(status_code=400, detail="SQL query is required")
        
        # Security check - prevent dangerous operations
        dangerous_keywords = ["DROP", "DELETE", "TRUNCATE", "ALTER", "CREATE"]
        if any(keyword in sql.upper() for keyword in dangerous_keywords):
            raise HTTPException(status_code=403, detail="Operation not allowed")
        
        db_manager = get_db_manager()
        result = db_manager.execute_query(sql)
        
        if result["success"]:
            return {
                "success": True,
                "data": result["data"],
                "row_count": result["row_count"],
                "columns": result["columns"]
            }
        else:
            raise HTTPException(status_code=400, detail=result.get("error"))
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Query execution error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# Analysis Endpoints
# ============================================================================

@app.post("/analyze", response_model=Analysis)
async def analyze_question(
    request: AnalysisQuestion,
    background_tasks: BackgroundTasks
):
    """
    Analyze a natural language question about data
    
    This endpoint:
    1. Converts the question to SQL
    2. Executes the query
    3. Analyzes the results
    4. Creates visualizations
    5. Generates insights
    """
    try:
        # Validate input
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        # Get agent
        agent = get_agent()
        
        # Run analysis
        analysis = await agent.analyze(
            question=request.question,
            user_id=request.user_id
        )
        
        logger.info(
            f"Analysis complete: {analysis.analysis_id} "
            f"({analysis.execution_time_ms:.0f}ms)"
        )
        
        return analysis
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

@app.post("/analyze/batch")
async def batch_analyze(
    requests: List[AnalysisQuestion],
    background_tasks: BackgroundTasks
):
    """
    Analyze multiple questions
    """
    try:
        agent = get_agent()
        results = []
        
        for req in requests:
            analysis = await agent.analyze(
                question=req.question,
                user_id=req.user_id
            )
            results.append(analysis)
        
        return {
            "total": len(results),
            "analyses": results,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Batch analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# Conversation Endpoints
# ============================================================================

@app.post("/conversation/create")
async def create_conversation(user_id: str = None):
    """Create new conversation"""
    from uuid import uuid4
    
    conversation_id = str(uuid4())
    
    return {
        "conversation_id": conversation_id,
        "user_id": user_id,
        "created_at": datetime.now().isoformat(),
        "messages": []
    }

@app.post("/conversation/{conversation_id}/message")
async def send_message(
    conversation_id: str,
    message: AnalysisQuestion
):
    """Send message in conversation"""
    try:
        agent = get_agent()
        
        analysis = await agent.analyze(
            question=message.question,
            user_id=message.user_id
        )
        
        return {
            "conversation_id": conversation_id,
            "message": message.question,
            "response": analysis,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Message error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# Statistics Endpoints
# ============================================================================

@app.get("/stats/queries")
async def query_stats():
    """Get query execution statistics"""
    # In production, would track actual stats
    return {
        "total_queries": 0,
        "successful_queries": 0,
        "failed_queries": 0,
        "average_execution_time_ms": 0,
        "most_common_pattern": "unknown"
    }

@app.get("/stats/analysis")
async def analysis_stats():
    """Get analysis statistics"""
    return {
        "total_analyses": 0,
        "average_execution_time_ms": 0,
        "most_common_question_type": "unknown",
        "total_data_points_analyzed": 0
    }

# ============================================================================
# Root Endpoints
# ============================================================================

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": config.API_TITLE,
        "version": config.API_VERSION,
        "status": "running",
        "endpoints": {
            "health": "/health",
            "info": "/info",
            "schema": "/schema",
            "analyze": "/analyze",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

@app.get("/docs-custom")
async def custom_docs():
    """Custom documentation"""
    return {
        "title": config.API_TITLE,
        "description": config.API_DESCRIPTION,
        "endpoints": [
            {
                "path": "/analyze",
                "method": "POST",
                "description": "Analyze natural language question",
                "request": {
                    "question": "string",
                    "conversation_id": "string (optional)",
                    "context": "object (optional)"
                }
            },
            {
                "path": "/query/execute",
                "method": "POST",
                "description": "Execute SQL query"
            },
            {
                "path": "/schema",
                "method": "GET",
                "description": "Get database schema"
            }
        ]
    }

# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host=config.HOST,
        port=config.PORT,
        log_level=config.LOG_LEVEL.lower(),
        reload=config.DEBUG
    )
