<p align="left">
  <img src="./frontend/logo.png" alt="Real Estate Logo" width="100" style="float:left; margin-right:10px;"/>
  <h1 style="display:inline;">🏡 EstateX Advisor MVP</h1>
</p>
**Machine Learning • Recommendations • Internal LLM • FastAPI • HTML/CSS/JS**

---

## 🚩 Problem  

In the real estate market, making informed property decisions requires accurate price predictions and personalized recommendations.  
Often, buyers and investors struggle to:  
- Get reliable price estimates for properties  
- Find properties that match their specific needs and budget  
- Access expert guidance without consulting multiple sources  

Traditional approaches lack scalability, consistency, and the ability to provide instant, data-driven insights.  

**Real-Estate Analytics MVP** was built to address these challenges by providing an all-in-one platform that combines machine learning, intelligent recommendations, and an AI assistant.  

---

## 💡 Solution  

**Real-Estate Analytics MVP** automates real estate analysis using AI and machine learning — from price prediction to personalized recommendations.  

**How it works:**  
1. **Price Prediction:** Uses XGBoost machine learning to predict price per square meter (SAR/sqm) based on property features.  
2. **Smart Recommendations:** Rule-based recommender system matches users with properties based on budget, area, type, and location.  
3. **AI Assistant:** Internal LLM (OpenAI API) answers questions using ONLY the project dataset, model predictions, and recommender rules.  
4. **Interactive Interface:** Simple web UI for predictions, recommendations, and chat with the AI assistant.  
5. **Deployment Ready:** Can be deployed online for public access.  

---

## 🗂️ Project Structure 

```bash
project/
│
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI entry point
│   │   ├── model.py                 # XGBoost loading + prediction
│   │   ├── recommender.py           # Rule-based recommender engine
│   │   └── llm_agent.py             # Internal LLM using OpenAI API
│   │
│   ├── models/
│   │   ├── xgb_model.json           # Trained XGBoost model
│   │   └── encoders.pkl             # Label encoders
│   │
│   ├── data/
│   │   └── Finalized_Data.xlsx      # Project dataset
│   │
│   └── training/
│       └── train_xgboost.py         # Model training script
│
├── frontend/
│   ├── index.html                   # Main UI
│   ├── styles.css                   # Frontend styling
│   └── script.js                    # JS requests to FastAPI backend
│
├── requirements.txt                 # Python dependencies
└── README.md                        # Project documentation
```

---

## 📊 Dataset Description

The dataset includes the following columns:

| Column           | Description                                    |
|------------------|------------------------------------------------|
| region           | Geographic region of the property              |
| city             | City where property is located                 |
| district         | Specific district within the city              |
| location         | Location direction (e.g., south, west, northeast) |
| property_type    | Type of property (residential, commercial, etc.) |
| property_class   | Classification of property                     |
| area_sqm         | Property area in square meters                 |
| price_sar        | Property price in Saudi Riyals                 |
| price_per_sqm    | Price per square meter (SAR/sqm)               |
| year             | Year of the property listing                   |
| quarter          | Quarter of the year                            |

---

## 🤖 Machine Learning Model (XGBoost)

The model predicts:

> **Price per square meter (SAR/sqm)**

The training pipeline includes:

- Dataset cleaning and preprocessing  
- Arabic categorical encoding  
- Train/test splitting  
- XGBoost model training and optimization  
- Performance evaluation (MAE, RMSE, R²)  
- Model and encoder serialization  

**Train the model:**
```bash
python backend/training/train_xgboost.py
```

**Output:**
- `backend/models/xgb_model.json`
- `backend/models/encoders.pkl`

---

## 🧭 Recommender System

A rule-based recommendation engine that intelligently matches users with properties based on:

- **Budget constraints**  
- **Area preferences (sqm)**  
- **Property type requirements**  
- **Location characteristics**  

The recommender uses filtering and scoring algorithms to provide personalized property suggestions.

---

## 🤖 Internal LLM (OpenAI API)

A constrained AI assistant with access ONLY to:

