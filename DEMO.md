# Clinical Trial Matcher - Demo Guide

This guide will walk you through a complete demo of the Clinical Trial Matcher application.

## Quick Start

### 1. Start the Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
python main.py
```

Backend will run at: `http://localhost:8000`

### 2. Start the Frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend will run at: `http://localhost:3000`

## Demo Scenario 1: Type 2 Diabetes Patient

This scenario demonstrates matching a diabetic patient to clinical trials.

### Patient Profile

**Demographics:**
- Age: 55
- Gender: Male
- Smoking Status: Former

**Conditions:**
- Name: Type 2 Diabetes Mellitus
- ICD-10: E11.9
- Onset: 2020-03-15

**Medications:**
- Metformin, 500mg, twice daily

**Lab Results:**
- HbA1c: 7.5%
- Fasting Glucose: 145 mg/dL

**Search Condition:** "Type 2 Diabetes"

### Expected Results

The system should:
1. Find 10-20 diabetes clinical trials
2. Match the patient against each trial's criteria
3. Return ranked results with match scores
4. Show which trials the patient is eligible for
5. Explain why criteria were met or not met

Typical matches might include:
- Trials testing new diabetes medications
- Studies for patients with HbA1c 7-10%
- Trials requiring metformin background therapy
- Studies excluding patients with kidney disease (patient should pass)

## Demo Scenario 2: Cancer Patient

### Patient Profile

**Demographics:**
- Age: 62
- Gender: Female
- Smoking Status: Never
- Pregnancy Status: Not pregnant

**Conditions:**
- Name: Breast Cancer
- ICD-10: C50.9
- Onset: 2023-06-01

**Medications:**
- Tamoxifen, 20mg, once daily

**Lab Results:**
- WBC: 5.5 K/uL
- Hemoglobin: 12.8 g/dL
- Platelets: 250 K/uL

**Search Condition:** "Breast Cancer"

### Expected Results

The system should find breast cancer trials and evaluate:
- Age requirements (many trials 18-75)
- Cancer stage and type
- Prior treatments
- Lab values for bone marrow function
- Hormone receptor status

## Demo Scenario 3: Edge Case - Pregnant Patient

### Patient Profile

**Demographics:**
- Age: 28
- Gender: Female
- Smoking Status: Never
- Pregnancy Status: **Pregnant** ✓

**Conditions:**
- Name: Gestational Diabetes
- Onset: 2023-11-01

**Search Condition:** "Diabetes in Pregnancy"

### Expected Results

This demonstrates the system's handling of exclusion criteria:
- Most diabetes trials exclude pregnant women
- Should receive low match scores
- Exclusion violations should clearly state pregnancy exclusion
- May find trials specifically for gestational diabetes

## Testing the API Directly

### Health Check
```bash
curl http://localhost:8000/api/health
```

### Search Trials
```bash
curl "http://localhost:8000/api/trials/search?condition=diabetes&max_results=5"
```

### Match Patient (Example)
```bash
curl -X POST "http://localhost:8000/api/matching/match?condition=diabetes" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 55,
    "gender": "male",
    "conditions": [
      {"name": "Type 2 Diabetes Mellitus", "icd10_code": "E11.9"}
    ],
    "lab_results": [
      {"test_name": "HbA1c", "value": 7.5, "unit": "%"}
    ],
    "smoking_status": "former"
  }'
```

## Expected Performance

### Response Times
- Trial Search: 2-5 seconds (first time), <1 second (cached)
- Single Match: 3-5 seconds (Claude API call)
- Full Matching (10 trials): 30-60 seconds

### Cache Behavior
- Trials are cached for 24 hours
- Subsequent searches for same condition are instant
- Cache stored in `backend/trials_cache/`

## Export Features

After getting match results:

1. **CSV Export**: Downloads spreadsheet with all matches
   - Columns: NCT ID, Title, Score, Eligible, Explanation, Criteria
   - Good for Excel analysis

2. **JSON Export**: Downloads structured data
   - Complete match objects
   - Good for programmatic processing

## Troubleshooting

### "Error: ANTHROPIC_API_KEY not configured"
- Ensure `.env` file exists in backend/
- Verify API key starts with `sk-ant-`
- Restart backend after changing `.env`

### No Trials Found
- Try broader search terms ("diabetes" vs "type 2 diabetes mellitus")
- Check ClinicalTrials.gov is accessible
- Look at backend logs for API errors

### Slow Matching
- First search is slow (querying ClinicalTrials.gov)
- Matching 10 trials takes ~30-60 seconds (10 Claude API calls)
- This is normal - real AI analysis takes time
- Consider reducing `max_trials` for faster demos

### Frontend Can't Connect
- Ensure backend is running on port 8000
- Check Vite proxy configuration
- Try accessing `http://localhost:8000/api/health` directly

## Demo Tips

1. **Start with Diabetes**: Most trials available, clear criteria
2. **Show the Explanation**: AI explanations are the key feature
3. **Compare Scores**: Show why one trial scores 90% vs 40%
4. **Demonstrate Exclusions**: Pregnant patient shows exclusion handling
5. **Export Results**: Show the CSV/JSON export features
6. **Highlight Privacy**: Mention no data is saved

## What to Showcase

This project demonstrates:
- ✅ Real API integration (ClinicalTrials.gov)
- ✅ AI/LLM usage (Claude for criteria analysis)
- ✅ Healthcare data modeling
- ✅ Complex eligibility logic
- ✅ Modern full-stack development
- ✅ User-friendly medical interface
- ✅ Privacy-conscious design

## Next Steps

After the demo, potential discussion points:
- How to make this HIPAA compliant
- Scaling to thousands of trials
- Adding FHIR support
- Integration with EHR systems
- Validation with clinical professionals
- Multi-language support
- Real-time trial updates

---

**Have fun demonstrating! This is a solid portfolio piece showing healthcare + AI integration.**
