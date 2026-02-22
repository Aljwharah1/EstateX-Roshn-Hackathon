# EstateX Integration Test Guide

This guide will help you run the comprehensive integration tests for the EstateX application to verify that all components are properly connected.

## ✅ Components Tested

1. **Frontend Accessibility** - HTML pages (home, chatbot, login)
2. **Backend Health** - FastAPI server connectivity
3. **Data Loading** - Excel dataset import
4. **XGBoost Model** - ML model initialization
5. **Recommender System** - Property recommendation engine
6. **API Endpoints** - /recommend and /ask endpoints
7. **Investment Forecasting** - Revenue prediction for investment goals
8. **OpenAI LLM Integration** - Chatbot with GPT-4
9. **Supabase Database** - Frontend database configuration
10. **End-to-End Workflow** - Complete user journey

## 🚀 Quick Start

### Step 1: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 2: Set Up Environment Variables

Create a `.env` file in the project root (or update the existing one):

```env
OPENAI_API_KEY=your_openai_api_key_here
```

**Get your OpenAI API key:**
- Visit https://platform.openai.com/api-keys
- Create a new API key
- Copy it to your `.env` file

### Step 3: Start the Backend Server

In a PowerShell terminal, run:

```powershell
# Navigate to project directory
cd c:\Users\HP\EstateX-Roshn-Hackathon

# Start FastAPI server
uvicorn app.main:app --reload
```

**Expected output:**
```
Uvicorn running on http://127.0.0.1:8000
```

Keep this terminal open while running tests.

### Step 4: Run Integration Tests

In a **new PowerShell terminal**, run:

```powershell
# Navigate to project directory
cd c:\Users\HP\EstateX-Roshn-Hackathon

# Run all integration tests
python test_integration.py
```

## 📊 Expected Output

The test suite will display:
- ✓ for passed tests (green)
- ✗ for failed tests (red)
- ⚠ for warnings (yellow)

### Sample Output
```
======================================================================
  EstateX - Complete Integration Test Suite
  Testing all components: Backend, Frontend, Database, Model, LLM
======================================================================

[Test results...]

======================================================================
Integration Test Summary
======================================================================
  ✓ Environment Setup: PASS
  ✓ Data Loading: PASS
  ✓ XGBoost Model: PASS
  ✓ Recommender System: PASS
  ✓ Backend Health: PASS
  ✓ Frontend Accessibility: PASS
  ✓ Recommender Endpoint: PASS
  ✓ Investment Forecasting: PASS
  ✓ Chatbot Endpoint (OpenAI LLM): PASS
  ✓ Supabase Integration: PASS
  ✓ End-to-End Workflow: PASS

Passed: 11/11 tests

✓ All integration tests passed! System is fully connected and operational.
```

## 🔧 Troubleshooting

### Issue: "Cannot connect to backend at http://localhost:8000"

**Solution:** Make sure the FastAPI server is running
- Check that you ran `uvicorn app.main:app --reload`
- Check that the terminal shows "Uvicorn running on http://127.0.0.1:8000"
- Try accessing http://localhost:8000 in your browser

### Issue: "OpenAI API key not found"

**Solution:** Set the OPENAI_API_KEY environment variable
```powershell
$env:OPENAI_API_KEY = "your-api-key-here"
```

### Issue: "Dataset not found at data/Finalized_Data.xlsx"

**Solution:** Ensure the data file exists
- Check that `data/Finalized_Data.xlsx` exists in the project
- If missing, download it from your data source

### Issue: "XGBoost model file missing"

**Solution:** This is expected if model files haven't been generated
- Run the training notebook: `training/train_xgboost.ipynb`
- This will generate `models/xgb_model.json` and `models/encoders.pkl`

## 📋 Component Status Indicators

| Component | Expected Status | Notes |
|-----------|-----------------|-------|
| Backend | PASS | Must be running for endpoint tests |
| Frontend | PASS | HTML files should be accessible |
| Data | PASS | Excel file must exist |
| Model | PASS/WARNING | Optional - forecasting will be disabled without it |
| Recommender | PASS | Core functionality, requires data |
| LLM | PASS/WARNING | Optional - requires OpenAI API key |
| Supabase | PASS | Configuration checked in frontend code |
| Database | N/A | Full test requires browser interaction |

## 🧪 Running Individual Tests

To debug specific components, you can run Python commands directly:

### Test Data Loading
```powershell
python -c "import pandas as pd; df = pd.read_excel('data/Finalized_Data.xlsx'); print(f'Loaded {len(df)} records')"
```

### Test Backend Connection
```powershell
python -c "import requests; r = requests.get('http://localhost:8000'); print(f'Status: {r.status_code}')"
```

### Test Recommender Directly
```powershell
python -c "
from app.recommender import RuleBasedRecommender
import pandas as pd
df = pd.read_excel('data/Finalized_Data.xlsx')
rec = RuleBasedRecommender(df)
prefs = {'goal': 'residential', 'min_budget': 2000000, 'max_budget': 5000000}
results = rec.recommend(prefs)
print(f'Found {len(results)} recommendations')
"
```

## 📞 Support

If you encounter any issues:
1. Check the error messages carefully
2. Review the troubleshooting section above
3. Verify all environment variables are set
4. Ensure the backend server is running
5. Check that all required files exist

## 🎯 Success Criteria

Your system is fully integrated when:
- ✓ All 11 tests pass
- ✓ Backend server runs without errors
- ✓ API endpoints respond within 10 seconds
- ✓ Chatbot endpoint returns LLM responses
- ✓ Recommender returns 5+ results for queries
- ✓ Frontend pages load successfully
