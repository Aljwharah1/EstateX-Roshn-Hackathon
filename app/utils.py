# app/utils.py
"""
Utility functions for EstateX.
All data operations use Supabase as the single source of truth.
"""
import os
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import joblib
from dotenv import load_dotenv

load_dotenv()


def get_supabase_client():
    """Get initialized Supabase client."""
    from supabase import create_client
    
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")
    
    return create_client(url, key)


def load_properties_from_supabase():
    """Load properties with latest transaction data from Supabase."""
    sb = get_supabase_client()
    
    try:
        result = sb.table('properties').select('*').execute()
        return result.data or []
    except Exception as e:
        print(f"Error loading properties from Supabase: {e}")
        return []


def load_transactions_from_supabase():
    """Load all transactions from Supabase."""
    sb = get_supabase_client()
    
    try:
        result = sb.table('transactions').select('*').execute()
        return result.data or []
    except Exception as e:
        print(f"Error loading transactions from Supabase: {e}")
        return []


def get_property_with_transactions(property_id: str):
    """Get property with its transaction history from Supabase."""
    sb = get_supabase_client()
    
    try:
        prop_result = sb.table('properties').select('*').eq('property_id', property_id).execute()
        if not prop_result.data:
            return None
        
        trans_result = sb.table('transactions').select('*').eq('property_id', property_id).order('date', desc=True).execute()
        
        property_data = prop_result.data[0]
        property_data['transactions'] = trans_result.data or []
        
        return property_data
    except Exception as e:
        print(f"Error loading property {property_id}: {e}")
        return None


def build_preprocessor(properties: list):
    """
    Build and save a preprocessor for ML models using Supabase data.
    
    Args:
        properties: List of property dicts from Supabase
    """
    if not properties:
        print("Warning: No properties provided to build preprocessor")
        return {}
    
    # Extract categorical and numeric features
    cat_cols = ['district', 'property_type']
    num_cols = ['area_sqm', 'price_per_sqm']
    
    # Build lists of values for fitting
    cat_data = []
    num_data = []
    
    for prop in properties:
        try:
            cat_row = [prop.get(col, '') for col in cat_cols]
            cat_data.append(cat_row)
        except Exception:
            pass
    
    # For numeric columns, we'd need to get from transactions
    # For now, create dummy data so preprocessor can be initialized
    ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    scaler = StandardScaler()
    
    if cat_data:
        ohe.fit(cat_data)
    
    # Save preprocessor
    joblib.dump({'ohe': ohe, 'scaler': scaler}, "models/preprocessing.joblib")
    return {'ohe': ohe, 'scaler': scaler}