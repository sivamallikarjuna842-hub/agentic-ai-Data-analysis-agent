# Data Analyst Agent — Frontend

> **React + TypeScript + Vite** frontend for the Autonomous Data Analyst Agent.  
> Asks natural-language questions → backend generates SQL → executes → visualizes → interprets.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **🔍 Natural Language Input** | Type any data question in plain English |
| **📋 Smart Suggestions** | Pre-built sample questions for quick start |
| **🔎 SQL Preview** | Expand to see the generated SQL; copy with one click |
| **📊 Interactive Charts** | Bar, line, pie, area — rendered via Recharts |
| **📑 Data Table** | Toggleable table view with formatted numbers |
| **📝 Rich Interpretation** | AI-generated insights with patterns, anomalies, recommendations |
| **💬 Conversation History** | Browse past queries and results |
| **🌙 Dark Theme** | Modern gradient UI with dark mode design |
| **🔗 Backend Connected** | Calls real backend API (not mock data) |

---

## 🎨 UI Preview

```
┌─────────────────────────────────────────────────────────────┐
│  🗄️  Data Analyst Agent                                     │
│  Ask questions about your data in natural language          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Ask a question about your data...          [➤ Send] │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
│  ✨ Try asking about your data:                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐    │
│  │ Total sales │  │ Top 5       │  │ Daily revenue   │    │
│  │ by category │  │ products    │  │ trend           │    │
│  └─────────────┘  └─────────────┘  └─────────────────┘    │
│                                                             │
│  ┌─ Generated SQL ─────────────────────────────────────────┐│
│  │ SELECT p.category, SUM(s.revenue) ...                   ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  ┌─ Data Visualization ────────────────────────────────────┐│
│  │  ████████████                                           ││
│  │  ████████████  ██████████                               ││
│  │  ████████████  ██████████  ████████                     ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  💡 Analysis: Electronics leads with 53% of total revenue. ││
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Component Architecture

```
src/
├── App.tsx                         # Root component — state, routing, layout
├── main.tsx                        # React entry point
├── index.css                       # Tailwind CSS v4 + global styles
├── vite-env.d.ts                   # Vite environment type declarations
├── components/
│   ├── DataAnalystAgent.tsx        # API client → backend POST /analyze
│   ├── QueryPreview.tsx            # SQL display — expand/collapse + copy
│   ├── ResultsDisplay.tsx          # Charts + interpretation + data table
│   └── SampleQuestions.tsx         # Clickable sample question buttons
└── utils/
    ├── api.ts                      # Axios client for backend communication
    └── cn.ts                       # Tailwind className utility
```

---

## 🔄 Data Flow

```
User Question
     │
     ▼
┌─────────────────┐     POST /analyze     ┌──────────────┐
│ DataAnalystAgent│ ────────────────────▶  │  Backend API │
│  (React)        │ ◀──────────────────── │  (FastAPI)   │
└─────────────────┘     JSON Response     └──────────────┘
     │
     ▼
┌─────────────────┐
│ mapBackendResponse │
└─────────────────┘
     │
     ▼
┌──────────────────────────────────────────┐
│  App.tsx — setAnalysis(result)           │
│    ├─ QueryPreview   (SQL display)       │
│    ├─ ResultsDisplay (charts + table)    │
│    └─ Conversation History               │
└──────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Backend server running on `http://localhost:8000`

### Setup

```powershell
# 1. Navigate to project root
cd 'c:\Users\hp\OneDrive\Desktop\agentic ai 4'

# 2. Install dependencies
npm install

# 3. Configure backend URL (optional — defaults to localhost:8000)
# Edit .env:
# VITE_API_URL=http://localhost:8000

# 4. Start the development server
npm run dev
```

Open **http://localhost:5173** in your browser.

---

## ⚙️ Configuration

```ini
# .env — Frontend environment variables
VITE_API_URL=http://localhost:8000   # Backend API base URL
```

---

## 🧩 Key Components

### `App.tsx`
The main application shell:
- State management for questions, loading, results, conversation history
- Form submission handler connecting to `DataAnalystAgent`
- Scroll-to-results behavior and error state display
- Conversation history sidebar with click-to-restore

### `DataAnalystAgent.tsx`
The bridge between frontend and backend:
- Calls `POST /analyze` on the backend via `src/utils/api.ts`
- Maps backend response (`BackendAnalysis`) → frontend `AnalysisResult`
- Handles network errors with clear user-facing messages
- Works without any API key — uses fallback SQL generation on the backend

### `QueryPreview.tsx`
Expandable SQL preview:
- Shows the user's original question
- Displays the generated SQL with syntax formatting
- One-click copy to clipboard with success feedback

### `ResultsDisplay.tsx`
Rich result rendering:
- **Interactive charts** via Recharts (bar, line, pie, area)
- **Interpretation panel** with colored gradient background
- **Data table** with toggle visibility, formatted numbers
- **Query metadata** (row count, columns, status)

### `SampleQuestions.tsx`
Quick-start buttons:
- 6 pre-built questions covering common use cases
- Click to populate the input field

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Framework | React 19 |
| Language | TypeScript 5.9 |
| Build Tool | Vite 7 |
| Styling | Tailwind CSS 4 |
| Charts | Recharts 3 |
| Icons | Lucide React |
| HTTP Client | Axios |
| Bundle | Single-file output (vite-plugin-singlefile) |

---

## 🌐 API Endpoints Used

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/analyze` | POST | Send natural language question, get analysis |
| `/health` | GET | Check backend availability |
| `/schema` | GET | Retrieve database schema |
| `/query/execute` | POST | Execute raw SQL (admin) |

---

## 🎨 Styling

The UI uses a dark gradient theme:
- Background: `from-slate-900 via-slate-800 to-slate-900`
- Accent colors: Cyan (`#06b6d4`), Blue (`#3b82f6`)
- Cards: Semi-transparent `bg-slate-800` with border `border-slate-700`
- Glassmorphism effects on the header (backdrop blur)

---

## ❌ Error Handling

The frontend gracefully handles:

| Scenario | User Experience |
|----------|----------------|
| Backend offline | "Cannot connect to the backend server" message with setup instructions |
| Invalid question | Error display with backend validation details |
| No results | "No data found" interpretation block |
| Chart render failure | Fallback text message instead of crash |

---

## 📄 License

MIT