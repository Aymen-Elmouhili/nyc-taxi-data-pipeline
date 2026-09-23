from pathlib import Path
import pandas as pd 


URL = (
    "https://d37ci6vzurychx.cloudfront.net/trip-data/"
    "yellow_tripdata_2025-01.parquet"
)


OUTPUT_DIR = Path("data/raw")
OUTPUT_FILE = OUTPUT_DIR / "yellow_tripdata_2025-01.parquet"


def download_data():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Downloading NYC taxi data ")

    df = pd.read_parquet(URL)

    df.to_parquet(OUTPUT_FILE, index = False)

    print(f"Data saved to: {OUTPUT_FILE}")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")


if __name__ == "__main__":
    download_data()