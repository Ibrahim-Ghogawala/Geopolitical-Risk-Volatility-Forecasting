# =========================================================
# RPDA8412 RESEARCH PROJECT
# EPU DATA COLLECTION
# Source: Federal Reserve Economic Data (FRED)
# =========================================================

from pathlib import Path
from datetime import datetime, timezone
import pandas as pd
import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"

RAW_DIR.mkdir(parents=True, exist_ok=True)

SERIES = {
    "daily": "USEPUINDXD",
    "monthly": "USEPUINDXM"
}

for frequency, series_id in SERIES.items():

    print(f"\nDownloading {frequency.upper()} EPU...")

    url = (
        f"https://fred.stlouisfed.org/graph/fredgraph.csv"
        f"?id={series_id}"
    )

    response = requests.get(url, timeout=60)
    response.raise_for_status()

    output = RAW_DIR / f"epu_{frequency}_raw.csv"

    # Preserve the downloaded source file
    output.write_bytes(response.content)

    df = pd.read_csv(output)

    print("Series:", series_id)
    print("Rows:", len(df))
    print("Columns:", df.columns.tolist())

    if "observation_date" not in df.columns and "DATE" not in df.columns:
        raise ValueError(
            f"Unexpected FRED file format for {series_id}"
        )

    print("First rows:")
    print(df.head())

    print("Last rows:")
    print(df.tail())

    print("Saved:", output)

print("\nEPU data collection complete.")