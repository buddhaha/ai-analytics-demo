# 🚀 Quick Start Guide

Get the AI Analytics Demo running in 5 minutes!

## Prerequisites

- Python 3.11+
- Anthropic API key ([Get one here](https://console.anthropic.com/))

## Setup Steps

### 1. Run Setup Script (Recommended)

```bash
cd backend
./setup.sh
```

This will:
- Create virtual environment
- Install all dependencies
- Create .env file
- Generate sample database

### 2. Add Your API Key

Edit `backend/.env` and add your Anthropic API key:

```env
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
```

### 3. Start the Server

```bash
# Make sure you're in the backend directory
cd backend

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start the server
python -m app.main
```

The API will be running at: **http://localhost:8000**

### 4. Test the API

Open your browser and visit:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

## Try Your First Query

### Using the API Docs (Easiest)

1. Go to http://localhost:8000/docs
2. Click on `POST /api/query`
3. Click "Try it out"
4. Enter a question like: `"Show me the top 10 customers by revenue"`
5. Click "Execute"

### Using curl

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Show me the top 10 customers by revenue"}'
```

### Using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/api/query",
    json={"question": "Show me the top 10 customers by revenue"}
)

result = response.json()
print(f"SQL: {result['sql']}")
print(f"Results: {result['results']}")
print(f"Analysis: {result['analysis']}")
```

## Example Questions to Try

1. **Sales Analysis**
   - "Show me monthly revenue for 2025"
   - "What are the top selling products?"
   - "Compare Q1 vs Q2 sales"

2. **Customer Insights**
   - "Who are my best customers?"
   - "Show customers who haven't ordered in 3 months"
   - "What is the average order value by country?"

3. **Product Performance**
   - "Which products have the highest profit margins?"
   - "Show me products with low ratings but high sales"
   - "What are the top 5 products in Electronics?"

4. **Inventory & Operations**
   - "Which products are low in stock?"
   - "How many orders are pending?"
   - "Show me inventory by warehouse"

## Database Overview

The demo includes:
- **200 customers** from 10 countries
- **80 products** across 8 categories
- **500 orders** with realistic data
- **Product reviews** and ratings
- **Inventory** tracking

## Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### "Database not found"
```bash
python scripts/seed_data.py
```

### "Invalid API key"
Check that your `ANTHROPIC_API_KEY` in `.env` is correct

### Port 8000 already in use
```bash
# Use a different port
uvicorn app.main:app --port 8001
```

## Next Steps

- Explore the API documentation at http://localhost:8000/docs
- Check out `notes.md` for architecture details
- Read `README.md` for comprehensive documentation
- Build a frontend to visualize the results!

## Manual Setup (Alternative)

If the setup script doesn't work:

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
cp .env.example .env
# Edit .env and add your API key

# 4. Create database
python scripts/seed_data.py

# 5. Start server
python -m app.main
```

## Need Help?

- Check the logs in the terminal
- Visit http://localhost:8000/docs for API documentation
- Review `README.md` for detailed information
- Check `notes.md` for architecture diagrams

---

**Ready to build something amazing? Let's go! 🚀**