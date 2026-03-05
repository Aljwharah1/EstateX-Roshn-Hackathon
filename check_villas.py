import os
from dotenv import load_dotenv
from supabase import create_client

# Load env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if SUPABASE_URL and SUPABASE_SERVICE_KEY:
    sb = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    
    # Get all villas in الجنادرية
    result = sb.table('properties').select('property_id, property_type, district').eq('district', 'الجنادرية').execute()
    
    print(f"Total properties in الجنادرية: {len(result.data)}")
    
    # Count by property type
    types_count = {}
    for prop in result.data:
        ptype = prop.get('property_type', 'unknown')
        types_count[ptype] = types_count.get(ptype, 0) + 1
    
    print("\nProperty types in الجنادرية:")
    for ptype, count in sorted(types_count.items()):
        print(f"  '{ptype}': {count}")
    
    # Check for villa-like values
    print("\nSearching for villa-related properties:")
    villa_props = [p for p in result.data if 'villa' in str(p.get('property_type', '')).lower()]
    print(f"  Lowercase match 'villa': {len(villa_props)}")
    
    villa_props_ar = [p for p in result.data if 'فيلا' in str(p.get('property_type', ''))]
    print(f"  Arabic 'فيلا' match: {len(villa_props_ar)}")
    
else:
    print("Supabase not configured")
