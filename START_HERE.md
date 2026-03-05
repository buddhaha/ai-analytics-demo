# 🚀 How to Start the AI Analytics Project

Follow these steps to get the application running on your machine.

## Prerequisites Check

Before starting, make sure you have:
- ✅ Python 3.11 or higher installed
- ✅ Node.js 18 or higher installed
- ✅ An OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

Check versions:
```bash
python --version  # Should be 3.11+
node --version    # Should be 18+
npm --version
```

---

## Step 1: Backend Setup (5 minutes)

### Option A: Automated Setup (Recommended)

```bash
# Navigate to backend directory
cd backend

# Run setup script
chmod +x setup.sh
./setup.sh

# Edit .env file and add your API key
nano .env  # or use any text editor
# Add: OPENAI_API_KEY=sk-your-key-here
```

### Option B: Manual Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here

# Create and seed database
python scripts/seed_data.py
```

### Start Backend Server

```bash
# Make sure you're in backend directory with venv activated
python -m app.main
```

You should see:
```
🚀 Starting AI Analytics API...
📊 Database: sqlite:///./database/ecommerce.db
🤖 AI Model: OpenAI GPT-4
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ **Backend is running!** Keep this terminal open.

Test it: Open http://localhost:8000/docs in your browser

---

## Step 2: Frontend Setup (3 minutes)

Open a **NEW terminal window** (keep backend running in the first one)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

You should see:
```
  VITE v5.0.11  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

✅ **Frontend is running!**

---

## Step 3: Use the Application

1. Open your browser to: **http://localhost:5173**

2. You'll see the AI Analytics interface with sample queries

3. Try asking a question like:
   - "Show me the top 10 customers by revenue"
   - "What are the best selling products?"
   - "Compare Q1 vs Q2 sales"

4. Watch as the AI:
   - Generates SQL
   - Executes the query
   - Analyzes results
   - Creates visualizations

---

## 🎯 Quick Test

To verify everything works:

1. **Backend Test:**
   ```bash
   curl http://localhost:8000/api/health
   ```
   Should return: `{"status":"healthy","service":"AI Analytics API","version":"1.0.0"}`

2. **Frontend Test:**
   Open http://localhost:5173 - you should see the welcome screen

3. **Full Test:**
   Click on a sample query or type: "Show me total revenue"

---

## 🛑 Stopping the Application

1. **Stop Frontend:** Press `Ctrl+C` in the frontend terminal
2. **Stop Backend:** Press `Ctrl+C` in the backend terminal
3. **Deactivate Python venv:** Type `deactivate` in backend terminal

---

## 🔄 Restarting Later

### Backend
```bash
cd backend
source venv/bin/activate  # On macOS/Linux
# OR venv\Scripts\activate on Windows
python -m app.main
```

### Frontend
```bash
cd frontend
npm run dev
```

---

## ❌ Troubleshooting

### "Module not found" errors (Backend)
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### "Database not found" error
```bash
cd backend
python scripts/seed_data.py
```

### "Invalid API key" error
- Check that `.env` file exists in `backend/` directory
- Verify your `OPENAI_API_KEY` is correct
- Make sure there are no extra spaces or quotes

### Port 8000 already in use
```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9  # macOS/Linux
# OR
netstat -ano | findstr :8000   # Windows (then kill the PID)
```

### Port 5173 already in use
```bash
# Use a different port
npm run dev -- --port 3000
```

### Frontend can't connect to backend
- Verify backend is running on http://localhost:8000
- Check browser console for errors
- Try accessing http://localhost:8000/docs directly

### npm install fails
```bash
# Clear cache and retry
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

---

## 📁 Project Structure

```
Current Directory: /path/to/ai-analytics-demo/

├── backend/          # Python FastAPI backend
│   ├── app/         # Application code
│   ├── scripts/     # Utility scripts
│   └── .env         # Your API key (create this!)
│
├── frontend/        # React frontend
│   ├── src/        # Source code
│   └── package.json
│
└── database/        # SQLite database
    └── ecommerce.db # (created by seed script)
```

---

## 🎓 Next Steps

Once running:

1. **Explore Sample Queries** - Click on the suggested questions
2. **Try Custom Questions** - Ask anything about the e-commerce data
3. **View SQL** - See how your questions become SQL queries
4. **Read Insights** - Check out AI-generated analysis
5. **Explore Visualizations** - See automatic chart generation

---

## 📚 Additional Resources

- **Full Documentation:** See `README.md`
- **Quick Reference:** See `QUICKSTART.md`
- **Architecture Details:** See `notes.md`
- **API Documentation:** http://localhost:8000/docs (when backend is running)
- **Frontend Docs:** See `frontend/README.md`

---

## 🆘 Need Help?

1. Check the troubleshooting section above
2. Review the error messages in the terminal
3. Check `README.md` for detailed information
4. Verify all prerequisites are installed

---

**Ready to start? Begin with Step 1! 🚀**