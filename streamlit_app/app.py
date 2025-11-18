# streamlit_app/app.py
import streamlit as st
import requests

API_URL = "http://localhost:8000/recommend"

st.title("Real Estate Intelligence Platform")

st.subheader("Enter your preferences")

min_budget = st.number_input("Minimum Budget (SAR)", 0)
max_budget = st.number_input("Maximum Budget (SAR)", 10000000)

property_type = st.multiselect("Property Type", ["قطعة أرض", "عمارة", "فيلا", "شقة"])
property_class = st.multiselect("Property Class", ["سكني", "تجاري"])
district = st.text_input("District (comma separated)")
location = st.multiselect("Location", ["شرق", "غرب", "شمال", "جنوب", "وسط"])
goal = st.selectbox("Goal", ["investment", "residential", "none"])

if st.button("Search"):
    prefs = {
        "min_budget": min_budget,
        "max_budget": max_budget,
        "property_type": property_type,
        "property_class": property_class,
        "district": [d.strip() for d in district.split(",")] if district else [],
        "location": location,
        "goal": goal
    }

    with st.spinner("Searching..."):
        response = requests.post(API_URL, json=prefs)

    if response.status_code == 200:
        results = response.json()
        st.success(f"Found {len(results)} matching properties")
        st.dataframe(results)
    else:
        st.error("Error: could not fetch results from API")



st.title("Real Estate AI Assistant")

question = st.text_input("Ask something:")

if st.button("Submit"):
    response = requests.post("http://localhost:8000/ask", json={"message": question})
    st.write(response.json()["answer"])
