# AI-Powered E-commerce Analytics Demo - Architecture Notes

## 🎯 Project Overview

An AI agent demo that extracts information from a local SQLite database, performs analytical reasoning, and generates visualizations. Users interact via natural language queries.

**Domain**: E-commerce (orders, customers, products, sales analytics)

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                      (React + TypeScript)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ Chat Input   │  │ Visualizations│  │ Query History│        │
│  │ Component    │  │ (Charts/Tables)│  │              │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP/WebSocket
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND API LAYER                          │
│                         (FastAPI)                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  POST /api/query - Process natural language queries      │  │
│  │  GET  /api/history - Retrieve query history              │  │
│  │  WS   /ws - WebSocket for streaming responses            │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AI AGENT ORCHESTRATION                       │
│                    (LangChain Framework)                        │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                   SQL Database Agent                     │  │
│  │  • Natural Language → SQL Translation                    │  │
│  │  • Query Validation & Safety Checks                      │  │
│  │  • Result Analysis & Insight Generation                  │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ SQL Tool     │  │ Analysis Tool│  │ Viz Formatter│        │
│  │ (Query DB)   │  │ (Generate    │  │ (Chart Config)│        │
│  │              │  │  Insights)   │  │              │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└────────────────────────┬───────────────────┬────────────────────┘
                         │                   │
                         ▼                   ▼
              ┌──────────────────┐  ┌──────────────────┐
              │  SQLite Database │  │  Claude API      │
              │  (E-commerce)    │  │  (Anthropic)     │
              │                  │  │                  │
              │  • customers     │  │  • SQL Gen       │
              │  • products      │  │  • Analysis      │
              │  • orders        │  │  • Insights      │
              │  • order_items   │  │                  │
              │  • categories    │  │                  │
              │  • reviews       │  │                  │
              │  • inventory     │  │                  │
              └──────────────────┘  └──────────────────┘
```

---

## 🔄 Data Flow Sequence

```
User Query: "Show me top 10 customers by revenue"
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ 1. Frontend sends query to Backend API                  │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ 2. LangChain Agent receives query                       │
│    • Analyzes intent                                     │
│    • Determines required tools                           │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ 3. Agent calls Claude API                               │
│    • Generates SQL query from natural language          │
│    • Returns: SELECT c.name, SUM(o.total) as revenue... │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ 4. SQL Tool validates and executes query                │
│    • Safety checks (read-only, no DROP/DELETE)          │
│    • Executes against SQLite database                   │
│    • Returns result set                                  │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ 5. Analysis Tool processes results                      │
│    • Sends data to Claude for interpretation            │
│    • Generates insights and trends                       │
│    • Identifies anomalies or patterns                    │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ 6. Visualization Formatter                              │
│    • Determines best chart type (bar, line, pie, table) │
│    • Formats data for frontend rendering                │
│    • Generates chart configuration                       │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ 7. Backend returns structured response                  │
│    {                                                     │
│      "query": "original question",                       │
│      "sql": "generated SQL",                             │
│      "data": [...results...],                            │
│      "insights": "AI-generated analysis",                │
│      "visualization": {                                  │
│        "type": "bar",                                    │
│        "config": {...}                                   │
│      }                                                   │
│    }                                                     │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ 8. Frontend renders results                             │
│    • Displays chart/table                               │
│    • Shows AI insights                                   │
│    • Saves to query history                              │
└─────────────────────────────────────────────────────────┘
```

---

## 🗄️ Database Schema (E-commerce)

```sql
┌─────────────────┐
│   customers     │
├─────────────────┤
│ id (PK)         │
│ name            │
│ email           │
│ country         │
│ registration_dt │
│ lifetime_value  │
└─────────────────┘
        │
        │ 1:N
        ▼
