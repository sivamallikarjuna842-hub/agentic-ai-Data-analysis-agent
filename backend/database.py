"""
Database connection and management
"""
import sqlite3
import logging
from typing import List, Dict, Any, Optional
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import pandas as pd
from config import config

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages database connections and queries"""
    
    def __init__(self):
        """Initialize database manager"""
        self.db_url = config.get_database_url()
        self.engine = None
        self.SessionLocal = None
        self._init_engine()
    
    def _init_engine(self):
        """Initialize SQLAlchemy engine"""
        try:
            if "sqlite" in self.db_url:
                # SQLite specific configuration
                self.engine = create_engine(
                    self.db_url,
                    connect_args={"check_same_thread": False},
                    poolclass=StaticPool,
                    echo=config.DEBUG
                )
            else:
                # PostgreSQL or other databases
                self.engine = create_engine(
                    self.db_url,
                    pool_pre_ping=True,
                    pool_size=10,
                    max_overflow=20,
                    echo=config.DEBUG
                )
            
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            logger.info(f"Database connected: {self.db_url}")
        
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def get_session(self) -> Session:
        """Get database session"""
        return self.SessionLocal()
    
    def execute_query(
        self,
        query: str,
        timeout: Optional[int] = None,
        limit: int = 1000
    ) -> Dict[str, Any]:
        """
        Execute SQL query safely
        
        Args:
            query: SQL query string
            timeout: Query timeout in seconds
            limit: Maximum rows to return
            
        Returns:
            Dictionary with results and metadata
        """
        timeout = timeout or config.MAX_QUERY_TIMEOUT
        limit = min(limit, config.MAX_QUERY_LIMIT)
        
        try:
            # Add LIMIT if not present
            if "LIMIT" not in query.upper():
                query = f"{query} LIMIT {limit}"
            
            # Execute query
            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                columns = result.keys()
                rows = result.fetchall()
                
                # Convert to list of dicts
                data = [dict(zip(columns, row)) for row in rows]
                
                return {
                    "success": True,
                    "data": data,
                    "row_count": len(data),
                    "columns": list(columns)
                }
        
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Query execution error: {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "data": [],
                "row_count": 0
            }
    
    def get_schema(self) -> Dict[str, Any]:
        """Get database schema information"""
        try:
            inspector = inspect(self.engine)
            
            tables_info = []
            for table_name in inspector.get_table_names():
                columns = []
                for col in inspector.get_columns(table_name):
                    columns.append({
                        "name": col["name"],
                        "type": str(col["type"]),
                        "nullable": col.get("nullable", True)
                    })
                
                # Get row count
                try:
                    with self.engine.connect() as conn:
                        result = conn.execute(
                            text(f"SELECT COUNT(*) FROM {table_name}")
                        )
                        row_count = result.scalar()
                except:
                    row_count = 0
                
                tables_info.append({
                    "name": table_name,
                    "columns": columns,
                    "row_count": row_count
                })
            
            return {
                "tables": tables_info,
                "database_type": self.db_url.split(":")[0]
            }
        
        except Exception as e:
            logger.error(f"Schema inspection error: {e}")
            return {"tables": [], "database_type": "unknown"}
    
    def get_dataframe(self, query: str) -> Optional[pd.DataFrame]:
        """Execute query and return as pandas DataFrame"""
        try:
            with self.engine.connect() as conn:
                df = pd.read_sql(text(query), conn)
                return df
        except Exception as e:
            logger.error(f"DataFrame query error: {e}")
            return None
    
    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False

# Global database manager instance
db_manager = DatabaseManager()

def get_db_manager() -> DatabaseManager:
    """Get database manager instance"""
    return db_manager

def get_db_session() -> Session:
    """Dependency for getting database session"""
    db = db_manager.get_session()
    try:
        yield db
    finally:
        db.close()
