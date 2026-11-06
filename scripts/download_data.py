"""
Download one year of City of Melbourne hourly pedestrian counts,
then print a quick check of what we got.

Run from the repo folder:  python scripts/download_data.py
"""
from pathlib import Path

import pandas as pd
import requests

YEAR = 2025  # change this if the year comes back empty

URL = (
    "https://data.melbourne.vic.gov.au/api/explore/v2.1/catalog/datasets/"
    "pedestrian-counting-system-monthly-counts-per-hour/exports/csv"
)
PARAMS = {
    "where": f"sensing_date >= date'{YEAR}-01-01' AND sensing_date < date'{YEAR + 1}-01-01'",
    "delimiter": ",",
}

out = Path(__file__).resolve().parents[1] / "data" / "raw" / f"pedestrian_counts_{YEAR}.csv"
out.parent.mkdir(parents=True, exist_ok=True)

# 1. Download (streamed in chunks so a big file doesn't fill your RAM)
print(f"Downloading {YEAR} data... this can take a few minutes")
with requests.get(URL, params=PARAMS, stream=True, timeout=900) as r:
    r.raise_for_status()
    with open(out, "wb") as f:
        for chunk in r.iter_content(chunk_size=1 << 20):
            f.write(chunk)
print(f"Saved {out.name} ({out.stat().st_size / 1e6:.1f} MB)")

# 2. Quick check - you should be able to explain every number printed here
df = pd.read_csv(out, parse_dates=["sensing_date"])
if df.empty:
    raise SystemExit(f"No rows for {YEAR}. Change YEAR at the top and run again.")

print("\nRows:", f"{len(df):,}")
print("Columns:", list(df.columns))
print("Date range:", df["sensing_date"].min().date(), "to", df["sensing_date"].max().date())
print("Number of sensors:", df["sensor_name"].nunique())
print("Missing values per column:\n", df.isna().sum())
print("\nTop 5 busiest sensors (total pedestrians):")
print(df.groupby("sensor_name")["pedestriancount"].sum().nlargest(5))
