# app/recommender.py
"""
Recommendation engine that works with Supabase data.
Performs client-side filtering and scoring on property lists from Supabase.
All data should come from Supabase tables: properties, transactions, user_preferences.
"""

def _to_float(value, default=None):
    """Safely convert value to float."""
    if value is None:
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


class RuleBasedRecommender:
    """
    Filters and scores properties based on user preferences.
    Input: List of properties with transaction data from Supabase.
    Output: Ranked list of recommended properties.
    """
    
    def __init__(self):
        """Initialize recommender (no data loading needed - uses Supabase directly)."""
        pass

    def recommend(self, properties: list, prefs: dict):
        """
        Score and filter properties based on user preferences.
        
        Args:
            properties: List of property dicts from Supabase with transaction data
            prefs: User preferences dict from Supabase user_preferences table
        
        Returns:
            Sorted list of recommended properties with scores
        """
        results = []
        
        print(f"DEBUG: Total records received: {len(properties)}")
        print(f"DEBUG: Preferences received: {prefs}")
        
        for prop in properties:
            # Skip properties without transaction data
            if not prop.get('transactions') or len(prop['transactions']) == 0:
                print(f"DEBUG: Skipping {prop.get('property_id')} - no transaction data")
                continue
            
            # ---- Budget Filter (from price_sar in transactions) ----
            latest_transaction = prop['transactions'][0]
            price_sar = _to_float(latest_transaction.get('price_sar'))
            
            if price_sar is None:
                print(f"DEBUG: Skipping {prop.get('property_id')} - invalid price")
                continue
            
            if "min_budget" in prefs and prefs["min_budget"] is not None:
                if price_sar < prefs["min_budget"]:
                    print(f"DEBUG: Filtering out {prop['property_id']}: price {price_sar} < min {prefs['min_budget']}")
                    continue
            
            if "max_budget" in prefs and prefs["max_budget"] is not None:
                if price_sar > prefs["max_budget"]:
                    print(f"DEBUG: Filtering out {prop['property_id']}: price {price_sar} > max {prefs['max_budget']}")
                    continue
            
            # ---- Property Type Filter ----
            if "property_type" in prefs and prefs["property_type"]:
                prop_types = prefs["property_type"] if isinstance(prefs["property_type"], list) else [prefs["property_type"]]
                if prop.get('property_type') not in prop_types:
                    print(f"DEBUG: Filtering out {prop['property_id']}: property_type {prop.get('property_type')} not in {prop_types}")
                    continue
            
            # ---- Property Class Filter ----
            if "property_class" in prefs and prefs["property_class"]:
                prop_classes = prefs["property_class"] if isinstance(prefs["property_class"], list) else [prefs["property_class"]]
                if prop.get('property_class') not in prop_classes:
                    print(f"DEBUG: Filtering out {prop['property_id']}: property_class {prop.get('property_class')} not in {prop_classes}")
                    continue
            
            # ---- Location Filter (شرق، غرب، شمال، جنوب، وسط) ----
            if "location" in prefs and prefs["location"]:
                locations = prefs["location"] if isinstance(prefs["location"], list) else [prefs["location"]]
                if prop.get('location') not in locations:
                    print(f"DEBUG: Filtering out {prop['property_id']}: location {prop.get('location')} not in {locations}")
                    continue
            
            # ---- Area Filter ----
            area_sqm = _to_float(latest_transaction.get('area_sqm'))
            if area_sqm is None:
                print(f"DEBUG: Skipping {prop['property_id']} - invalid area")
                continue
            
            if "area_min" in prefs and prefs["area_min"] is not None:
                if area_sqm < prefs["area_min"]:
                    print(f"DEBUG: Filtering out {prop['property_id']}: area {area_sqm} < min {prefs['area_min']}")
                    continue
            
            if "area_max" in prefs and prefs["area_max"] is not None:
                if area_sqm > prefs["area_max"]:
                    print(f"DEBUG: Filtering out {prop['property_id']}: area {area_sqm} > max {prefs['area_max']}")
                    continue
            
            # ---- Calculate Scores ----
            goal = prefs.get("goal", "investment")
            price_per_sqm = _to_float(latest_transaction.get('price_per_sqm'), 1)
            
            if goal == "investment":
                # Lower price_per_sqm → cheaper entry cost → higher score
                score = 1000 / (price_per_sqm + 1) if price_per_sqm else 0
            elif goal == "residential":
                # Larger area → preferable
                score = area_sqm
            else:
                score = 0
            
            results.append({
                **prop,
                'score': score
            })
        
        # Sort by score descending
        results.sort(key=lambda x: x['score'], reverse=True)
        print(f"DEBUG: Returning {len(results)} properties after filtering and scoring")
        return results