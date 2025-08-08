import pandas as pd

# Load the raw dataset
df = pd.read_csv("resultphyschem.csv", low_memory=False)

# Extract unique site names (ignore NaNs)
site_names = df['MonitoringLocationName'].dropna().unique()
site_names = sorted(site_names)

# Print to console
print(f"Found {len(site_names)} unique site names:\n")
for name in site_names:
    print(name)

# Optional: Save to CSV or TXT file for manual review
pd.Series(site_names).to_csv("unique_site_names.csv", index=False, header=["site_name"])
print("\n✅ Saved to 'unique_site_names.csv'")