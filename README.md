# 🤖 Autonomous Data Analyst Agent

> **Natural Language → SQL → Insights** — A full-stack application that lets you ask questions about your data in plain English and get back interactive visualizations, analysis, and recommendations.
>  <img width="960" height="441" alt="Screenshot 2026-06-18 102741" src="https://github.com/user-attachments/assets/0e11296a-0fcc-4360-99a3-671bf98d9486" />

<img width="959" height="442" alt="Screenshot 2026-06-18 141629" src="https://github.com/user-attachments/assets/61e3cad1-ec2c-4db8-adb9-735be7cee6e8" />

<img width="925" height="258" alt="Screenshot 2026-06-18 141917" src="https://github.com/user-attachments/assets/3395d777-9eb1-4787-a656-59662c676dbb" />

<img width="935" height="358" alt="Screenshot 2026-06-18 141938" src="https://github.com/user-attachments/assets/07ad7872-f3d6-4c1f-813f-d6847ba79a09" />




[![Backend](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi)](backend/)
[![Frontend](https://img.shields.io/badge/Frontend-React-61DAFB?logo=react)](src/)
[![LLM](https://img.shields.io/badge/LLM-Groq%20%7C%20OpenAI-FF6600)](#-llm-integration)
[![License](https://img.shields.io/badge/License-MIT-blue)](#license)

---

## 📋 Table of Contents

- [Architecture Overview](#-architecture-overview)
- [Quick Start](#-quick-start)
- [LLM Integration](#-llm-integration)
- [Project Structure](#-project-structure)
- [API Overview](#-api-overview)
- [Sample Questions](#-sample-questions)
- [Tech Stack](#-tech-stack)
- [Deployment](#-deployment)
- [License](#-license)

---

## 🏛️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend                              │
│              React + TypeScript + Vite                       │
│                   http://localhost:5173                      │
└──────────────────────────┬──────────────────────────────────┘
                           │ POST /analyze
                           │ JSON Response
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                        Backend                                │
│                    FastAPI + Uvicorn                          │
│                   http://localhost:8000                       │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐   ┌───────────┐   ┌────────────────────────┐  │
│  │  Routes  │──▶│  Agent    │──▶│  Database Manager      │  │
│  │  (REST)  │   │  (LLM)    │   │  (SQLite/PostgreSQL)   │  │
│  └──────────┘   └───────────┘   └────────────────────────┘  │
│       │                │                    │                │
│       ▼                ▼                    ▼                │
│  ┌──────────┐   ┌───────────┐   ┌────────────────────────┐  │
│  │ Models   │   │ Groq/     │   │  Pydantic              │  │
│  │ (Pydantic)│   │ OpenAI    │   │  Validation            │  │
│  └──────────┘   └───────────┘   └────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Backend Setup

```powershell
# Navigate to backend
cd 'c:\Users\hp\OneDrive\Desktop\agentic ai 4\backend'

# Install Python dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env and set your GROQ_API_KEY (optional — falls back to OpenAI)

# Initialize the database with sample data
python init_db.py

# Start the backend server
python -m uvicorn main:app --reload --port 8000
```

### 2. Frontend Setup

```powershell
# In a new terminal, navigate to project root
cd 'c:\Users\hp\OneDrive\Desktop\agentic ai 4'

# Install Node.js dependencies
npm install

# Start the development server
npm run dev
```

### 3. Open the App

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:5173 | User interface |
| **Backend API** | http://localhost:8000 | REST API |
| **API Docs** | http://localhost:8000/docs | Interactive Swagger docs |

---

## 🧠 LLM Integration

The agent supports **two LLM providers** with automatic fallback:

### Primary: Groq (Free — Recommended)
- Ultra-fast inference on open-source models
- [Get a free API key](https://console.groq.com)
- Configured via `GROQ_API_KEY` in `backend/.env`

### Fallback: OpenAI
- Used when Groq is unavailable / no key configured
- Configured via `OPENAI_API_KEY` in `backend/.env`

### How it works
```python
# In agent.py — auto-detection logic:
if GROQ_API_KEY is valid and not a placeholder:
    use ChatGroq(model="llama3-70b-8192")
else:
    use ChatOpenAI(model="gpt-4")  # fallback
```

If **neither** API key is configured, the agent falls back to **programmatic SQL generation** and **statistical interpretation** — fully functional without any external LLM.

---

## 📁 Project Structure

```
agentic-ai-4/
├── backend/                          # FastAPI Python backend
│   ├── main.py                      # API routes & middleware
│   ├── agent.py                     # LLM agent (Groq/OpenAI)
│   ├── config.py                    # Environment config
│   ├── models.py                    # Pydantic schemas
│   ├── database.py                  # SQLAlchemy database manager
│   ├── init_db.py                   # Seed script with sample data
│   ├── requirements.txt             # Python dependencies
│   ├── .env                         # Local configuration
│   └── README.md                    # Backend documentation
│
├── src/                              # React TypeScript frontend
│   ├── App.tsx                      # Main application component
│   ├── main.tsx                     # React entry point
│   ├── index.css                    # Tailwind styles
│   ├── components/
│   │   ├── DataAnalystAgent.tsx     # API client wrapper
│   │   ├── QueryPreview.tsx         # SQL display component
│   │   ├── ResultsDisplay.tsx       # Charts + table + insights
│   │   └── SampleQuestions.tsx      # Pre-built questions
│   ├── utils/
│   │   └── api.ts                   # Axios HTTP client
│   └── README.md                    # Frontend documentation
│
├── .env                              # Frontend env vars
├── package.json                      # Node.js dependencies
├── vite.config.ts                    # Vite build configuration
├── tsconfig.json                     # TypeScript configuration
└── docker-compose.yml                # Docker deployment
```

---

## 📡 API Overview

### Core Endpoint

```
POST /analyze
Content-Type: application/json

{
  "question": "What were total sales by product category?"
}
```

**Response:** SQL, query results, visualization config, and interpretation.

### Other Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check with database + LLM status |
| `/info` | GET | API metadata |
| `/schema` | GET | Full database schema |
| `/query/execute` | POST | Execute raw SQL (safe mode) |
| `/conversation/create` | POST | Start a conversation |
| `/conversation/{id}/message` | POST | Continue conversation |

[Full documentation → backend/README.md](backend/README.md)

---

## 💬 Sample Questions

Try asking any of these in the frontend:

| Question | What it does |
|----------|-------------|
| *"What were total sales by product category?"* | Groups revenue by Electronics, Accessories, Furniture |
| *"Show me the top 5 products by revenue"* | Ranks products by total revenue |
| *"What is the daily revenue trend?"* | Line chart of revenue over 30 days |
| *"How much revenue did each customer segment generate?"* | Enterprise vs SMB comparison |
| *"What is the average price by product category?"* | Average product pricing analysis |
| *"Which products had the highest sales volume?"* | Top sellers by quantity |

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **FastAPI** | REST API framework |
| **Uvicorn** | ASGI server |
| **SQLAlchemy** | ORM & database abstraction |
| **Groq / OpenAI** | LLM providers |
| **Plotly** | Chart generation (interactive HTML) |
| **Pandas / NumPy** | Data analysis & statistics |
| **Pydantic** | Request/response validation |

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 19** | UI framework |
| **TypeScript 5.9** | Type-safe development |
| **Vite 7** | Build tool & dev server |
| **Tailwind CSS 4** | Utility-first styling |
| **Recharts** | Interactive charts |
| **Lucide React** | Icon library |
| **Axios** | HTTP client |

---

## 🐳 Docker Deployment

```powershell
# From the project root
docker-compose up --build
```

This starts both the backend (FastAPI on port 8000) and frontend (Nginx on port 80).

See `docker-compose.yml`, `Dockerfile.frontend`, and `nginx.conf` for details.

---

## 🔒 Security

- **SQL Injection Protection**: Parameterized queries via SQLAlchemy
- **Dangerous Operation Blocking**: Keywords like `DROP`, `DELETE`, `TRUNCATE` are rejected
- **Row Limits**: Queries are automatically limited to 1000 rows
- **Query Timeouts**: Queries timeout after 30 seconds
- **CORS**: Whitelist-based origin control
- **Error Handling**: Safe error messages — no internal details exposed

---

## 📄 License

MIT

---

<p align="center">
  Built with ❤️ using <a href="https://fastapi.tiangolo.com/">FastAPI</a>, <a href="https://react.dev/">React</a>, and <a href="https://groq.com/">Groq</a>
</p>
