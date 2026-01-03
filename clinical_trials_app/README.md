# Clinical Trial Matcher

An AI-powered clinical trial matching application that connects patients with relevant clinical trials using real-time data from ClinicalTrials.gov and AI (Ollama or Claude) for intelligent eligibility analysis.

## Overview

This portfolio project demonstrates:
- Integration with ClinicalTrials.gov API v2 for real clinical trial data
- AI-powered eligibility criteria analysis using **Ollama (free, local)** or Claude API (cloud)
- Modern full-stack architecture (FastAPI + React)
- Healthcare data modeling (EMR-like patient records)
- Structured data extraction and matching algorithms

## Features

- **Patient Data Entry**: Comprehensive form for entering patient demographics, conditions, medications, and lab results
- **Trial Search**: Search ClinicalTrials.gov by medical condition with automatic caching
- **AI Matching**: Local LLMs (Ollama) or Claude AI analyze complex inclusion/exclusion criteria and match patients
- **Flexible LLM Backend**: Choose between free local models or cloud API
- **Match Scoring**: Each trial receives a 0-100% match score with detailed explanations
- **Criteria Breakdown**: Clear visualization of which criteria were met or not met
- **Export Results**: Download match results as CSV or JSON
- **Privacy-Focused**: No persistent patient data storage

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Ollama**: Local open source LLMs (Llama, Mistral, Qwen) - **Free!**
- **Anthropic Claude API** (optional): Cloud AI for faster matching
- **ClinicalTrials.gov API v2**: Real clinical trial data
- **Pydantic**: Data validation and modeling
- **httpx**: Async HTTP client

### Frontend
- **React**: UI framework
- **Vite**: Build tool and dev server
- **Axios**: HTTP client
- **CSS**: Custom styling with gradient design

## Architecture

```
portfolio/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── core/
│   │   └── config.py           # Configuration management
│   ├── models/
│   │   ├── patient.py          # Patient data models
│   │   └── trial.py            # Trial and match models
│   ├── services/
│   │   ├── clinicaltrials_client.py  # ClinicalTrials.gov API
│   │   └── matcher.py          # Claude AI matching logic
│   └── api/
│       └── routes/
│           ├── trials.py       # Trial search endpoints
│           └── matching.py     # Matching endpoints
└── frontend/
    ├── src/
    │   ├── App.jsx             # Main application
    │   ├── components/
    │   │   ├── PatientForm.jsx # Patient data entry
    │   │   └── MatchResults.jsx # Results display
    │   └── index.css           # Styling
    └── package.json
```

## Setup Instructions

### Prerequisites

