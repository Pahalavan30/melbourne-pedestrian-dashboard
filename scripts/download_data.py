"""
Download one year of City of Melbourne hourly pedestrian counts
plus the sensor locations table, then print a quick check.

Run from the repo folder:  python scripts/download_data.py
"""
from pathlib import Path

import pandas as pd
import requests

YEAR = 2025  # change this if the year comes back empty

BASE = "https://data.melbourne.vic.gov.au/api/explore/v2.1/catalog/datasets/"
RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)


def download(dataset: str, out: Path, where: str | None = None) -> None:
    """Stream a dataset export to a CSV file (chunks keep RAM use low)."""
    params = {"delimiter": ","}
    if where:
        params["where"] = where
    print(f"Downloading {out.name}...")
    with requests.get(f"{BASE}{dataset}/exports/csv", params=params, stream=True, timeout=900) as r:
        r.raise_for_status()
        with open(out, "wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 20):
                f.write(chunk)
    print(f"  saved ({out.stat().st_size / 1e6:.1f} MB)")


counts_file = RAW / f"pedestrian_counts_{YEAR}.csv"
sensors_file = RAW / "sensor_locations.csv"

# 1. Download (skip the big file if we already have it)
if not counts_file.exists():
    download(
        "pedestrian-counting-system-monthly-counts-per-hour",
        counts_file,
        where=f"sensing_date >= date'{YEAR}-01-01' AND sensing_date < date'{YEAR + 1}-01-01'",
    )
download("pedestrian-counting-system-sensor-locations", sensors_file)

# 2. Quick check of the hourly counts
df = pd.read_csv(counts_file, parse_dates=["sensing_date"])
if df.empty:
    raise SystemExit(f"No rows for {YEAR}. Change YEAR at the top and run again.")

print("\n--- Hourly counts ---")
print("Rows:", f"{len(df):,}")
print("Date range:", df["sensing_date"].min().date(), "to", df["sensing_date"].max().date())
print("Sensors:", df["location_id"].nunique())
print("Rows missing a sensor name:", f"{df['sensor_name'].isna().sum():,}")

# 3. Quick check of the sensor locations
sensors = pd.read_csv(sensors_file)
print("\n--- Sensor locations ---")
print("Rows:", len(sensors))
print("Columns:", list(sensors.columns))

# 4. Does joining on location_id fix the missing names?
lookup = sensors[["location_id", "sensor_description"]].drop_duplicates("location_id")
merged = df.merge(lookup, on="location_id", how="left")
missing_before = df["sensor_name"].isna().sum()
still_missing = merged.loc[df["sensor_name"].isna(), "sensor_description"].isna().sum()
print("\n--- Join check ---")
print(f"Missing names before join: {missing_before:,}")
print(f"Still missing after join:  {still_missing:,}")
print(f"Count rows with no matching sensor at all: {merged['sensor_description'].isna().sum():,}")

print("\nTop 5 busiest locations (readable names):")
print(merged.groupby("sensor_description")["pedestriancount"].sum().nlargest(5))
