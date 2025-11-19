import pandas as pd

df = pd.read_excel('data/Finalized_Data.xlsx')

# Filter by location, property type, and budget
north_apts = df[(df['location'] == 'شمال') & (df['property_type'] == 'apartment') & (df['price_sar'] <= 500000)]
print(f'North apartments under 500k SAR: {len(north_apts)}')

# Try without budget
north_apts_all = df[(df['location'] == 'شمال') & (df['property_type'] == 'apartment')]
print(f'North apartments (any budget): {len(north_apts_all)}')

# Check what prices exist for north
if len(north_apts_all) > 0:
    print(f'Min price: {north_apts_all["price_sar"].min()}')
    print(f'Max price: {north_apts_all["price_sar"].max()}')
    print(f'\nSample north apartments:')
    print(north_apts_all[['location', 'property_type', 'price_sar', 'district']].head(3))

