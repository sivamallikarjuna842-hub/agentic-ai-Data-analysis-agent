# Data Analyst Agent - Backend Implementation

Complete Python backend using LangGraph, LangChain, and FastAPI for the Autonomous Data Analyst Agent.

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐  ┌──────────────────┐                 │
│  │  API Routes      │  │  Error Handlers  │                 │
│  │  • /analyze      │  │  • Validation    │                 │
│  │  • /query        │  │  • Exceptions    │                 │
│  │  • /schema       │  │  • Logging       │                 │
│  └────────┬─────────┘  └──────────────────┘                 │
│           │                                                   │
│  ┌────────▼──────────────────────────────────────────────┐  │
│  │         DataAnalystAgent (LangGraph)                  │  │
│  │  • SQL Generation using LLM                           │  │
│  │  • Query Execution Tools                             │  │
│  │  • Data Analysis Tools                               │  │
│  │  • Visualization Creation Tools                      │  │
│  └────────┬─────────────────────────────────────────────┘  │
│           │                                                   │
│  ┌────────▼──────────────┐  ┌──────────────────────────┐   │
│  │  DatabaseManager      │  │  LLM Integration         │   │
│  │  • Query Execution    │  │  • OpenAI GPT-4          │   │
│  │  • Schema Inspection  │  │  • LangChain Chains      │   │
│  │  • Result Caching     │  │  • Tool Calling          │   │
│  └────────┬──────────────┘  └──────────────────────────┘   │
│           │                                                   │
│  ┌────────▼──────────────────────────────────────────────┐  │
│  │              Database Layer                           │  │
│  │  • SQLite / PostgreSQL                               │  │
│  │  • Connection Pooling                                │  │
│  │  • Query Optimization                                │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
backend/
├── main.py                      # FastAPI application
├── config.py                    # Configuration management
├── models.py                    # Pydantic data models
├── database.py                  # Database operations
├── agent.py                     # LangGraph agent with tools
├── init_db.py                   # Database initialization
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
└── README_BACKEND.md           # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 3. Initialize Database

```bash
python init_db.py
```

### 4. Run Server

```bash
python main.py
# Or with uvicorn directly:
uvicorn main:app --reload --port 8000
```

Server will be available at `http://localhost:8000`

## 📚 Core Components

### Config (config.py)
Centralized configuration management:
- Database settings (SQLite/PostgreSQL)
- LLM settings (OpenAI API key, model, temperature)
- LangChain settings (tracing, project)
- Query limits and timeouts
- Security settings

```python
from config import config

openai_key = config.OPENAI_API_KEY
db_url = config.get_database_url()
max_rows = config.MAX_QUERY_LIMIT
```

### Models (models.py)
Pydantic models for type safety:
- `AnalysisQuestion` - User input
- `SQLGeneration` - Generated SQL with confidence
- `QueryResult` - Query execution results
- `Visualization` - Chart configuration
- `Interpretation` - AI-generated insights
- `Analysis` - Complete analysis result

```python
from models import AnalysisQuestion, Analysis

question = AnalysisQuestion(question="What were total sales by category?")
analysis: Analysis = await agent.analyze(question.question)
```

### Database (database.py)
Database operations and connection management:

```python
from database import get_db_manager

db_manager = get_db_manager()

# Execute query
result = db_manager.execute_query("SELECT * FROM sales LIMIT 10")

# Get schema
schema = db_manager.get_schema()

# Get as DataFrame
df = db_manager.get_dataframe("SELECT * FROM sales")
```

**Features:**
- SQLite and PostgreSQL support
- Connection pooling
- Query safety (LIMIT enforcement)
- Result caching
- Schema inspection
- Transaction handling

### DataAnalystAgent (agent.py)
LangGraph-based agent with tool use:

```python
from agent import get_agent

agent = get_agent()

# Analyze question
analysis = await agent.analyze(
    question="What were total sales by category?",
    user_id="user_123"
)

# Returns:
# - SQL generation
# - Query execution
# - Visualization
# - Interpretation
```

**Tool Suite:**
1. `execute_sql_query` - Run SQL with safety checks
2. `get_database_schema` - Inspect schema
3. `analyze_data` - Statistical analysis
4. `create_visualization` - Generate charts

