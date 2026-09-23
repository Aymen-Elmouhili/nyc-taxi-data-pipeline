import logging
from pathlib import Path

import pandas as pd

from src.config.database import engine
from src.config.logging_config import setup_logging

from src.config.settings import DATA_FILE

setup_logging()

logger = logging.getLogger(__name__)


def load_raw_data():
    try:
        logger.info("Reading parquet file...")

        df = pd.read_parquet(DATA_FILE)

        logger.info(f"Rows loaded from parquet: {len(df):,}")

        logger.info("Loading data into PostgreSQL...")

        df.to_sql(
            "yellow_taxi_trips",
            con=engine,
            schema="raw",
            if_exists="replace",
            index=False,
            chunksize=5000,
            method="multi",
        )

        logger.info(
            "Data successfully loaded into raw.yellow_taxi_trips"
        )

    except Exception:
        logger.exception("Error during raw data loading")
        raise


if __name__ == "__main__":
    load_raw_data()