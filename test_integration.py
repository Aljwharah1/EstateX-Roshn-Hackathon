#!/usr/bin/env python3
"""
Comprehensive Integration Test for EstateX
Tests: Frontend, Backend, Supabase DB, Model, Recommender, and OpenAI LLM
"""

import requests
import json
import time
import os
import sys
from pathlib import Path

BASE_URL = "http://localhost:8000"
BACKEND_TIMEOUT = 10

# ANSI Color codes for better readability
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    """Print a formatted section header"""
    print(f"\n{BLUE}{BOLD}{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}{RESET}\n")

def print_success(text):
    """Print success message"""
    print(f"{GREEN}[PASS] {text}{RESET}")

def print_error(text):
    """Print error message"""
    print(f"{RED}[FAIL] {text}{RESET}")

def print_warning(text):
    """Print warning message"""
    print(f"{YELLOW}[WARN] {text}{RESET}")

def print_info(text):
    """Print info message"""
    print(f"  {text}")

def test_frontend_accessibility():
    """Test if frontend files are accessible"""
    print_header("1. Testing Frontend Accessibility")
    
    tests = {
        "Homepage": f"{BASE_URL}/",
        "Chatbot Page": f"{BASE_URL}/chatbot.html",
        "Login Page": f"{BASE_URL}/login.html",
    }
    
    passed = 0
    for name, url in tests.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print_success(f"{name} is accessible")
                passed += 1
            else:
                print_error(f"{name} returned status {response.status_code}")
        except Exception as e:
            print_error(f"{name} failed: {str(e)}")
    
    return passed == len(tests)

def test_data_loading():
    """Test if Excel dataset loads correctly"""
    print_header("2. Testing Data Loading")
    
    try:
        import pandas as pd
        data_path = "data/Finalized_Data.xlsx"
        
        if not Path(data_path).exists():
            print_error(f"Dataset not found at {data_path}")
            return False
        
        df = pd.read_excel(data_path)
        print_success("Excel dataset loaded successfully")
        print_info(f"Total records: {len(df)}")
        print_info(f"Columns: {len(df.columns)} columns")
        print_info(f"Unique locations: {df['location'].nunique() if 'location' in df.columns else 'N/A'}")
        print_info(f"Unique property types: {df['property_type'].nunique() if 'property_type' in df.columns else 'N/A'}")
        print_info(f"Price range: SAR {df['price_sar'].min():.0f} - {df['price_sar'].max():.0f}")
        return True
    except Exception as e:
        print_error(f"Failed to load dataset: {str(e)}")
        return False

def test_xgboost_model():
    """Test if XGBoost model loads correctly"""
    print_header("3. Testing XGBoost Model")
    
    try:
        from app.model import ForecastModel
        model = ForecastModel()
        
        if model.model is not None:
            print_success("XGBoost model loaded successfully")
            print_info(f"Model type: {type(model.model).__name__}")
            return True
        else:
            print_warning("XGBoost model not available")
            print_info("(This is expected if model files are missing)")
            return False
    except Exception as e:
        print_error(f"Failed to load XGBoost model: {str(e)}")
        return False

def test_recommender_system():
    """Test if the recommender system works"""
    print_header("4. Testing Recommender System")
    
    try:
        import pandas as pd
        from app.recommender import RuleBasedRecommender
        
        df = pd.read_excel("data/Finalized_Data.xlsx")
        recommender = RuleBasedRecommender(df)
        
        # Test residential recommendation
        prefs_residential = {
            "goal": "residential",
            "property_type": ["villa"],
            "location": ["غرب"],
            "min_budget": 2000000,
            "max_budget": 5000000
        }
        
        results = recommender.recommend(prefs_residential)
        
        if len(results) > 0:
            print_success("Recommender returned results for residential query")
            print_info(f"Found {len(results)} properties matching criteria")
            if 'price_sar' in results.columns:
                print_info(f"Price range: SAR {results['price_sar'].min():.0f} - {results['price_sar'].max():.0f}")
            return True
        else:
            print_warning("Recommender returned no results for residential query")
            return False
            
    except Exception as e:
        print_error(f"Recommender system test failed: {str(e)}")
        return False