**Workflow:**
1. SQL Generation using LLM
2. Query Execution with safety checks
3. Data Analysis and statistics
4. Visualization Creation (Plotly)
5. Interpretation Generation

### FastAPI App (main.py)
REST API endpoints:

**Health & Status:**
- `GET /health` - Health check
- `GET /info` - API information

**Database:**
- `GET /schema` - Get schema information
- `POST /query/execute` - Execute SQL query

**Analysis:**
- `POST /analyze` - Analyze natural language question
- `POST /analyze/batch` - Batch analyze multiple questions

**Conversations:**
- `POST /conversation/create` - Create conversation
- `POST /conversation/{id}/message` - Send message

**Statistics:**
- `GET /stats/queries` - Query statistics
- `GET /stats/analysis` - Analysis statistics

## 🔧 Configuration

### Database Setup

**SQLite (Default):**
```env
DATABASE_URL=sqlite:///./analytics.db
SQLITE_DB_PATH=./analytics.db
```

**PostgreSQL:**
```env
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### LLM Configuration

```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4
LLM_TEMPERATURE=0.0
```

### Query Limits

```env
MAX_QUERY_LIMIT=1000        # Max rows returned
MAX_QUERY_TIMEOUT=30        # Query timeout (seconds)
```

## 📊 API Usage Examples

### Analyze a Question

```python
import requests

response = requests.post(
    "http://localhost:8000/analyze",
    json={
        "question": "What were total sales by product category?"
    }
)

analysis = response.json()
print(analysis["interpretation"]["summary"])
print(analysis["visualization"]["type"])
```

### Execute Raw SQL

```python
response = requests.post(
    "http://localhost:8000/query/execute",
    json={
        "sql": "SELECT category, SUM(revenue) FROM sales GROUP BY category"
    }
)

results = response.json()
```

### Get Database Schema

```python
response = requests.get("http://localhost:8000/schema")
schema = response.json()

for table in schema["tables"]:
    print(f"Table: {table['table_name']}")
    for col in table["columns"]:
        print(f"  - {col['name']}: {col['type']}")
```

## 🛠️ Tool Definitions

### execute_sql_query
```
Executes SQL query and returns results as JSON.
Args:
  sql (str): SQL query to execute
Returns:
  JSON with results, row count, columns
Safety:
  - LIMIT enforcement
  - Timeout protection
  - Error handling
```

### get_database_schema
```
Gets database schema information.
Returns:
  JSON with tables, columns, types, row counts
Usage:
  Context for SQL generation
```

### analyze_data
```
Analyzes data and calculates statistics.
Args:
  data_json (str): Data as JSON
Returns:
  Statistics (count, types, nulls, etc.)
```

### create_visualization
```
Creates interactive charts using Plotly.
Args:
  data_json (str): Data as JSON
  chart_type (str): bar, line, pie, area, scatter
  x_key (str): X-axis column
  y_key (str): Y-axis column
  title (str): Chart title
Returns:
  Interactive HTML chart
```

## 🔐 Security Features

1. **SQL Injection Prevention**
   - Parameterized queries
   - Input validation
   - Dangerous keyword filtering

2. **Access Control**
   - Optional user ID tracking
   - Conversation isolation
   - Request ID generation

3. **Rate Limiting**
   - Query timeout (30 seconds default)
   - Row limit (1000 default)
   - Result size constraints

4. **Error Handling**
   - Safe error messages
   - Logging without sensitive data
   - Exception recovery

## 📈 Performance Optimization

1. **Database**
   - Connection pooling
   - Query result caching
   - Index creation
   - LIMIT enforcement

2. **LLM**
   - Prompt optimization
   - Token counting
   - Response caching

3. **Visualization**
   - Plotly rendering
   - HTML compression
   - Base64 encoding

## 🧪 Testing

```bash
# Run with test environment
ENVIRONMENT=testing python main.py

# Test specific endpoint
curl http://localhost:8000/health

# Batch testing
python -m pytest backend/tests/ -v
```

## 📝 Logging

Logs are written to:
- Console (INFO level and above)
- File (logs/app.log)

Configuration:
```env
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

## 🚨 Troubleshooting

### Database Connection Issues
```
Check:
- DATABASE_URL is correct
- Database file exists or server is running
- Permissions for database file
```

