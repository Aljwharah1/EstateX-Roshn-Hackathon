# app/recommender.py
import pandas as pd

class RuleBasedRecommender:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.df['price_sar'] = pd.to_numeric(self.df['price_sar'], errors='coerce')
        self.df['area_sqm'] = pd.to_numeric(self.df['area_sqm'], errors='coerce')
        self.df['price_per_sqm'] = pd.to_numeric(self.df['price_per_sqm'], errors='coerce')

    def recommend(self, prefs: dict):

        results = self.df.copy()

        # ---- Budget ----
        if "min_budget" in prefs:
            results = results[results["price_sar"] >= prefs["min_budget"]]

        if "max_budget" in prefs:
            results = results[results["price_sar"] <= prefs["max_budget"]]

        # ---- Property Type ----
        if "property_type" in prefs and prefs["property_type"]:
            results = results[results["property_type"].isin(prefs["property_type"])]

        # ---- Property Class ----
        if "property_class" in prefs and prefs["property_class"]:
            results = results[results["property_class"].isin(prefs["property_class"])]

        # ---- District ----
        if "district" in prefs and prefs["district"]:
            results = results[results["district"].isin(prefs["district"])]

        # ---- Location (شرق، غرب، شمال، جنوب، وسط) ----
        if "location" in prefs and prefs["location"]:
            results = results[results["location"].isin(prefs["location"])]

        # ---- Goal Handling ----
        goal = prefs.get("goal", "")

        if goal == "investment":
            # Lower price_per_sqm → cheaper entry cost
            results["score"] = -results["price_per_sqm"]

        elif goal == "residential":
            # Larger area → preferable
            results["score"] = results["area_sqm"]

        else:
            results["score"] = 0

        return results.sort_values(by="score", ascending=False).reset_index(drop=True)