# app/main.py
"""EstateX Backend API"""
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file in project root
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)

# ============ Supabase Client Setup ============
try:
    from supabase import create_client, Client
    
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
    
    print(f"[DEBUG] SUPABASE_URL from env: {SUPABASE_URL}")
    print(f"[DEBUG] SUPABASE_SERVICE_KEY exists: {bool(SUPABASE_SERVICE_KEY)}")
    
    if SUPABASE_URL and SUPABASE_SERVICE_KEY:
        sb = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        print("[INFO] ✓ Supabase client initialized with service role")
    else:
        sb = None
        print("[WARNING] ✗ SUPABASE_URL or SUPABASE_SERVICE_KEY not configured")
except Exception as e:
    sb = None
    print(f"[ERROR] Failed to initialize Supabase: {e}")
    print("[WARNING] supabase-py not installed - database operations will be limited")

app = FastAPI(title="EstateX - Real Estate AI Advisor")

# ============ CORS Configuration ============
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ Static Files ============
# Mount frontend directory to serve images, CSS, JS, etc.
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")
else:
    print(f"[WARNING] Frontend directory not found at {frontend_path}")

# ============ Pydantic Models ============
class UserPrefs(BaseModel):
    min_budget: Optional[float] = None
    max_budget: Optional[float] = None
    property_type: Optional[List[str]] = None
    property_class: Optional[List[str]] = None
    district: Optional[List[str]] = None
    location: Optional[List[str]] = None
    goal: Optional[str] = None

class UserUpdate(BaseModel):
    """Update user profile"""
    user_id: str
    role: Optional[str] = None
    preferred_language: Optional[str] = None
    household_size: Optional[int] = None
    life_stage: Optional[str] = None
    risk_tolerance: Optional[str] = None

class PreferencesUpdate(BaseModel):
    """Update user preferences"""
    user_id: str
    city: Optional[str] = None
    districts_included: Optional[List[str]] = None
    districts_excluded: Optional[List[str]] = None
    max_commute_minutes: Optional[int] = None
    property_type: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    area_min: Optional[float] = None
    area_max: Optional[float] = None

class FinancialUpdate(BaseModel):
    """Update financial profile"""
    user_id: str
    monthly_payment_ceiling: Optional[float] = None
    down_payment_budget: Optional[float] = None
    financing: Optional[str] = None
    preapproval_status: Optional[bool] = None
    investment_horizon_months: Optional[int] = None


# ============ Routes ============

@app.get("/")
def root():
    """Serve home page"""
    return FileResponse("frontend/home.html")

@app.get("/home.html")
def home():
    """Serve home page"""
    return FileResponse("frontend/home.html")

@app.get("/chatbot.html")
def chatbot_page():
    """Serve chatbot page"""
    return FileResponse("frontend/chatbot.html")

@app.get("/login.html")
def login_page():
    """Serve login page"""
    return FileResponse("frontend/login.html")

# ============ User Management Endpoints ============
@app.post("/api/user")
async def update_user(user_data: UserUpdate):
    """Update user profile (uses backend service role to bypass RLS)"""
    try:
        if not sb:
            return {
                "success": True,
                "message": "User update accepted (Supabase not configured)",
                "data": user_data.dict()
            }
        
        user_id = user_data.user_id
        update_payload = {k: v for k, v in user_data.dict().items() if v is not None and k != 'user_id'}
        update_payload['last_active_at'] = datetime.utcnow().isoformat()
        
        # Try to update existing user
        result = sb.table('users').update(update_payload).eq('user_id', user_id).execute()
        
        if result.data:
            print(f"Updated user {user_id}: {update_payload}")
            return {
                "success": True,
                "message": "User updated successfully",
                "data": result.data
            }
        
        # If no rows updated, insert new user
        insert_payload = {'user_id': user_id, **update_payload}
        result = sb.table('users').insert(insert_payload).execute()
        print(f"Inserted user {user_id}: {insert_payload}")
        
        return {
            "success": True,
            "message": "User created successfully",
            "data": result.data
        }
    except Exception as e:
        print(f"Error updating user: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/preferences")
async def update_preferences(prefs_data: PreferencesUpdate):
    """Update user preferences"""
    try:
        if not sb:
            return {
                "success": True,
                "message": "Preferences update accepted (Supabase not configured)",
                "data": prefs_data.dict()
            }
        
        user_id = prefs_data.user_id
        update_payload = {k: v for k, v in prefs_data.dict().items() if v is not None and k != 'user_id'}
        update_payload['updated_at'] = datetime.utcnow().isoformat()
        
        # Check if preferences exist
        existing = sb.table('user_preferences').select('preference_id').eq('user_id', user_id).order('updated_at', desc=True).limit(1).execute()
        
        if existing.data and len(existing.data) > 0:
            # Update existing
            result = sb.table('user_preferences').update(update_payload).eq('preference_id', existing.data[0]['preference_id']).execute()
            print(f"Updated preferences for user {user_id}")
        else:
            # Insert new
            insert_payload = {'user_id': user_id, **update_payload}
            result = sb.table('user_preferences').insert(insert_payload).execute()
            print(f"Inserted preferences for user {user_id}")
        
        return {
            "success": True,
            "message": "Preferences updated successfully",
            "data": result.data
        }
    except Exception as e:
        print(f"Error updating preferences: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/financial")
async def update_financial(fin_data: FinancialUpdate):
    """Update financial profile"""
    try:
        if not sb:
            return {
                "success": True,
                "message": "Financial profile update accepted (Supabase not configured)",
                "data": fin_data.dict()
            }
        
        user_id = fin_data.user_id
        update_payload = {k: v for k, v in fin_data.dict().items() if v is not None and k != 'user_id'}
        update_payload['updated_at'] = datetime.utcnow().isoformat()
        
        # Check if financial profile exists
        existing = sb.table('financial_profiles').select('financial_profile_id').eq('user_id', user_id).order('updated_at', desc=True).limit(1).execute()
        
        if existing.data and len(existing.data) > 0:
            # Update existing
            result = sb.table('financial_profiles').update(update_payload).eq('financial_profile_id', existing.data[0]['financial_profile_id']).execute()
            print(f"Updated financial profile for user {user_id}")
        else:
            # Insert new
            insert_payload = {'user_id': user_id, **update_payload}
            result = sb.table('financial_profiles').insert(insert_payload).execute()
            print(f"Inserted financial profile for user {user_id}")
        
        return {
            "success": True,
            "message": "Financial profile updated successfully",
            "data": result.data
        }
    except Exception as e:
        print(f"Error updating financial profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recommend")
def recommend_properties(prefs: UserPrefs):
    """Get property recommendations based on user preferences"""
    try:
        # For now, return empty list since data file is missing
        # In production, this will filter against the database
        return []
    except Exception as e:
        return {"error": str(e)}

@app.post("/ask")
def ask_ai(payload: dict):
    """Chat with AI advisor"""
    user_message = payload.get("message", "")
    
    # Return a demo response  
    return {
        "answer": f"Thanks for your interest in EstateX! You asked: '{user_message}'. In production, this would provide intelligent AI-powered real estate advice from GPT-4."
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "OK", "service": "EstateX API"}
