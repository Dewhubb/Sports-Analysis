# fetch_jma_month.py
# python3 fetch_jma_month.py

import time
import requests
import pandas as pd

# target: Hiroshima daily page (example)
BASE_URL = "https://www.data.jma.go.jp/stats/etrn/view/daily_s1.php"

params = {
    "prec_no": 67,     # prefecture code
    "block_no": 47765, # observation block / station code from your URL
    "year": 2025,
    "month": 3,        # change to 3 for March 2025
    "day": 15,
    "view": ""         # empty or choose view type; e.g. daily_s1.php returns daily summary
}

headers = {
    "User-Agent": "Mozilla/5.0 (your-email-or-project-name) Python requests" 
}

def fetch_month_csv(params, out_csv):
    # request page
    r = requests.get(BASE_URL, params=params, headers=headers, timeout=20)
    r.raise_for_status()
    r.encoding = r.apparent_encoding  # ensures correct Japanese encoding

    # parse tables on the page
    tables = pd.read_html(r.text)
    if not tables:
        raise RuntimeError("No tables found on page")

    # JMA pages often contain multiple tables; find the main data table.
    # Heuristic: pick the longest table (most rows/columns)
    main = max(tables, key=lambda df: df.shape[0] * df.shape[1])

    # Basic cleaning: drop completely empty columns, rename first column to '日付' if needed
    main = main.dropna(axis=1, how="all")
    # If the date is in a separate header row or index, adjust here
    # Example: ensure the first column is date-like
    if main.columns[0] != "日付" and "日" in str(main.columns[0]):
        main = main.rename(columns={ main.columns[0]: "日付" })

    # Save to CSV (UTF-8 with BOM so Excel in Windows can open easily)
    main.to_csv(out_csv, index=False, encoding="utf-8-sig")
    print(f"Saved {out_csv} (rows: {len(main)})")

if __name__ == "__main__":
    out_csv = "hiroshima_2025_03_daily.csv"
    fetch_month_csv(params, out_csv)
    # polite pause
    time.sleep(1)
