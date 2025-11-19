# EstateX Advisor -Roshn-Hackathon
🏡 Real Estate Analytics Platform
Price Prediction • Recommender System • FastAPI • HTML/CSS Frontend • XGBoost • OpenAI LLM

This project is a complete real-estate analytics MVP combining machine learning, rules-based recommendations, and a lightweight AI assistant that only uses internal project resources (dataset + XGBoost + recommender). Users can:

Predict price per square meter (SAR/sqm)

Receive personalized property recommendations

Ask questions to an AI assistant grounded ONLY in your dataset and models

Interact through a simple HTML/CSS/JS frontend

Access the platform online after deployment

📂 Project Structure
project/
├── backend/
│   ├── app/
│   │   ├── main.py               # FastAPI entry point
│   │   ├── model.py              # XGBoost loading + prediction
│   │   ├── recommender.py        # Rule-based recommender
│   │   └── llm_agent.py          # LLM constrained to project data
│   ├── models/
│   │   ├── xgb_model.json        # Saved XGBoost model
│   │   └── encoders.pkl          # LabelEncoders
│   ├── data/
│   │   └── Finalized_Data.xlsx   # Dataset
│   └── training/
│       └── train_xgboost.py      # Model training script
│
├── frontend/
│   ├── index.html                # Main UI
│   ├── styles.css                # Frontend styling
│   └── script.js                 # API calls to FastAPI
│
└── README.md

📊 Dataset Description

The dataset includes the following columns:

region

city

district

location (north, south, west…)

property_type

property_class

area_sqm

year

quarter

price_sar

price_per_sqm

These features are used for:

XGBoost model input

Recommender system filtering

LLM contextual knowledge

🤖 Machine Learning Model (XGBoost)
🎯 Target

price_per_sqm (SAR per square meter)

🧪 Training Script

Located in:

backend/training/train_xgboost.py


It includes:

Data cleaning

Label encoding

Train/test splitting

Model training

Performance metrics (MAE, RMSE, R²)

Saving model + encoders

📈 Latest Performance
R²   = 0.606
MAE  = 900.74 SAR per sqm
RMSE = 2,050.29 SAR per sqm


This means the model explains ~60% of price variance and predicts with ±900 SAR/sqm typical error.

🔍 Recommender System

The recommender filters and scores properties based on:

District

Price range

Property class

Area

User goal

Encoded categorical similarity

Works for all properties, budgets, and goals.

🧠 OpenAI LLM Integration (Internal Use Only)

The LLM:

Uses your dataset, XGBoost model, and recommender system as its ONLY knowledge sources

Cannot fetch outside information

Provides contextual explanations, summaries, and answers

API Key

Create an environment variable:

OPENAI_API_KEY=your_api_key_here

🚀 FastAPI Backend
Run locally:
cd backend
uvicorn app.main:app --reload

API Documentation:
http://127.0.0.1:8000/docs

📡 API Endpoints
1️⃣ Prediction (XGBoost)

POST /predict

Example Input:

{
  "region": "منطقة الرياض",
  "city": "الرياض",
  "district": "حطين",
  "location": "north",
  "property_type": "شقة",
  "property_class": "سكني",
  "area_sqm": 120,
  "year": 2022
}

2️⃣ Recommender

POST /recommend

Example Input:

{
  "min_budget": 500000,
  "max_budget": 1500000,
  "district": ["السلام"],
  "property_class": ["تجاري"],
  "goal": "investment"
}

3️⃣ LLM Assistant

POST /ask-agent

Example Input:

{
  "query": "What is the price trend in حطين?"
}

🎨 Frontend (HTML/CSS/JS)

Your frontend contains:

index.html (form inputs + prediction results)

styles.css (styling)

script.js (API calls)

To run:

Open index.html in your browser


For production, host it on Vercel or GitHub Pages.

🌐 Deployment Instructions
🖥️ Deploy Backend (FastAPI) on Render

Push backend/ to GitHub

Go to Render.com → New Web Service

Connect GitHub repo

Setup:

Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port 10000


Add ENV:

OPENAI_API_KEY=your_key_here


Deploy and copy backend URL:

https://your-backend.onrender.com

🌍 Deploy Frontend on Vercel

Push frontend/ to GitHub

Go to Vercel.com → New Project

Deploy

Update script.js:

const BASE_URL = "https://your-backend.onrender.com";

🔧 CORS Configuration (Required)

Add to main.py:

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

🧪 Local Testing
Run backend:
uvicorn app.main:app --reload

Train model:
python backend/training/train_xgboost.py