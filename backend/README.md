# Data Analyst Agent — Backend API

> **FastAPI-powered backend** for converting natural language questions into SQL queries, executing them against a relational database, and returning structured insights with interactive visualizations.

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────┐
│                     FastAPI Server                        │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────┐   ┌───────────┐   ┌──────────────────────┐ │
│  │  Routes  │──▶│  Agent    │──▶│  Database Manager    │ │
│  │  (REST)  │   │  (LLM)    │   │  (SQLite/PostgreSQL) │ │
│  └──────────┘   └───────────┘   └──────────────────────┘ │
│       │               │                    │              │
│       ▼               ▼                    ▼              │
│  ┌──────────┐   ┌───────────┐   ┌──────────────────────┐ │
│  │ Models   │   │ Groq/     │   │  Pydantic            │ │
│  │ (Pydantic)│   │ OpenAI    │   │  Validation          │ │
│  └──────────┘   └───────────┘   └──────────────────────┘ │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

## ✨ Features

| Feature | Description |
|---------|-------------|
| **🧠 LLM Integration** | Groq (primary) with automatic OpenAI fallback |
| **🗣️ NL → SQL** | Natural language to SQL query generation |
| **📊 Visualizations** | Auto-generated Plotly charts (bar, line, pie, area) |
| **📈 Analysis** | Programmatic + LLM-enhanced interpretation |
| **🔒 Safe Queries** | Row limits, timeout, dangerous SQL prevention |
| **🗄️ Multi-DB** | SQLite (dev) / PostgreSQL (production) |
| **📝 Logging** | Structured console + file logging |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- (Optional) Groq API key — [get one free](https://console.groq.com)

### Setup

```powershell
# 1. Navigate to backend
cd 'c:\Users\hp\OneDrive\Desktop\agentic ai 4\backend'

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
copy .env.example .env
# Edit .env and set your GROQ_API_KEY

# 4. Initialize the sample database
python init_db.py

# 5. Start the server
python -m uvicorn main:app --reload --port 8000
```

The API will be available at **http://localhost:8000**  
Interactive docs at **http://localhost:8000/docs**

---

## ⚙️ Configuration

All configuration lives in `backend/.env`:

```ini
# ── LLM (Groq preferred, OpenAI fallback) ──
GROQ_API_KEY=gsk_your_key_here
GROQ_MODEL=llama3-70b-8192

OPENAI_API_KEY=sk-...           # Only used if Groq is unavailable
OPENAI_MODEL=gpt-4

# ── Database ──
# SQLite (default):
# DATABASE_URL=sqlite:///path/to/analytics.db
# PostgreSQL (production):
# DATABASE_URL=postgresql://user:password@host/dbname

# ── Server ──
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### Supported Groq Models
| Model | ID |
|-------|----|
| Llama 3 70B | `llama3-70b-8192` |
| Llama 3 8B | `llama3-8b-8192` |
| Mixtral 8x7B | `mixtral-8x7b-32768` |
| Gemma 2 9B | `gemma2-9b-it` |

> **Note**: If `GROQ_API_KEY` is empty or starts with `gsk_YOUR`, the system falls back to `OPENAI_API_KEY`.

---

## 📡 API Reference

### Health

```http
GET /health
```
```json
{
  "status": "healthy",
  "database_connection": true,
  "llm_connection": true
}
```

### Information

```http
GET /info
```

### Schema

```http
GET /schema
```
Returns all tables, columns, types, and row counts.

### Analyze (Core Endpoint)

```http
POST /analyze
Content-Type: application/json

{
  "question": "What were total sales by product category?",
  "user_id": "optional-user-id"
}
```

**Response structure:**
```json
{
  "analysis_id": "a_1741771456902",
  "question": "What were total sales by product category?",
  "sql_generation": {
    "sql": "SELECT p.category, SUM(s.revenue) ...",
    "confidence": 0.85
  },
  "query_result": {
    "rows": [{"category": "Electronics", "total_revenue": 15000}],
    "row_count": 3,
    "execution_time_ms": 45
  },
  "visualization": {
    "type": "bar",
    "x_key": "category",
    "y_key": "total_revenue",
    "interactive_html": "<div>...</div>"
  },
  "interpretation": {
    "summary": "Analysis of 3 records completed. ...",
    "patterns": ["High variance in revenue..."],
    "recommendations": ["Focus on top-performing categories..."],
    "next_steps": ["Drill down into specific products..."]
  },
  "execution_time_ms": 1626
}
```

### Execute SQL (Admin)

```http
POST /query/execute
{
  "sql": "SELECT * FROM sales LIMIT 5"
}
```
> ⚠ Dangerous keywords (`DROP`, `DELETE`, `TRUNCATE`, etc.) are blocked.

### Conversation

```http
POST /conversation/create
POST /conversation/{id}/message
```

### Statistics

```http
GET /stats/queries
GET /stats/analysis
```

---

## 🗄️ Database Schema

The sample database contains 3 tables with 95+ records:

```sql
-- products (8 rows)
CREATE TABLE products (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  category TEXT NOT NULL,         -- Electronics, Accessories, Furniture
  price REAL NOT NULL
);

-- customers (6 rows)
CREATE TABLE customers (
  id INTEGER PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  segment TEXT NOT NULL           -- Enterprise, SMB
);

-- sales (95 rows)
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

---

## 🧩 Project Structure

```
backend/
├── main.py              # FastAPI app — routes, middleware, error handlers
├── config.py            # Environment-based configuration
├── models.py            # Pydantic models for all request/response schemas
├── agent.py             # DataAnalystAgent — LLM integration + analysis logic
├── database.py          # Database manager — queries, schema, connection
├── init_db.py           # Seed script — creates tables + sample data
├── requirements.txt     # Python dependencies
├── .env.example         # Configuration template
└── README.md            # This file
```

---

## 🔌 Frontend Integration

The frontend connects via `POST /analyze`. CORS is pre-configured for:

```
http://localhost:3000
http://localhost:5173  (Vite dev server)
http://localhost:8000
```

**Frontend `.env`:**
```ini
VITE_API_URL=http://localhost:8000
```

---

## 🧪 Running Tests

```powershell
# Test health
python -c "import urllib.request, json; \
  r = urllib.request.urlopen('http://localhost:8000/health'); \
  print(json.loads(r.read()))"

# Test analysis
python -c "import urllib.request, json; \
  d = json.dumps({'question':'Total sales by category?'}).encode(); \
  r = urllib.request.Request('http://localhost:8000/analyze', data=d, \
    headers={'Content-Type':'application/json'}, method='POST'); \
  print(json.loads(urllib.request.urlopen(r).read()))"
```

---

## 🔒 Security

| Measure | Implementation |
|---------|---------------|
| SQL Injection | Parameterized queries via SQLAlchemy |
| Dangerous Ops | Keyword blocklist (`DROP`, `DELETE`, etc.) |
| Row Limits | `MAX_QUERY_LIMIT=1000` enforced |
| Timeouts | `MAX_QUERY_TIMEOUT=30s` |
| CORS | Whitelist-based origin control |
| Error Handling | Safe messages — no internal details leaked |

---

## 🐳 Docker Deployment

```powershell
# From project root
docker-compose up --build
```

---

## 📊 Sample Questions

Try these with the API or frontend:

- *"What were total sales by product category?"*
- *"Show me the top 5 products by revenue"*
- *"What is the daily revenue trend?"*
- *"How much revenue did each customer segment generate?"*
- *"What is the average price by product category?"*
- *"Which products had the highest sales volume?"*

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Framework | FastAPI 0.104+ |
| Server | Uvicorn |
| LLM | Groq (primary) / OpenAI (fallback) |
| Database | SQLAlchemy + SQLite / PostgreSQL |
| Charts | Plotly |
| Data | Pandas, NumPy |
| Validation | Pydantic v2 |

---

## 📄 License

MIT