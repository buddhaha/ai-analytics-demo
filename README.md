# AI-Powered E-commerce Analytics Demo

An intelligent data analytics system that uses AI to convert natural language questions into SQL queries, analyze results, and generate visualizations automatically.

## 🎯 Features

- **Natural Language Queries**: Ask questions in plain English
- **AI-Powered SQL Generation**: Claude converts questions to SQL automatically
- **Smart Analysis**: AI-generated insights and trend identification
- **Dynamic Visualizations**: Automatic chart selection (bar, line, pie, table)
- **Safe Query Execution**: Built-in SQL injection prevention
- **E-commerce Data Model**: Realistic sample data with customers, products, orders, reviews

## 🏗️ Architecture

```
Frontend (React + TypeScript)
    ↓
Backend API (FastAPI)
    ↓
AI Agent (LangChain + Claude)
    ↓
SQLite Database
```

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+ (for frontend)
- Anthropic API key (for Claude)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/YOUR_USERNAME/ai-analytics-demo.git
cd ai-analytics-demo
```

### 2. Backend Setup

```bash
# Create virtual environment
cd backend
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 3. Initialize Database

```bash
# Create and seed the database
python scripts/seed_data.py
```

This will create `database/ecommerce.db` with:
- 200 customers
- 80 products across 8 categories
- 500 orders with items
- Product reviews
- Inventory data

### 4. Start Backend Server

```bash
# From backend directory
python -m app.main

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at: http://localhost:8000
API Documentation: http://localhost:8000/docs

### 5. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: http://localhost:5173

## 🔑 Environment Variables

Create `backend/.env` file:

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional (defaults shown)
DATABASE_URL=sqlite:///./database/ecommerce.db
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

## 📊 Database Schema

### Tables
- **customers**: Customer information and lifetime value
- **products**: Product catalog with pricing
- **categories**: Product categories
- **orders**: Order headers with status
- **order_items**: Order line items
- **reviews**: Product reviews and ratings
- **inventory**: Stock levels by warehouse

### Views (Pre-built Analytics)
- **customer_analytics**: Customer metrics and RFM analysis
- **product_performance**: Product sales and profitability
- **monthly_sales**: Time-series sales data
- **category_performance**: Category-level metrics

## 🎮 Example Queries

Try these natural language questions:

### Sales Analysis
- "Show me the top 10 customers by total revenue"
- "What is the monthly revenue trend for 2025?"
- "Compare sales between Q1 and Q2 of 2025"

### Product Insights
- "Which products are the best sellers?"
- "Show me products with low ratings but high sales"
- "What are the top 5 products in the Electronics category?"

### Customer Analytics
- "Who are the customers that haven't ordered in 3 months?"
- "What is the average order value by country?"
- "Show me customer lifetime value distribution"

### Inventory & Operations
- "Which products are low in stock?"
- "How many orders are pending or processing?"
- "Show me the profit margin by product category"

## 🛠️ API Endpoints

### POST /api/query
Process a natural language query

**Request:**
```json
{
  "question": "Show me top 10 customers by revenue",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "success": true,
  "question": "Show me top 10 customers by revenue",
  "sql": "SELECT name, SUM(total_amount) as revenue...",
  "results": [...],
  "analysis": "AI-generated insights...",
  "visualization": {
    "type": "bar",
    "xAxis": "name",
    "yAxis": "revenue"
  },
  "row_count": 10
}
```

### GET /api/schema
Get database schema information

### GET /api/sample-queries
Get example queries to try

### GET /api/health
Health check endpoint

## 🔒 Security Features

- **SQL Injection Prevention**: Query validation and sanitization
- **Read-Only Access**: Only SELECT queries allowed
- **Keyword Blacklist**: Blocks dangerous SQL operations
- **Query Timeout**: Prevents long-running queries
- **CORS Configuration**: Controlled frontend access

## 🧪 Testing

```bash
# Run the seed script to verify database setup
python backend/scripts/seed_data.py

# Test API endpoints
curl http://localhost:8000/api/health
curl http://localhost:8000/api/sample-queries

# Test query endpoint
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Show me total revenue"}'
```

## 📁 Project Structure

```
ai-analytics-demo/
├── backend/
│   ├── app/
│   │   ├── agents/          # AI agent logic
│   │   │   └── sql_agent.py # LangChain SQL agent
│   │   ├── api/             # API routes
│   │   │   └── routes.py
│   │   ├── models/          # Data models
│   │   ├── utils/           # Utilities
│   │   ├── config.py        # Configuration
│   │   ├── database.py      # Database connection
│   │   └── main.py          # FastAPI app
│   ├── scripts/
│   │   └── seed_data.py     # Database seeding
│   ├── requirements.txt
│   └── .env.example
├── frontend/                # React frontend (TBD)
├── database/
│   ├── schema.sql          # Database schema
│   └── ecommerce.db        # SQLite database (generated)
├── notes.md                # Architecture notes
└── README.md
```

## 🤖 How It Works

1. **User asks a question** in natural language
2. **LangChain agent** receives the question
3. **Claude AI** generates appropriate SQL query
4. **Query validator** ensures safety (read-only, no injection)
5. **SQL executes** against SQLite database
6. **Results returned** to agent
7. **Claude analyzes** the data and generates insights
8. **Visualization config** determined automatically
9. **Response sent** to frontend with data, analysis, and chart config
10. **Frontend renders** charts and displays insights

## 🎨 Visualization Types

The system automatically selects the best visualization:

- **Line Chart**: Time-series data, trends over time
- **Bar Chart**: Comparisons, rankings, top N queries
- **Pie Chart**: Distributions, percentages, breakdowns
- **Table**: Detailed data, complex results, many columns

## 🐛 Troubleshooting

### Database not found
```bash
# Recreate database
python backend/scripts/seed_data.py
```

### Import errors
```bash
# Reinstall dependencies
pip install -r backend/requirements.txt
```

### API key errors
```bash
# Verify .env file exists and contains valid key
cat backend/.env
```

### CORS errors
```bash
# Update CORS_ORIGINS in .env to include your frontend URL
```

## 📚 Technology Stack

### Backend
- **FastAPI**: Modern async web framework
- **LangChain**: AI agent orchestration
- **Claude 3.5 Sonnet**: Natural language understanding
- **SQLAlchemy**: Database ORM
- **SQLite**: Lightweight database
- **Pydantic**: Data validation

### Frontend (Coming Soon)
- **React 18**: UI framework
- **TypeScript**: Type safety
- **Recharts**: Data visualization
- **TailwindCSS**: Styling
- **Axios**: HTTP client

## 🔮 Future Enhancements

- [ ] Frontend React application
- [ ] Real-time streaming responses
- [ ] Query history and favorites
- [ ] Export to CSV/Excel
- [ ] Multi-user sessions
- [ ] Advanced analytics (forecasting, anomaly detection)
- [ ] Custom dashboard builder
- [ ] Email report scheduling

## 📄 License

MIT License - feel free to use for learning and demos

## 🤝 Contributing

This is a demo project. Feel free to fork and customize for your needs!

## 📞 Support

For issues or questions, please check:
- API Documentation: http://localhost:8000/docs
- Architecture Notes: `notes.md`
- Sample Queries: GET /api/sample-queries

---

**Built with ❤️ using Claude, LangChain, and FastAPI**