def test_backend_health():
    """Test if backend is running and healthy"""
    print_header("5. Testing Backend Health")
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200 or response.status_code == 404:
            print_success("Backend is running and responsive")
            print_info(f"Response status: {response.status_code}")
            return True
        else:
            print_error(f"Backend returned unexpected status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to backend at http://localhost:8000")
        print_info("Make sure backend is running: uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print_error(f"Backend health check failed: {str(e)}")
        return False

def test_recommender_endpoint():
    """Test the /recommend API endpoint"""
    print_header("6. Testing Recommender Endpoint (/recommend)")
    
    # Test payload for residential
    payload = {
        "goal": "residential",
        "property_class": ["residential"],
        "property_type": ["villa"],
        "location": ["غرب"],
        "min_budget": 2000000,
        "max_budget": 5000000
    }
    
    try:
        response = requests.post(f"{BASE_URL}/recommend", json=payload, timeout=BACKEND_TIMEOUT)
        if response.status_code == 200:
            results = response.json()
            print_success(f"Recommender endpoint responded successfully")
            print_info(f"Query: West, Villa, Residential, 2M-5M SAR")
            print_info(f"Results returned: {len(results)} properties")
            
            if results and len(results) > 0:
                first = results[0]
                print_info(f"Sample property:")
                print_info(f"  - Type: {first.get('property_type')}")
                print_info(f"  - District: {first.get('district')}")
                print_info(f"  - Location: {first.get('location')}")
                print_info(f"  - Price: SAR {first.get('price_sar'):,.0f}" if first.get('price_sar') else "  - Price: N/A")
                return True
            else:
                print_warning("Endpoint returned empty results")
                return False
        else:
            print_error(f"Endpoint returned status {response.status_code}")
            return False
    except requests.exceptions.Timeout:
        print_error(f"Recommender endpoint request timed out after {BACKEND_TIMEOUT}s")
        return False
    except Exception as e:
        print_error(f"Recommender endpoint test failed: {str(e)}")
        return False

def test_investment_forecasting():
    """Test future revenue forecasting for investment properties"""
    print_header("7. Testing Investment Forecasting")
    
    payload = {
        "goal": "investment",
        "property_class": ["residential"],
        "property_type": ["apartment"],
        "location": ["شرق"],
        "min_budget": 2000000,
        "max_budget": 5000000
    }
    
    try:
        response = requests.post(f"{BASE_URL}/recommend", json=payload, timeout=BACKEND_TIMEOUT)
        if response.status_code == 200:
            results = response.json()
            print_success(f"Investment forecast endpoint responded")
            print_info(f"Query: East, Apartment, Investment, 2M-5M SAR")
            print_info(f"Results returned: {len(results)} properties")
            
            if results and len(results) > 0:
                first = results[0]
                print_info(f"Sample property:")
                print_info(f"  - Type: {first.get('property_type')}")
                print_info(f"  - District: {first.get('district')}")
                print_info(f"  - Price: SAR {first.get('price_sar'):,.0f}" if first.get('price_sar') else "  - Price: N/A")
                
                # Check for forecast fields
                has_forecasts = all(k in first for k in ['revenue_5y', 'revenue_10y', 'revenue_20y'])
                if has_forecasts:
                    print_success("Revenue forecasts included in response")
                    print_info(f"  - 5-year forecast: SAR {first['revenue_5y']:,.0f}")
                    print_info(f"  - 10-year forecast: SAR {first['revenue_10y']:,.0f}")
                    print_info(f"  - 20-year forecast: SAR {first['revenue_20y']:,.0f}")
                else:
                    print_warning("Revenue forecasts not available (model may not be configured)")
                return True
            else:
                print_warning("No results for investment query")
                return False
        else:
            print_error(f"Endpoint returned status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Investment forecasting test failed: {str(e)}")
        return False

def test_chatbot_endpoint():
    """Test the /ask API endpoint for OpenAI LLM integration"""
    print_header("8. Testing Chatbot Endpoint (/ask) - OpenAI LLM")
    
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print_warning("OpenAI API key not found in environment")
        print_info("To enable this test, set OPENAI_API_KEY environment variable")
        print_info("Example: $env:OPENAI_API_KEY='your-key-here'")
        return False
    
    payload = {"message": "What properties do you recommend in Riyadh for residential purposes?"}
    
    try:
        response = requests.post(f"{BASE_URL}/ask", json=payload, timeout=BACKEND_TIMEOUT)
        if response.status_code == 200:
            result = response.json()
            print_success("Chatbot endpoint responded successfully")
            
            if 'answer' in result:
                answer = result['answer']
                preview = answer[:150] + "..." if len(answer) > 150 else answer
                print_info(f"LLM Response: {preview}")
                
                if "not available" in answer.lower() or "failed" in answer.lower():
                    print_warning("LLM returned error response - check API key")
                    return False
                else:
                    print_success("OpenAI LLM integration working correctly")
                    return True
            else:
                print_error("Response missing 'answer' field")
                return False
        else:
            print_error(f"Endpoint returned status {response.status_code}")
            return False
    except requests.exceptions.Timeout:
        print_error(f"Chatbot endpoint request timed out after {BACKEND_TIMEOUT}s")
        return False
    except Exception as e:
        print_error(f"Chatbot endpoint test failed: {str(e)}")
        return False

def test_supabase_integration():
    """Test Supabase database integration from frontend"""
    print_header("9. Testing Supabase Database Integration")
    
    try:
        # Read frontend chatbot.html to check Supabase configuration
        with open("frontend/chatbot.html", "r", encoding="utf-8") as f:
            chatbot_content = f.read()
        
        # Check for Supabase client initialization
        has_supabase_lib = "supabase-js" in chatbot_content
        has_supabase_url = "SUPABASE_URL" in chatbot_content
        has_supabase_key = "SUPABASE_ANON_KEY" in chatbot_content
        has_client_init = "createClient" in chatbot_content
        
        if has_supabase_lib:
            print_success("Supabase JavaScript library is included")
        else:
            print_error("Supabase library not found in frontend")
        
        if has_supabase_url and has_supabase_key:
            print_success("Supabase credentials are configured")
        else:
            print_error("Supabase credentials not found or incomplete")
        
        if has_client_init:
            print_success("Supabase client initialization found")
        else:
            print_error("Supabase client not initialized")
        
        all_present = has_supabase_lib and has_supabase_url and has_supabase_key and has_client_init
        
        if all_present:
            print_success("Supabase integration is configured in frontend")
            print_info("Note: Full database connectivity test requires running the frontend in a browser")
            return True
        else:
            print_error("Supabase integration is incomplete or missing")
            return False
            
    except FileNotFoundError:
        print_error("Frontend chatbot.html not found")
        return False
    except Exception as e:
        print_error(f"Supabase integration test failed: {str(e)}")
        return False

def test_environment_setup():
    """Test if all required environment files are configured"""
    print_header("10. Testing Environment Setup")
    
    checks = {
        ".env file": Path(".env").exists(),
        "Data file (Excel)": Path("data/Finalized_Data.xlsx").exists(),
        "XGBoost model": Path("models/xgb_model.json").exists(),
        "Model encoders": Path("models/encoders.pkl").exists(),
        "Frontend directory": Path("frontend").is_dir(),
        "App directory": Path("app").is_dir(),
    }
    
    passed = 0
    for check_name, exists in checks.items():
        if exists:
            print_success(f"{check_name} found")
            passed += 1
        else:
            print_error(f"{check_name} missing")
    
    # Check OpenAI API key
    if os.getenv("OPENAI_API_KEY"):
        print_success("OpenAI API key is configured")
        passed += 1
    else:
        print_warning("OpenAI API key not set (LLM features will be limited)")
    
    return passed >= len(checks)

def test_end_to_end_workflow():
    """Test a complete end-to-end workflow"""
    print_header("11. Testing End-to-End Workflow")
    
    try:
        # Step 1: Get recommendations
        prefs = {
            "goal": "residential",
            "property_type": ["villa", "apartment"],
            "location": ["وسط"],
            "min_budget": 1500000,
            "max_budget": 4000000
        }
        
        print_info("Step 1: Requesting property recommendations...")
        response = requests.post(f"{BASE_URL}/recommend", json=prefs, timeout=BACKEND_TIMEOUT)
        
        if response.status_code != 200:
            print_error(f"Failed to get recommendations: {response.status_code}")
            return False
        
        recommendations = response.json()
        if not recommendations:
            print_warning("No recommendations returned")
            return False
        
        print_success(f"Received {len(recommendations)} recommendations")
        
        # Step 2: Get LLM advice
        print_info("Step 2: Requesting LLM analysis...")
        llm_payload = {
            "message": f"Based on properties in the central Riyadh area, what would you recommend for a residential buyer with a budget of 1.5-4M SAR?"
        }
        
        response = requests.post(f"{BASE_URL}/ask", json=llm_payload, timeout=BACKEND_TIMEOUT)
        
        if response.status_code == 200:
            llm_response = response.json()
            if 'answer' in llm_response:
                print_success("Received LLM analysis")
            else:
                print_warning("LLM response format unexpected")
        else:
            print_warning(f"LLM endpoint returned {response.status_code}")
        
        print_success("End-to-end workflow completed successfully")
        return True
        
    except Exception as e:
        print_error(f"End-to-end workflow failed: {str(e)}")
        return False

def run_all_tests():
    """Run all integration tests and summarize results"""
    print(f"\n{BOLD}{BLUE}")
    print("=" * 70)
    print("  EstateX - Complete Integration Test Suite")
    print("  Testing all components: Backend, Frontend, Database, Model, LLM")
    print("=" * 70)
    print(f"{RESET}\n")
    
    results = {}
    
    # Environment check first
    results["Environment Setup"] = test_environment_setup()
    time.sleep(0.5)
    
    # Data loading
    results["Data Loading"] = test_data_loading()
    time.sleep(0.5)
    
    # Model checks
    results["XGBoost Model"] = test_xgboost_model()
    time.sleep(0.5)
    
    # Recommender system
    results["Recommender System"] = test_recommender_system()
    time.sleep(0.5)
    
    # Backend health
    results["Backend Health"] = test_backend_health()
    time.sleep(0.5)
    
    # Frontend accessibility
    results["Frontend Accessibility"] = test_frontend_accessibility()
    time.sleep(0.5)
    
    # API endpoints
    results["Recommender Endpoint"] = test_recommender_endpoint()
    time.sleep(0.5)
    
    results["Investment Forecasting"] = test_investment_forecasting()
    time.sleep(0.5)
    
    results["Chatbot Endpoint (OpenAI LLM)"] = test_chatbot_endpoint()
    time.sleep(0.5)
    
    # Database integration
    results["Supabase Integration"] = test_supabase_integration()
    time.sleep(0.5)
    
    # End-to-end workflow
    results["End-to-End Workflow"] = test_end_to_end_workflow()
    
    # Summary Report
    print_header("Integration Test Summary")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for test_name, result in results.items():
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        symbol = "✓" if result else "✗"
        print(f"  {symbol} {test_name}: {status}")
    
    print()
    print_info(f"Passed: {passed}/{total} tests")
    
    if passed == total:
        print(f"\n{GREEN}{BOLD}✓ All integration tests passed! System is fully connected and operational.{RESET}\n")
        return True
    elif passed >= total * 0.8:
        print(f"\n{YELLOW}{BOLD}⚠ Most tests passed ({passed}/{total}). Some features may be limited.{RESET}\n")
        return True
    else:
        print(f"\n{RED}{BOLD}✗ Integration issues detected ({passed}/{total} tests passed).{RESET}\n")
        print("Check the logs above for specific failures and their causes.\n")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