- Python 3.9+
- Node.js 18+
- **Option A (Recommended)**: [Ollama](https://ollama.ai) - Free, local LLMs (no API key needed!)
- **Option B**: Anthropic API key ([get one here](https://console.anthropic.com/)) - Cloud API

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file from the example:
```bash
cp .env.example .env
```

5. **Choose your LLM provider:**

   **Option A: Ollama (Free, Local - Recommended)**

   1. Install Ollama from [https://ollama.ai](https://ollama.ai)
   2. Download a model: `ollama pull llama3.1:8b`
   3. Your `.env` should have:
   ```env
   LLM_PROVIDER=ollama
   OLLAMA_MODEL=llama3.1:8b
   ```

   See [OLLAMA_SETUP.md](OLLAMA_SETUP.md) for detailed instructions.

   **Option B: Anthropic Claude (Cloud API)**

   Edit `.env` and add:
   ```env
   LLM_PROVIDER=anthropic
   ANTHROPIC_API_KEY=your_api_key_here
   ```

6. Start the backend server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Usage

1. **Enter Search Condition**: Enter a medical condition (e.g., "Type 2 Diabetes", "Breast Cancer")

2. **Fill Patient Information**:
   - Demographics: Age, gender, smoking status
   - Medical conditions with ICD-10 codes
   - Current medications with dosage
   - Lab results (e.g., HbA1c, glucose levels)

3. **Find Matches**: Click "Find Matching Trials" to:
   - Search ClinicalTrials.gov for relevant trials
   - Use Claude AI to analyze eligibility criteria
   - Display ranked results with match scores

4. **Review Results**: Each trial shows:
   - Match percentage (0-100%)
   - Eligibility determination
   - Inclusion criteria met/not met
   - Exclusion criteria violations/passes
   - Detailed AI explanation

5. **Export**: Download results as CSV or JSON for further analysis

## Example Use Case

**Patient Profile:**
- 55-year-old male
- Type 2 Diabetes Mellitus (E11.9)
- HbA1c: 7.5%
- Current medication: Metformin 500mg twice daily
- Former smoker

**Result:** The system searches for diabetes trials and matches the patient against each trial's inclusion/exclusion criteria, providing a ranked list of suitable trials with detailed explanations.

## API Endpoints

### Trials

- `GET /api/trials/search?condition={condition}` - Search for trials
- `GET /api/trials/{nct_id}` - Get specific trial details

### Matching

- `POST /api/matching/match?condition={condition}` - Match patient to trials
- `POST /api/matching/match/{nct_id}` - Match patient to specific trial
- `POST /api/matching/export/csv` - Export results as CSV
- `POST /api/matching/export/json` - Export results as JSON

### Health

- `GET /` - API health check
- `GET /api/health` - Detailed health status

## How It Works

### 1. Trial Search
The application queries ClinicalTrials.gov API v2 to find trials matching the search condition. Results are cached locally to improve performance.

### 2. AI Analysis
For each trial, Claude AI receives:
- Complete patient profile
- Trial eligibility criteria (inclusion/exclusion)

Claude analyzes the criteria in structured format and returns:
- Eligibility determination (yes/no)
- Match score (0.0-1.0)
- Detailed breakdown of criteria matches/mismatches
- Human-readable explanation

### 3. Scoring Algorithm
- **1.0 (100%)**: Perfect match, all inclusion met, no exclusions violated
- **0.8-0.9**: Strong match, minor uncertainties
- **0.6-0.7**: Moderate match, some unclear criteria
- **0.4-0.5**: Weak match, significant mismatches
- **0.0-0.3**: Poor match or exclusion violated

### 4. Results Display
Matches are sorted by score (highest first) and displayed with full transparency about why each match succeeded or failed.

## Privacy & Security

- **No Persistent Storage**: Patient data is not saved to any database
- **In-Memory Processing**: All patient data exists only during the request
- **HIPAA Awareness**: Designed with healthcare privacy principles in mind
- **API Key Security**: Sensitive keys stored in environment variables

## Limitations & Disclaimer

**This is a portfolio/educational project, not a clinical tool:**

- ❌ Not validated for clinical use
- ❌ Not HIPAA compliant for production
- ❌ Should not be used for actual patient care decisions
- ❌ AI analysis may miss nuanced medical criteria
- ✅ Demonstrates technical capabilities
- ✅ Shows integration with healthcare APIs
- ✅ Illustrates AI application in healthcare

Always consult qualified healthcare professionals for clinical trial matching in real-world scenarios.

## Future Enhancements

Potential improvements for this project:
- FHIR-compliant patient data import
- Integration with additional trial databases (EU Clinical Trials, WHO ICTRP)
- Multi-language support for international trials
- Machine learning model for criteria extraction
- Real-time eligibility updates as patient data changes
- Patient consent and data encryption
- Trial site distance calculation
- Email notifications for new matching trials

## Technologies Demonstrated

This project showcases:
- ✅ RESTful API design with FastAPI
- ✅ AI/LLM integration (Claude API)
- ✅ External API integration (ClinicalTrials.gov)
- ✅ Healthcare data modeling
- ✅ React single-page application
- ✅ Data validation with Pydantic
- ✅ Async/await patterns in Python
- ✅ Caching strategies
- ✅ Export functionality (CSV, JSON)
- ✅ Error handling and logging
- ✅ Environment-based configuration

## License

This is a portfolio project created for educational and demonstration purposes.

## Contact

For questions about this project, please visit my portfolio or reach out via GitHub.

---

**Built with ❤️ to demonstrate healthcare technology capabilities**
