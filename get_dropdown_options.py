import os
from dotenv import load_dotenv
from supabase import create_client

# Load env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if SUPABASE_URL and SUPABASE_SERVICE_KEY:
    sb = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    
    # Get distinct property types
    result = sb.table('properties').select('property_type').execute()
    property_types = sorted(list(set([r.get('property_type') for r in result.data if r.get('property_type')])))
    print("Property Types:")
    print(property_types)
    
    # Get distinct cities
    result = sb.table('properties').select('region').execute()
    cities = sorted(list(set([r.get('region') for r in result.data if r.get('region')])))
    print("\nCities/Regions:")
    print(cities)
    
    # Get bedrooms range
    result = sb.table('properties').select('bedrooms').execute()
    bedrooms = [r.get('bedrooms') for r in result.data if r.get('bedrooms') is not None]
    print(f"\nBedrooms range: {min(bedrooms)} - {max(bedrooms)}")
    
    # Get bathrooms range
    result = sb.table('properties').select('bathrooms').execute()
    bathrooms = [r.get('bathrooms') for r in result.data if r.get('bathrooms') is not None]
    print(f"Bathrooms range: {min(bathrooms)} - {max(bathrooms)}")
    
    # Get area range from transactions
    result = sb.table('transactions').select('area_sqm').execute()
    areas = []
    for r in result.data:
        try:
            area = float(r.get('area_sqm', 0))
            if area > 0:
                areas.append(area)
        except:
            pass
    if areas:
        print(f"Area range: {min(areas)} - {max(areas)} m²")
    
else:
    print("Supabase not configured")
