"""
Debug script for testing the recommendation engine with Supabase data.
"""
import os
from dotenv import load_dotenv
from supabase import create_client
from app.recommender import RuleBasedRecommender

load_dotenv()

# Initialize Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    print("[ERROR] SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")
    exit(1)

sb = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Fetch properties and transactions from Supabase
print("[INFO] Fetching properties from Supabase...")
props_result = sb.table('properties').select('*').execute()
properties = props_result.data or []
print(f"[INFO] Found {len(properties)} properties")

# Enrich properties with transaction data
print("[INFO] Enriching properties with transaction data...")
for prop in properties:
    trans_result = sb.table('transactions').select('*').eq('property_id', prop['property_id']).order('date', desc=True).limit(5).execute()
    prop['transactions'] = trans_result.data or []

# Create recommender and define preferences
recommender = RuleBasedRecommender()

# Test case 1: North apartments
print("\n=== Test Case 1: North Apartments (any budget) ===")
prefs1 = {
    "location": ["شمال"],
    "property_type": "apartment",
    "goal": "investment"
}
results1 = recommender.recommend(properties, prefs1)
print(f"North apartments found: {len(results1)}")
if results1:
    for i, prop in enumerate(results1[:3]):
        trans = prop.get('transactions', [{}])[0]
        print(f"  {i+1}. {prop['property_id']} - Price: {trans.get('price_sar')}, Area: {trans.get('area_sqm')}")

# Test case 2: Properties in specific district with budget
print("\n=== Test Case 2: Properties in District with Budget Limit ===")
prefs2 = {
    "district": ["الرياض"],
    "min_budget": 100000,
    "max_budget": 1000000,
    "goal": "residential"
}
results2 = recommender.recommend(properties, prefs2)
print(f"Results found: {len(results2)}")
if results2:
    for i, prop in enumerate(results2[:3]):
        trans = prop.get('transactions', [{}])[0]
        print(f"  {i+1}. {prop['property_id']} - Price: {trans.get('price_sar')}, Area: {trans.get('area_sqm')}")

print("\n[INFO] Debug script completed")


