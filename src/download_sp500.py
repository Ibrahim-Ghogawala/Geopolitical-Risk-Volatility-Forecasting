import yfinance as yf
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)

print("Downloading S&P 500...")

sp500 = yf.download(
    "^GSPC",
    start="2010-01-01",
    end="2026-01-01",
    interval="1d",
    auto_adjust=False,
    progress=False
)

if sp500.empty:
    raise RuntimeError("S&P 500 download returned no data.")

output = RAW / "sp500_daily_raw.csv"
sp500.to_csv(output)

print("\nDownload complete.")
print("Rows:", len(sp500))
print("First date:", sp500.index.min())
print("Last date:", sp500.index.max())
print("Saved to:", output)