✅ **The project dataset**  
✅ **XGBoost model predictions**  
✅ **Recommender system rules**  

❌ **Cannot access external data or internet information**  

This ensures responses are grounded in the project's internal resources, maintaining accuracy and relevance.

---

## 🌐 Frontend (HTML/CSS/JS)

The frontend provides a clean, intuitive interface with:

- 🔢 **Prediction Form** — Input property features to get price estimates  
- 🏠 **Recommendation View** — Browse personalized property suggestions  
- 💬 **Chat Interface** — Ask questions to the AI assistant  
- 🎨 **Responsive Design** — Works seamlessly on desktop and mobile  

---

## 🚀 Getting Started

You can run **Real-Estate Analytics MVP** locally by following these steps:

---

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 2️⃣ Start FastAPI Backend

```bash
uvicorn backend.app.main:app --reload
```

> The API will be available at http://localhost:8000

---

### 3️⃣ Open Frontend

**Option A:** Open directly in browser:
```bash
open frontend/index.html
```

**Option B:** Serve via HTTP server:
```bash
cd frontend
python -m http.server 8080
```

> Then open http://localhost:8080 in your browser.

---

### 🧠 Note
- Configure OpenAI API key in your environment variables  
- Ensure the dataset file is present in `backend/data/`  
- Train the model before first use  

---

## 🧪 Training the Model

Run the training script to generate the XGBoost model:

```bash
python backend/training/train_xgboost.py
```

**This generates:**
- `backend/models/xgb_model.json` — Trained XGBoost model  
- `backend/models/encoders.pkl` — Label encoders for categorical features  

---

## 🌍 Deployment Options

You can deploy this project to various platforms:

- **Render** — Easy FastAPI deployment  
- **Railway** — One-click deployment  
- **Deta Space** — Free tier available  
- **Azure App Service** — Enterprise-grade hosting  
- **Docker Container** — Containerized deployment  
- **GitHub Pages** — Frontend-only hosting  

**For full deployment:**
1. Deploy backend (FastAPI) to a platform like Render  
2. Update frontend API endpoints to point to deployed backend  
3. Host frontend on GitHub Pages or serve from backend static files  

---

## 🎯 Features Summary

| Feature                    | Technology              |
|----------------------------|-------------------------|
| Price Prediction           | XGBoost ML Model        |
| Property Recommendations   | Rule-based Engine       |
| AI Assistant               | OpenAI API (Internal)   |
| Backend API                | FastAPI                 |
| Frontend                   | HTML/CSS/JavaScript     |
| Model Training             | Scikit-learn, XGBoost   |
| Data Processing            | Pandas, NumPy           |

---

## 📈 Model Performance

The XGBoost model is evaluated using:

- **MAE (Mean Absolute Error)** — Average prediction error  
- **RMSE (Root Mean Squared Error)** — Standard deviation of errors  
- **R² Score** — Proportion of variance explained by the model  

*(Add your actual performance metrics after training)*

---

## 🔧 Configuration

Key configuration files:

- **`requirements.txt`** — Python dependencies  
- **`backend/app/main.py`** — API routes and configuration  
- **Environment Variables:**
  - `OPENAI_API_KEY` — Required for LLM agent  
  - Database credentials (if using external DB)  

---

## 📝 API Endpoints

| Endpoint                   | Method | Description                          |
|----------------------------|--------|--------------------------------------|
| `/predict`                 | POST   | Get price prediction                 |
| `/recommend`               | POST   | Get property recommendations         |
| `/chat`                    | POST   | Chat with AI assistant               |
| `/health`                  | GET    | Check API health status              |

---

## 🤝 Contributing

This is an MVP project. Future enhancements could include:

- Deep learning models for better predictions  
- Collaborative filtering for recommendations  
- Real-time data updates  
- Mobile application  
- Advanced visualizations and analytics  

---

## 📧 Contact

For questions or feedback about this project, please reach out through the appropriate channels.

---

**Built with ❤️ using Machine Learning, FastAPI, and AI**

