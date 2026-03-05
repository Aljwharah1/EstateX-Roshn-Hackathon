import os
from dotenv import load_dotenv
from supabase import create_client

# Load env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if SUPABASE_URL and SUPABASE_SERVICE_KEY:
    sb = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    
    # Get distinct districts
    result = sb.table('properties').select('district').execute()
    districts = []
    for row in result.data:
        if row.get('district'):
            districts.append(row['district'])
    
    districts = sorted(list(set(districts)))
    print(f"Total districts: {len(districts)}")
    
    # Check for جنادرية
    target = "جنادرية"
    matching = [d for d in districts if target.lower() in d.lower()]
    print(f"\nDistricts matching '{target}':")
    for d in matching:
        print(f"  {repr(d)}")
    
    # Count properties in each matching district
    for district in matching:
        props = sb.table('properties').select('property_id').eq('district', district).execute()
        print(f"    Properties in {repr(district)}: {len(props.data)}")
    
    # Show all districts for reference
    print("\n\nAll districts in database (count):")
    for i, d in enumerate(districts):
        if i % 5 == 0:
            print()
        print(f"{i+1:2}. ", end="")
else:
    print("Supabase not configured")
