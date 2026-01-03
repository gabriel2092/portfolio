# Quick Start Guide

Get the Clinical Trial Matcher running in 5 minutes!

## Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- An Anthropic API key (free tier available at [console.anthropic.com](https://console.anthropic.com/))

## Step 1: Clone and Navigate

```bash
cd portfolio
```

## Step 2: Backend Setup (2 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env

# Edit .env and add your API key
# ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**Start the backend:**
```bash
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Keep this terminal open!

## Step 3: Frontend Setup (1 minute)

**Open a NEW terminal:**

```bash
# Navigate to frontend
cd portfolio/frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
```

## Step 4: Open in Browser

Visit: **http://localhost:3000**

You should see the Clinical Trial Matcher interface!

## Step 5: Test It Out

### Quick Test (30 seconds)

1. **Search Condition**: Enter "diabetes"
2. **Age**: 55
3. **Gender**: Male
4. Click **"+ Add Condition"**
   - Name: Type 2 Diabetes
5. Click **"+ Add Lab Result"**
   - Test: HbA1c
   - Value: 7.5
   - Unit: %
6. Click **"Find Matching Trials"**

Wait 30-60 seconds... you'll see:
- List of diabetes clinical trials
- Match scores for each trial
- Detailed eligibility explanations

## Troubleshooting

### Backend won't start
- **Error: "No module named 'fastapi'"**
  - Make sure virtual environment is activated
  - Run `pip install -r requirements.txt` again

- **Error: "ANTHROPIC_API_KEY not configured"**
  - Check `.env` file exists in `backend/`
  - Verify it contains: `ANTHROPIC_API_KEY=sk-ant-...`

### Frontend won't start
- **Error: "Cannot find module"**
  - Run `npm install` again
  - Delete `node_modules` and retry

- **Error: "Port 3000 already in use"**
  - Kill existing process or change port in `vite.config.js`

### Can't connect frontend to backend
- Verify backend is running on http://localhost:8000
- Try accessing http://localhost:8000/api/health in your browser
- Check Vite proxy settings in `frontend/vite.config.js`

### No trials found
- Check your internet connection
- Try simpler search terms ("diabetes" not "type 2 diabetes mellitus")
- Check backend logs for errors

### Matching is slow
- This is normal! Each trial takes 3-5 seconds to analyze
- 10 trials = 30-60 seconds total
- Reduce max_trials in the code for faster testing

## What Next?

- Read [README.md](README.md) for full documentation
- Try [DEMO.md](DEMO.md) for complete demo scenarios
- Explore [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) to understand the architecture

## API Testing (Optional)

Test the backend directly:

```bash
# Health check
curl http://localhost:8000/api/health

# Search trials
curl "http://localhost:8000/api/trials/search?condition=diabetes&max_results=3"
```

## Common Commands

### Backend
```bash
# Start backend
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python main.py

# Stop: Ctrl+C
```

### Frontend
```bash
# Start frontend
cd frontend
npm run dev

# Stop: Ctrl+C

# Build for production
npm run build
```

## Production Deployment Notes

This is a development setup. For production:

1. **Backend**: Use proper WSGI server (Gunicorn + Uvicorn workers)
2. **Frontend**: Build and serve static files (`npm run build`)
3. **Environment**: Never commit `.env` file
4. **Security**: Add authentication, rate limiting, HTTPS
5. **Database**: Add PostgreSQL for persistent data
6. **Monitoring**: Add logging and error tracking

## Getting Help

If you're stuck:
1. Check the error message carefully
2. Look at backend console for Python errors
3. Check browser console (F12) for JavaScript errors
4. Verify API key is valid
5. Try restarting both servers

---

**You're all set! Start matching patients to clinical trials! 🏥**