┌─────────────────┐      ┌─────────────────┐
│     orders      │      │   categories    │
├─────────────────┤      ├─────────────────┤
│ id (PK)         │      │ id (PK)         │
│ customer_id(FK) │      │ name            │
│ order_date      │      │ description     │
│ status          │      └─────────────────┘
│ total_amount    │              │
└─────────────────┘              │ 1:N
        │                        ▼
        │ 1:N          ┌─────────────────┐
        │              │    products     │
        │              ├─────────────────┤
        │              │ id (PK)         │
        │              │ category_id(FK) │
        │              │ name            │
        │              │ price           │
        │              │ cost            │
        │              │ description     │
        ▼              └─────────────────┘
┌─────────────────┐              │
│  order_items    │              │ 1:N
├─────────────────┤              │
│ id (PK)         │◄─────────────┘
│ order_id (FK)   │
│ product_id (FK) │
│ quantity        │
│ unit_price      │
│ subtotal        │
└─────────────────┘
        │
        │ 1:1
        ▼
┌─────────────────┐      ┌─────────────────┐
│    reviews      │      │   inventory     │
├─────────────────┤      ├─────────────────┤
│ id (PK)         │      │ id (PK)         │
│ product_id (FK) │      │ product_id (FK) │
│ customer_id(FK) │      │ quantity        │
│ rating          │      │ warehouse       │
│ comment         │      │ last_updated    │
│ review_date     │      └─────────────────┘
└─────────────────┘
```

---

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (async, high-performance)
- **AI Framework**: LangChain (agent orchestration)
- **LLM**: Anthropic Claude 3.5 Sonnet
- **Database**: SQLite (local, file-based)
- **ORM**: SQLAlchemy
- **Data Processing**: pandas, numpy

### Frontend
- **Framework**: React 18+ with TypeScript
- **Visualization**: Recharts or Chart.js
- **HTTP Client**: Axios
- **Styling**: TailwindCSS
- **State Management**: React Query

### DevOps
- **Containerization**: Docker (optional)
- **Package Management**: pip (backend), npm (frontend)

---

## 📦 Project Structure

```
talk-to-data/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application entry
│   │   ├── config.py            # Configuration & environment
│   │   ├── database.py          # SQLite connection setup
│   │   │
│   │   ├── models/              # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── customer.py
│   │   │   ├── product.py
│   │   │   ├── order.py
│   │   │   └── ...
│   │   │
│   │   ├── agents/              # LangChain agents
│   │   │   ├── __init__.py
│   │   │   ├── sql_agent.py     # Main SQL agent
│   │   │   └── tools.py         # Custom tools
│   │   │
│   │   ├── api/                 # API routes
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   │
│   │   └── utils/               # Utilities
│   │       ├── __init__.py
│   │       ├── validators.py
│   │       └── formatters.py
│   │
│   ├── scripts/
│   │   └── seed_data.py         # Generate sample data
│   │
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── ChartRenderer.tsx
│   │   │   ├── QueryHistory.tsx
│   │   │   └── InsightPanel.tsx
│   │   │
│   │   ├── services/
│   │   │   └── api.ts           # API client
│   │   │
│   │   ├── hooks/
│   │   │   └── useQuery.ts      # Custom hooks
│   │   │
│   │   ├── types/
│   │   │   └── index.ts         # TypeScript types
│   │   │
│   │   ├── App.tsx
│   │   └── main.tsx
│   │
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── database/
│   ├── schema.sql               # Database schema
│   └── ecommerce.db            # SQLite database file (generated)
│
├── notes.md                     # This file
├── README.md                    # Project documentation
└── .gitignore
```

---

## 🎯 Key Features

### 1. Natural Language Queries
Users can ask questions in plain English:
- "Show me the top 10 customers by revenue"
- "What products are trending this month?"
- "Compare Q1 vs Q2 sales performance"
- "Which categories have the highest profit margins?"
- "Show me customers who haven't ordered in 3 months"

### 2. Intelligent SQL Generation
- LangChain agent uses Claude to convert NL → SQL
- Validates queries for safety (read-only operations)
- Handles complex joins and aggregations
- Optimizes query performance

### 3. Automated Analysis
- AI analyzes query results
- Identifies trends and patterns
- Detects anomalies
- Generates actionable insights
- Provides context and explanations

### 4. Dynamic Visualizations
- Automatically selects appropriate chart type
- Bar charts for comparisons
- Line charts for trends over time
- Pie charts for distributions
- Tables for detailed data
- Configurable and interactive

### 5. Conversation Memory
- Maintains context across queries
- Supports follow-up questions
- References previous results
- Session-based history

---

## 🔒 Safety & Security

### Query Validation
- Whitelist of allowed SQL operations (SELECT only)
- Blacklist dangerous keywords (DROP, DELETE, UPDATE, INSERT)
- Parameter sanitization
- Query timeout limits

### Database Protection
- Read-only database connection
- No write operations allowed
- Isolated demo environment
- Regular backups

### API Security
- Rate limiting
- Input validation
- Error handling without exposing internals
- CORS configuration

---

## 📊 Example Interactions

### Example 1: Revenue Analysis
**User**: "Show me monthly revenue for 2025"

**Agent Process**:
1. Generates SQL: `SELECT strftime('%Y-%m', order_date) as month, SUM(total_amount) as revenue FROM orders WHERE strftime('%Y', order_date) = '2025' GROUP BY month ORDER BY month`
2. Executes query
3. Analyzes results with Claude
4. Generates line chart configuration
5. Returns insights: "Revenue shows steady growth with peak in December..."

### Example 2: Customer Segmentation
**User**: "Who are my best customers?"

**Agent Process**:
1. Generates SQL with customer lifetime value calculation
2. Ranks customers by total spend
3. Analyzes purchasing patterns
4. Creates bar chart of top 10
5. Provides insights: "Top 10 customers represent 35% of revenue..."

### Example 3: Product Performance
**User**: "Which products have low ratings but high sales?"

**Agent Process**:
1. Joins products, reviews, and order_items
2. Filters for rating < 3.5 and high order volume
3. Analyzes the discrepancy
4. Creates scatter plot
5. Suggests: "These products may need quality improvements..."

---

## 🚀 Development Phases

### Phase 1: Foundation ✓
- [x] Architecture design
- [ ] Project structure setup
- [ ] Database schema creation
- [ ] Sample data generation

### Phase 2: Backend Core
- [ ] FastAPI setup
- [ ] SQLite connection
- [ ] SQLAlchemy models
- [ ] Basic API endpoints

### Phase 3: AI Agent
- [ ] LangChain integration
- [ ] Claude API setup
- [ ] SQL generation tool
- [ ] Analysis tool
- [ ] Visualization formatter

### Phase 4: Frontend
- [ ] React project setup
- [ ] Chat interface
- [ ] Chart components
- [ ] API integration
- [ ] State management

### Phase 5: Integration & Testing
- [ ] End-to-end testing
- [ ] Query optimization
- [ ] Error handling
- [ ] Performance tuning

### Phase 6: Polish
- [ ] UI/UX improvements
- [ ] Documentation
- [ ] Demo scenarios
- [ ] Deployment guide

---

## 🎓 Learning Outcomes

This demo showcases:
- **AI Agent Development**: Building intelligent agents with LangChain
- **Natural Language Processing**: Converting text to structured queries
- **Data Analysis**: Automated insight generation
- **Full-Stack Development**: React + FastAPI integration
- **Database Design**: Relational schema for analytics
- **API Design**: RESTful endpoints with async processing
- **Visualization**: Dynamic chart generation

---

## 📝 Next Steps

1. ✅ Create project structure
2. ✅ Set up SQLite database with schema
3. ✅ Generate realistic sample data
4. ✅ Initialize FastAPI backend
5. ✅ Configure LangChain with Claude
6. ✅ Build SQL agent with tools
7. ✅ Create API endpoints
8. ✅ Set up React frontend
9. ✅ Implement chat interface
10. ✅ Add visualizations
11. ✅ Test and refine
12. ✅ Document and demo

---

**Status**: Architecture Complete - Ready for Implementation
**Last Updated**: 2026-03-05