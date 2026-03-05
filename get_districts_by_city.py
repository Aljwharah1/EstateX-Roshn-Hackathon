import os
import json
from dotenv import load_dotenv
from supabase import create_client

# Load env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if SUPABASE_URL and SUPABASE_SERVICE_KEY:
    sb = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    
    # Get distinct cities and their districts
    result = sb.table('properties').select('region, district').execute()
    
    districts_by_city = {}
    for row in result.data:
        city = row.get('region', 'Unknown')
        district = row.get('district')
        if district:
            if city not in districts_by_city:
                districts_by_city[city] = set()
            districts_by_city[city].add(district)
    
    # Convert sets to sorted lists
    districts_by_city = {city: sorted(list(districts)) for city, districts in districts_by_city.items()}
    
    print("Districts by City:")
    print(json.dumps(districts_by_city, ensure_ascii=False, indent=2))
    
else:
    print("Supabase not configured")
