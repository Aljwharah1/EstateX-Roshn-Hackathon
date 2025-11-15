import pandas as pd

class RuleBasedRecommender:
    def __init__(self, data_path: str):
        self.df = pd.read_excel(data_path)

    def recommend(self, prefs: dict):
        df = self.df.copy()

        # ----- 1. Budget -----
        if "min_budget" in prefs:
            df = df[df["price_sar"] >= prefs["min_budget"]]

        if "max_budget" in prefs:
            df = df[df["price_sar"] <= prefs["max_budget"]]

        # ----- 2. Region -----
        if "region" in prefs:
            df = df[df["region"].isin(prefs["region"])]

        # ----- 3. City -----
        if "city" in prefs:
            df = df[df["city"].isin(prefs["city"])]

        # ----- 4. District -----
        if "district" in prefs:
            df = df[df["district"].isin(prefs["district"])]

        # ----- 5. Property Class -----
        if "property_class" in prefs:
            df = df[df["property_class"].isin(prefs["property_class"])]

        # ----- 6. Property Type -----
        if "property_type" in prefs:
            df = df[df["property_type"].isin(prefs["property_type"])]

        # ----- 7. Area Filters -----
        if "min_area" in prefs:
            df = df[df["area_sqm"] >= prefs["min_area"]]

        if "max_area" in prefs:
            df = df[df["area_sqm"] <= prefs["max_area"]]

        # ----- 8. Price per sqm filters -----
        if "min_ppm" in prefs:  # ppm = price per sqm
            df = df[df["price_per_sqm"] >= prefs["min_ppm"]]

        if "max_ppm" in prefs:
            df = df[df["price_per_sqm"] <= prefs["max_ppm"]]

        # ========== 9. GOAL-BASEd RANKING ==========
        # Investment Goal → choose low price per sqm + large area
        if prefs.get("goal") == "investment":
            df["score"] = (
                -df["price_per_sqm"] * 0.6 +
                df["area_sqm"] * 0.4
            )
            df = df.sort_values("score", ascending=False)

        # Residential Goal → choose affordable yet larger area
        elif prefs.get("goal") == "residential":
            df["score"] = (
                -(df["price_sar"]) * 0.5 +
                df["area_sqm"] * 0.5
            )
            df = df.sort_values("score", ascending=False)

        # Default sorting if no goal is given
        else:
            df = df.sort_values("price_sar")

        return df.reset_index(drop=True)