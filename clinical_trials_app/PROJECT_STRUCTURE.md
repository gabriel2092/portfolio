# Clinical Trial Matcher - Project Structure

## Directory Layout

```
portfolio/
│
├── README.md                      # Main project documentation
├── DEMO.md                        # Demo scenarios and guide
├── PROJECT_STRUCTURE.md           # This file
├── .gitignore                     # Git ignore rules
│
├── backend/                       # FastAPI Python Backend
│   ├── main.py                   # Application entry point
│   ├── requirements.txt          # Python dependencies
│   ├── .env.example              # Environment variables template
│   ├── run.sh                    # Linux/Mac start script
│   ├── run.bat                   # Windows start script
│   │
│   ├── core/                     # Core configuration
│   │   ├── __init__.py
│   │   └── config.py             # Settings and environment config
│   │
│   ├── models/                   # Data models (Pydantic)
│   │   ├── __init__.py
│   │   ├── patient.py            # Patient/EMR data models
│   │   └── trial.py              # Trial and match result models
│   │
│   ├── services/                 # Business logic
│   │   ├── __init__.py
│   │   ├── clinicaltrials_client.py  # ClinicalTrials.gov API client
│   │   └── matcher.py            # Claude AI matching service
│   │
│   └── api/                      # API routes
│       ├── __init__.py
│       └── routes/
│           ├── __init__.py
│           ├── trials.py         # Trial search endpoints
│           └── matching.py       # Matching endpoints
│
└── frontend/                     # React Frontend
    ├── package.json              # Node dependencies
    ├── vite.config.js            # Vite configuration
    ├── index.html                # HTML entry point
    │
    └── src/
        ├── main.jsx              # React entry point
        ├── App.jsx               # Main application component
        ├── index.css             # Global styles
        │
        └── components/
            ├── PatientForm.jsx   # Patient data entry form
            └── MatchResults.jsx  # Match results display
```

## Key Components

### Backend Components

#### 1. **main.py**
- FastAPI application setup
- CORS middleware configuration
- Route registration
- Health check endpoints

#### 2. **core/config.py**
- Environment variable management
- Application settings
- Pydantic Settings integration

#### 3. **models/patient.py**
- `PatientData`: Complete patient record
- `Condition`: Medical condition with ICD-10
- `Medication`: Current medication record
- `LabResult`: Laboratory test results
- `Gender`: Enumeration for gender values

#### 4. **models/trial.py**
- `ClinicalTrial`: Trial information from ClinicalTrials.gov
- `MatchResult`: Complete matching result with scoring and explanations

#### 5. **services/clinicaltrials_client.py**
- `ClinicalTrialsClient`: API client for ClinicalTrials.gov
- Trial search by condition/keywords
- Individual trial retrieval
- Local caching (24-hour expiry)
- API response parsing

#### 6. **services/matcher.py**
- `TrialMatcher`: Claude AI integration
- Patient data formatting
- Eligibility analysis
- Match scoring algorithm
- Structured output parsing

#### 7. **api/routes/trials.py**
- `GET /api/trials/search`: Search for trials
- `GET /api/trials/{nct_id}`: Get specific trial

#### 8. **api/routes/matching.py**
- `POST /api/matching/match`: Match patient to trials
- `POST /api/matching/match/{nct_id}`: Match to specific trial
- `POST /api/matching/export/csv`: Export as CSV
- `POST /api/matching/export/json`: Export as JSON

### Frontend Components

#### 1. **App.jsx**
- Main application state management
- API communication
- Error handling
- Component orchestration

#### 2. **components/PatientForm.jsx**
- Patient demographics input
- Dynamic condition/medication/lab arrays
- Form validation
- Submission handling

#### 3. **components/MatchResults.jsx**
- Match display with scoring
- Criteria breakdown visualization
- Export functionality
- Result filtering and sorting

#### 4. **index.css**
- Responsive design
- Gradient color scheme
- Card-based layout
- Accessibility considerations