### OpenAI API Errors
```
Check:
- OPENAI_API_KEY is set
- API key is valid
- Account has available credits
```

### Query Execution Failures
```
Check:
- SQL syntax is valid
- Tables and columns exist
- User has query permissions
```

## 🔄 Workflow Example

### Request
```json
{
  "question": "What were total sales by product category in Q4?"
}
```

### Processing Steps

1. **SQL Generation**
   - LLM analyzes question
   - Generates SQL based on schema
   - Confidence: 0.95

2. **Query Execution**
   - Adds LIMIT 1000
   - Executes against database
   - Returns 3 rows in 45ms

3. **Data Analysis**
   - Calculates statistics
   - Detects patterns
   - Identifies anomalies

4. **Visualization**
   - Creates Plotly chart
   - Generates interactive HTML
   - Selects bar chart type

5. **Interpretation**
   - LLM analyzes results
   - Generates 200+ word summary
   - Provides recommendations

### Response
```json
{
  "analysis_id": "a_1234567890",
  "timestamp": "2024-01-15T10:30:00Z",
  "question": "What were total sales by category in Q4?",
  "sql_generation": {
    "sql": "SELECT category, SUM(revenue) FROM sales WHERE QUARTER(date) = 4 GROUP BY category",
    "confidence": 0.95,
    "pattern_type": "revenue_by_category"
  },
  "query_result": {
    "status": "success",
    "rows": [
      {"category": "Electronics", "total_revenue": 15000},
      {"category": "Furniture", "total_revenue": 8000},
      {"category": "Accessories", "total_revenue": 5000}
    ],
    "row_count": 3,
    "execution_time_ms": 45
  },
  "visualization": {
    "type": "bar",
    "title": "Sales by Category",
    "x_key": "category",
    "y_key": "total_revenue",
    "interactive_html": "..."
  },
  "interpretation": {
    "summary": "Q4 sales show strong performance across all categories...",
    "key_metrics": {
      "total_revenue": 28000,
      "top_category": "Electronics",
      "category_count": 3
    },
    "patterns": ["Electronics dominates with 53% of revenue"],
    "recommendations": ["Increase Electronics inventory for Q1"]
  },
  "execution_time_ms": 250
}
```

## 🔗 Integration with Frontend

Frontend connects to backend at:
```
http://localhost:8000
```

**CORS Configuration:**
```python
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8000"
]
```

**Example Frontend Request:**
```javascript
const response = await fetch('http://localhost:8000/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    question: 'What were total sales by category?'
  })
});

const analysis = await response.json();
console.log(analysis.interpretation.summary);
```

## 📊 Database Schema

### Products
```sql
CREATE TABLE products (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  category TEXT NOT NULL,
  price REAL NOT NULL,
  created_at TIMESTAMP
);
```

### Customers
```sql
CREATE TABLE customers (
  id INTEGER PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  segment TEXT NOT NULL,
  created_at TIMESTAMP
);
```

### Sales
```sql
CREATE TABLE sales (
  id INTEGER PRIMARY KEY,
  date DATE NOT NULL,
  product_id INTEGER NOT NULL,
  customer_id INTEGER NOT NULL,
  quantity INTEGER NOT NULL,
  revenue REAL NOT NULL,
  segment TEXT NOT NULL,
  FOREIGN KEY(product_id) REFERENCES products(id),
  FOREIGN KEY(customer_id) REFERENCES customers(id)
);
```

## 🎯 Future Enhancements

- [ ] Query result caching with Redis
- [ ] Advanced NLP with multiple LLM providers
- [ ] Real-time data streaming
- [ ] Scheduled report generation
- [ ] User authentication and authorization
- [ ] API rate limiting
- [ ] Database query optimization suggestions
- [ ] Machine learning model integration
- [ ] Data quality monitoring
- [ ] Performance metrics dashboard

## 📞 Support

For issues or questions:
1. Check logs: `logs/app.log`
2. Review API documentation: `http://localhost:8000/docs`
3. Check Pydantic models for required fields
4. Verify database connection and schema

## 📄 License

MIT License - See LICENSE file

---

**Backend Status: ✅ Production Ready**

Complete implementation with LangGraph, LangChain, and FastAPI. Ready for integration with frontend and real database deployment.
