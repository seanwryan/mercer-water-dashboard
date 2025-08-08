import pandas as pd

# Load CSV file
file_path = 'resultphyschem.csv'  # Adjust path if needed
df = pd.read_csv(file_path, low_memory=False)

# Show basic info
print("=== Dataset Info ===")
print(df.info())

# Preview first few rows
print("\n=== Sample Data ===")
print(df.head())

# Check for missing data
print("\n=== Missing Values Summary ===")
print(df.isnull().sum().sort_values(ascending=False))

# List of all columns
print("\n=== Column Names ===")
print(df.columns.tolist())

# Identify unique values in key fields
key_fields = [
    'MonitoringLocationName', 
    'CharacteristicName', 
    'ResultMeasure/MeasureUnitCode', 
    'ActivityStartDate', 
    'ResultSampleFractionText'
]

print("\n=== Unique Values in Key Fields ===")
for field in key_fields:
    if field in df.columns:
        print(f"\n{field} ({df[field].nunique()} unique values):")
        print(df[field].unique()[:10])  # Show only first 10 unique values

# Convert date and inspect range
if 'ActivityStartDate' in df.columns:
    df['ActivityStartDate'] = pd.to_datetime(df['ActivityStartDate'], errors='coerce')
    print("\n=== Date Range ===")
    print(f"From {df['ActivityStartDate'].min()} to {df['ActivityStartDate'].max()}")

# Location coverage
if 'MonitoringLocationName' in df.columns:
    print("\n=== Number of Monitoring Locations ===")
    print(df['MonitoringLocationName'].nunique())
    print(df['MonitoringLocationName'].value_counts().head(10))

# Parameters/Characteristics sampled
if 'CharacteristicName' in df.columns:
    print("\n=== Most Common Parameters ===")
    print(df['CharacteristicName'].value_counts().head(10))