## Data Flow

### 1. Search Flow
```
User Input → PatientForm → API Request → Backend
  → ClinicalTrialsClient → ClinicalTrials.gov API
  → Cache → Response → Frontend
```

### 2. Matching Flow
```
Patient Data → API Request → Backend
  → ClinicalTrialsClient (search trials)
  → TrialMatcher (for each trial)
    → Format patient data
    → Claude API call
    → Parse response
  → Aggregate results
  → Sort by score
  → Return to Frontend
  → MatchResults display
```

### 3. Export Flow
```
Match Results → Export Button → API Request
  → Format as CSV/JSON → Stream response
  → Browser download
```

## API Architecture

### REST Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Health check |
| GET | `/api/health` | Detailed health status |
| GET | `/api/trials/search` | Search trials |
| GET | `/api/trials/{nct_id}` | Get specific trial |
| POST | `/api/matching/match` | Match patient to trials |
| POST | `/api/matching/match/{nct_id}` | Match to specific trial |
| POST | `/api/matching/export/csv` | Export CSV |
| POST | `/api/matching/export/json` | Export JSON |

### Request/Response Flow

1. **Trial Search**
   - Input: condition, keywords, max_results
   - Output: List[ClinicalTrial]

2. **Patient Matching**
   - Input: PatientData + condition
   - Process: Search → Match → Score
   - Output: List[MatchResult] (sorted by score)

3. **Export**
   - Input: List[MatchResult]
   - Output: File stream (CSV or JSON)

## Technology Stack Summary

### Backend Stack
- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **httpx**: Async HTTP client
- **Anthropic SDK**: Claude API integration
- **python-dotenv**: Environment management

### Frontend Stack
- **React 18**: UI framework
- **Vite**: Build tool
- **Axios**: HTTP client
- **CSS3**: Styling

### External APIs
- **ClinicalTrials.gov API v2**: Trial data
- **Anthropic Claude API**: AI matching

## Development Workflow

### Local Development

1. **Backend**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   # Add ANTHROPIC_API_KEY to .env
   python main.py
   ```

2. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

### Production Build

1. **Backend**:
   ```bash
   pip install -r requirements.txt
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

2. **Frontend**:
   ```bash
   npm run build
   # Serve the dist/ directory
   ```

## Caching Strategy

- **Location**: `backend/trials_cache/`
- **Format**: JSON files
- **Key**: Hash of query parameters
- **Expiry**: 24 hours
- **Benefits**:
  - Faster subsequent searches
  - Reduced API calls
  - Better user experience

## Error Handling

### Backend
- Input validation (Pydantic)
- API error handling (try/catch)
- Logging (Python logging)
- HTTP error responses

### Frontend
- API error display
- Loading states
- User-friendly messages
- Form validation

## Security Considerations

### Current Implementation
- API keys in environment variables
- No persistent patient data storage
- CORS configuration
- Input validation

### Production Recommendations
- HTTPS only
- Rate limiting
- Authentication/authorization
- Database encryption
- HIPAA compliance measures
- Audit logging

## Performance Considerations

### Bottlenecks
1. ClinicalTrials.gov API (2-5 seconds)
2. Claude API calls (3-5 seconds each)
3. Sequential matching (10 trials = 30-60 seconds)

### Optimizations
- Local caching (implemented)
- Async operations (implemented)
- Potential: Parallel Claude API calls
- Potential: Result pagination
- Potential: Background job processing

## Future Architecture Enhancements

1. **Database Layer**: PostgreSQL for patient records
2. **Message Queue**: Celery for background matching
3. **Caching**: Redis instead of file-based
4. **Authentication**: OAuth2/JWT
5. **Containerization**: Docker + Docker Compose
6. **CI/CD**: GitHub Actions
7. **Monitoring**: Prometheus + Grafana
8. **Logging**: ELK stack

---

This structure provides a clean separation of concerns, maintainability, and scalability for a production-ready clinical trial matching application.
