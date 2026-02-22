# app/main.py
"""EstateX Backend API"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import os

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

