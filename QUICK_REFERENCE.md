# Quick Reference Card

## Installation Commands

### Ollama Setup (Free, Local)
```bash
# 1. Download Ollama from https://ollama.ai

# 2. Install a model
ollama pull llama3.1:8b

# 3. Verify
ollama list
```

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Configuration (.env file)

### Ollama (Default - Free!)
```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.1:8b
```

### Anthropic (Optional - Paid)
```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

## Common Commands

### Check Ollama Status
```bash
curl http://localhost:11434/api/tags
```

### List Downloaded Models
```bash
ollama list
```

### Test a Model
```bash
ollama run llama3.1:8b "Test message"
```

### Check Backend Health
```bash
curl http://localhost:8000/api/health
```

### Search Trials (API Test)
```bash
curl "http://localhost:8000/api/trials/search?condition=diabetes&max_results=3"
```

## Recommended Models

| Model | Command | Size | RAM | Quality |
|-------|---------|------|-----|---------|
| Llama 3.1 8B ⭐ | `ollama pull llama3.1:8b` | 4.7GB | 8GB | ★★★★★ |
| Mistral | `ollama pull mistral` | 4.1GB | 8GB | ★★★★☆ |
| Qwen 2.5 7B | `ollama pull qwen2.5:7b` | 4.7GB | 8GB | ★★★★★ |
| Phi-3 14B | `ollama pull phi3:14b` | 7.9GB | 16GB | ★★★★★ |

## Troubleshooting Quick Fixes

### Backend won't start
```bash
# Make sure venv is activated
source venv/bin/activate  # or venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

### "Cannot connect to Ollama"
```bash
# Check if running
ollama list

# If not, start it
ollama serve
```

### Frontend won't start
```bash
# Reinstall dependencies
rm -rf node_modules
npm install
```

### Slow performance
```bash
# Use smaller model
ollama pull mistral

# Edit .env
OLLAMA_MODEL=mistral
```

## File Structure

```
portfolio/
├── README.md                  # Main documentation
├── QUICKSTART.md             # 5-minute setup
├── OLLAMA_SETUP.md           # Ollama detailed guide
├── WHY_OLLAMA.md             # Why use Ollama
├── CHANGES_SUMMARY.md        # What changed
├── QUICK_REFERENCE.md        # This file
├── DEMO.md                   # Demo scenarios
│
├── backend/
│   ├── main.py               # FastAPI app
│   ├── requirements.txt      # Python dependencies
│   ├── .env.example          # Configuration template
│   ├── core/config.py        # Settings
│   ├── models/               # Data models
│   ├── services/
│   │   ├── matcher.py        # LLM integration ⭐
│   │   └── clinicaltrials_client.py
│   └── api/routes/           # API endpoints
│
└── frontend/
    ├── package.json          # Node dependencies
    ├── src/
    │   ├── App.jsx          # Main component
    │   └── components/       # UI components
    └── vite.config.js       # Build config
```

## URLs

### Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Health Checks
- API Health: http://localhost:8000/api/health
- Ollama: http://localhost:11434/api/tags

### Resources
- Ollama: https://ollama.ai
- Anthropic: https://console.anthropic.com/
- ClinicalTrials.gov: https://clinicaltrials.gov/

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `LLM_PROVIDER` | No | `ollama` | "ollama" or "anthropic" |
| `OLLAMA_BASE_URL` | No | `http://localhost:11434` | Ollama server URL |
| `OLLAMA_MODEL` | No | `llama3.1:8b` | Ollama model name |
| `ANTHROPIC_API_KEY` | Only for Anthropic | - | Claude API key |
| `CLINICALTRIALS_API_URL` | No | `https://clinicaltrials.gov/api/v2` | Trials API |
| `ENABLE_CACHE` | No | `True` | Enable trial caching |

## Performance

### Ollama (llama3.1:8b)
- First match: 10-15s (loading)
- After: 5-8s per match
- 10 trials: ~60-90s
- **Cost: $0**

### Anthropic Claude
- Each match: 3-5s
- 10 trials: ~30-50s
- **Cost: ~$0.10-0.20**

## Switching Providers

### To Ollama
1. Edit `.env`: `LLM_PROVIDER=ollama`
2. Install Ollama: https://ollama.ai
3. Download model: `ollama pull llama3.1:8b`
4. Restart: `python main.py`

### To Anthropic
1. Get API key: https://console.anthropic.com/
2. Edit `.env`:
   ```
   LLM_PROVIDER=anthropic
   ANTHROPIC_API_KEY=sk-ant-...
   ```
3. Restart: `python main.py`

## Demo Patient Data (Quick Test)

```json
{
  "age": 55,
  "gender": "male",
  "conditions": [
    {"name": "Type 2 Diabetes Mellitus"}
  ],
  "lab_results": [
    {"test_name": "HbA1c", "value": 7.5, "unit": "%"}
  ],
  "smoking_status": "former"
}
```

Search for: **"diabetes"**

## Git Commands

```bash
# Create new repo
git init
git add .
git commit -m "Initial commit: Clinical Trial Matcher with Ollama"

# Push to GitHub
git remote add origin https://github.com/yourusername/clinical-trial-matcher.git
git push -u origin main
```

## Safety Tips

### ✅ DO:
- Use Ollama for portfolio/demo
- Commit `.env.example` to Git
- Test both providers locally
- Share the GitHub repo freely

### ❌ DON'T:
- Commit `.env` to Git
- Share API keys publicly
- Deploy with hardcoded keys
- Forget to update `.gitignore`

## Support

### Documentation Files:
1. [QUICKSTART.md](QUICKSTART.md) - Get started fast
2. [OLLAMA_SETUP.md](OLLAMA_SETUP.md) - Ollama details
3. [README.md](README.md) - Full documentation
4. [WHY_OLLAMA.md](WHY_OLLAMA.md) - Why Ollama?
5. [DEMO.md](DEMO.md) - Demo scenarios

### Check if things are working:
```bash
# Backend running?
curl http://localhost:8000/api/health

# Ollama running?
curl http://localhost:11434/api/tags

# Frontend running?
curl http://localhost:3000
```

---

**Print this page and keep it handy! 📋**
