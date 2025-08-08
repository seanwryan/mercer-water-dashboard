import pandas as pd

# Load raw dataset
df = pd.read_csv("resultphyschem.csv", low_memory=False)

# Rename useful columns with final user-friendly names
df = df.rename(columns={
    'MonitoringLocationName': 'Location',
    'ActivityLocation/LatitudeMeasure': 'Latitude',
    'ActivityLocation/LongitudeMeasure': 'Longitude',
    'ActivityStartDate': 'Date',
    'CharacteristicName': 'Parameter',
    'ResultSampleFractionText': 'Sample Fraction',
    'ResultMeasureValue': 'Value',
    'ResultMeasure/MeasureUnitCode': 'Unit',
    'OrganizationFormalName': 'Organization'
})

# Select only relevant columns
keep_cols = [
    'Location', 'Latitude', 'Longitude', 'Date',
    'Parameter', 'Sample Fraction', 'Value', 'Unit', 'Organization'
]
df_clean = df[keep_cols].copy()

# Drop rows with critical missing values
df_clean.dropna(subset=[
    'Location', 'Latitude', 'Longitude', 'Date', 'Parameter', 'Value', 'Unit'
], inplace=True)

# Parse types
df_clean['Date'] = pd.to_datetime(df_clean['Date'], errors='coerce')
df_clean['Value'] = pd.to_numeric(df_clean['Value'], errors='coerce')

# Standardize units
df_clean['Unit'] = df_clean['Unit'].str.strip().str.lower().replace({
    'mg/l': 'mg/L',
    '#/100ml': '#/100mL',
    'cfu/100ml': '#/100mL',
    'mpn/100ml': '#/100mL',
    'ug/l': 'µg/L'
})

# Drop rows with invalid parsed values
df_clean.dropna(subset=['Date', 'Value'], inplace=True)

# Reset index and export
df_clean.reset_index(drop=True, inplace=True)
df_clean.to_csv("cleaned_water_quality_for_app.csv", index=False)
print("✅ Cleaned and exported to 'cleaned_water_quality_for_app.csv'")