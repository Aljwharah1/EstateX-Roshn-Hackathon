# 🏡 Real-Estate Analytics MVP  
**Machine Learning • Recommendations • Internal LLM • FastAPI • HTML/CSS/JS**

This project is a complete real-estate analytics MVP combining:

- **XGBoost machine learning**
- **Rule-based recommender system**
- **An internal AI assistant (OpenAI API) restricted ONLY to internal project resources**
- **FastAPI backend**
- **HTML/CSS/JS frontend**

Users can:

- 🔢 Predict **price per square meter (SAR/sqm)**
- 🧭 Receive personalized **property recommendations**
- 🤖 Ask questions to an internal **AI assistant grounded in the dataset + XGBoost + recommender**
- 🌐 Interact through a lightweight web interface
- 🚀 Access the platform online after deployment

---

## 📁 Project Structure

project/
│
├── backend/
│ ├── app/
│ │ ├── main.py # FastAPI entry point
│ │ ├── model.py # XGBoost loading + prediction
│ │ ├── recommender.py # Rule-based recommender engine
│ │ ├── llm_agent.py # Internal LLM using OpenAI API
│ │
│ ├── models/
│ │ ├── xgb_model.json # Trained XGBoost model
│ │ ├── encoders.pkl # Label encoders
│ │
│ ├── data/
│ │ └── Finalized_Data.xlsx # Project dataset
│ │
│ └── training/
│ └── train_xgboost.py # Model training script
│
├── frontend/
│ ├── index.html # Main UI
│ ├── styles.css # Frontend styling
│ └── script.js # JS requests to FastAPI backend
│
└── README.md


---

## 📊 Dataset Description

The dataset includes the following columns:

- region  
- city  
- district  
- location (e.g., south, west, northeast)  
- property_type  
- property_class  
- area_sqm  
- price_sar  
- price_per_sqm  
- year  
- quarter  

---

## 🤖 Machine Learning Model (XGBoost)

The model predicts:

> **Price per square meter (SAR/sqm)**

The training script performs:

- Dataset cleaning  
- Arabic categorical encoding  
- Train/test splitting  
- XGBoost model training  
- Evaluation (MAE, RMSE, R²)  
- Saving the model + encoders  

Train the model using:

```bash
python backend/training/train_xgboost.py

🧭 Recommender System

A rule-based recommendation engine that matches users with properties based on:

Budget

Area preferences

Property type

Location characteristics

🤖 Internal LLM (OpenAI API)

A constrained assistant that has access ONLY to:

The dataset

XGBoost predictions

Recommender rules

It cannot use external data or internet information.

🌐 Frontend (HTML/CSS/JS)

The frontend provides:

A prediction form

Recommendation view

Chat interface for the LLM agent

🚀 Running the Project Locally
1️⃣ Install dependencies

pip install -r requirements.txt

2️⃣ Start FastAPI backend
uvicorn backend.app.main:app --reload

3️⃣ Open the frontend

Open the file:

frontend/index.html


Or serve it via a static server.

🧪 Training the Model

Run:

python backend/training/train_xgboost.py


This generates:

backend/models/xgb_model.json

backend/models/encoders.pkl


🌍 Deployment

You can deploy to:

Render

Railway

Deta Space

Azure App Service

Docker container

GitHub Pages (frontend only)

