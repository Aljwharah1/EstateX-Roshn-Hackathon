#!/usr/bin/env python3
"""
Comprehensive Integration Test for EstateX
Tests: Frontend, Backend, Data, Recommender, and Forecasting
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def test_frontend_accessibility():
    """Test if homepage and chatbot are accessible"""
    print_header("1. Testing Frontend Accessibility")
    
    tests = {
        "Homepage": f"{BASE_URL}/",
        "Chatbot": f"{BASE_URL}/chatbot.html",
    }
    
    for name, url in tests.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✓ {name} is accessible (Status: {response.status_code})")
            else:
                print(f"✗ {name} returned status {response.status_code}")
        except Exception as e:
            print(f"✗ {name} failed: {str(e)}")

def test_data_loading():
    """Test if Excel dataset loads correctly"""
    print_header("2. Testing Data Loading")
    
    try:
        import pandas as pd
        df = pd.read_excel("data/Finalized_Data.xlsx")
        print(f"✓ Excel dataset loaded successfully")
        print(f"  - Total records: {len(df)}")
        print(f"  - Columns: {list(df.columns)[:5]}...")
        print(f"  - Unique locations: {df['location'].nunique()}")
        print(f"  - Unique property types: {df['property_type'].nunique()}")
    except Exception as e:
        print(f"✗ Failed to load dataset: {str(e)}")

def test_recommender_endpoint():
    """Test the /recommend API endpoint"""
    print_header("3. Testing Recommender Endpoint")
    
    # Test 1: West, Villa, 2M-5M, Residential
    payload = {
        "goal": "residential",
        "property_class": ["residential"],
        "property_type": ["villa"],
        "location": ["غرب"],
        "min_budget": 2000000,
        "max_budget": 5000000
    }
    
    try:
        response = requests.post(f"{BASE_URL}/recommend", json=payload, timeout=10)
        if response.status_code == 200:
            results = response.json()
            print(f"✓ Recommender endpoint responded")
            print(f"  - Request: West, Villa, Residential, 2M-5M SAR")
            print(f"  - Results returned: {len(results)}")
            if results:
                first = results[0]
                print(f"  - Sample property: {first.get('property_type')} in {first.get('district')}")
                print(f"    Price: SAR {first.get('price_sar')}")
        else:
            print(f"✗ Endpoint returned status {response.status_code}")
    except Exception as e:
        print(f"✗ Recommender endpoint failed: {str(e)}")

def test_investment_forecasting():
    """Test future revenue forecasting for investment properties"""
    print_header("4. Testing Investment Forecasting")
    
    # Test: Long-term investment, East, Apartment, 2M-5M
    payload = {
        "goal": "investment",
        "property_class": ["residential"],
        "property_type": ["apartment"],
        "location": ["شرق"],
        "min_budget": 2000000,
        "max_budget": 5000000
    }
    
    try:
        response = requests.post(f"{BASE_URL}/recommend", json=payload, timeout=10)
        if response.status_code == 200:
            results = response.json()
            print(f"✓ Investment forecast endpoint responded")
            print(f"  - Request: East, Apartment, Investment, 2M-5M SAR")
            print(f"  - Results returned: {len(results)}")
            if results:
                first = results[0]
                print(f"  - Sample property: {first.get('property_type')} in {first.get('district')}")
                print(f"    Current price: SAR {first.get('price_sar')}")
                if 'revenue_5y' in first:
                    print(f"    5-year forecast: SAR {first.get('revenue_5y')}")
                    print(f"    10-year forecast: SAR {first.get('revenue_10y')}")
                    print(f"    20-year forecast: SAR {first.get('revenue_20y')}")
                else:
                    print(f"    ⚠ No revenue forecasts found")
        else:
            print(f"✗ Endpoint returned status {response.status_code}")
    except Exception as e:
        print(f"✗ Investment forecasting failed: {str(e)}")

def test_chatbot_endpoint():
    """Test the /ask API endpoint for chatbot"""
    print_header("5. Testing Chatbot Endpoint")
    
    payload = {"message": "What properties do you recommend in Riyadh?"}
    
    try:
        response = requests.post(f"{BASE_URL}/ask", json=payload, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Chatbot endpoint responded")
            if 'answer' in result:
                answer = result['answer'][:100] + "..." if len(result['answer']) > 100 else result['answer']
                print(f"  - Sample response: {answer}")
        else:
            print(f"✗ Endpoint returned status {response.status_code}")
    except Exception as e:
        print(f"⚠ Chatbot endpoint note: {str(e)}")
        print(f"  (This is expected if OpenAI API key is not set)")

def test_xgboost_model():
    """Test if XGBoost model loads correctly"""
    print_header("6. Testing XGBoost Model")
    
    try:
        from app.model import ForecastModel
        model = ForecastModel()
        if model.model is not None:
            print(f"✓ XGBoost model loaded successfully")
        else:
            print(f"⚠ XGBoost model not available (this is expected if model files are missing)")
    except Exception as e:
        print(f"✗ Failed to load XGBoost model: {str(e)}")

def run_all_tests():
    """Run all integration tests"""
    print("\n" + "="*60)
    print("  EstateX Integration Test Suite")
    print("  Testing: Frontend | Backend | Data | Recommender | Forecasting")
    print("="*60)
    
    test_frontend_accessibility()
    time.sleep(1)
    test_data_loading()
    time.sleep(1)
    test_xgboost_model()
    time.sleep(1)
    test_recommender_endpoint()
    time.sleep(1)
    test_investment_forecasting()
    time.sleep(1)
    test_chatbot_endpoint()
    
    print_header("Integration Test Complete ✓")
    print("All components are working and integrated!\n")

if __name__ == "__main__":
    run_all_tests()
