import pandas as pd
from sqlalchemy import text

from src.config.database import engine

import logging 

logger = logging.getLogger(__name__)

def transform_data():

    try:

        logger.info("Reading data from raw.yellow_taxi_trips...")

        query = """
            SELECT
                "tpep_pickup_datetime",
                "tpep_dropoff_datetime",
                "passenger_count",
                "trip_distance",
                "PULocationID",
                "DOLocationID",
                "payment_type",
                "fare_amount",
                "tip_amount",
                "total_amount"
            FROM raw.yellow_taxi_trips
        """

        df = pd.read_sql(query, engine)

        logger.info(f"Rows read: {len(df):,}")

        # --------------------------------------------------
        # 1. Clean data
        # --------------------------------------------------

        df["tpep_pickup_datetime"] = pd.to_datetime(
            df["tpep_pickup_datetime"]
        )

        df["tpep_dropoff_datetime"] = pd.to_datetime(
            df["tpep_dropoff_datetime"]
        )

        df = df.dropna(
            subset=[
                "tpep_pickup_datetime",
                "tpep_dropoff_datetime",
                "PULocationID",
                "DOLocationID",
            ]
        )

        df = df[
            (df["tpep_dropoff_datetime"] >= df["tpep_pickup_datetime"])
            & (df["trip_distance"] >= 0)
            & (df["total_amount"] >= 0)
        ].copy()

        logger.info(f"Rows after cleaning: {len(df):,}")

        # --------------------------------------------------
        # 2. Create dim_location
        # --------------------------------------------------

        locations = pd.concat(
            [
                df["PULocationID"],
                df["DOLocationID"],
            ]
        ).dropna().drop_duplicates()

        locations = pd.DataFrame(
            {
                "location_id": locations.astype(int)
            }
        )

        # --------------------------------------------------
        # 3. Create dim_datetime
        # --------------------------------------------------

        datetimes = pd.concat(
            [
                df["tpep_pickup_datetime"],
                df["tpep_dropoff_datetime"],
            ]
        ).drop_duplicates()

        dim_datetime = pd.DataFrame(
            {
                "datetime": datetimes
            }
        )

        dim_datetime["date"] = dim_datetime["datetime"].dt.date
        dim_datetime["year"] = dim_datetime["datetime"].dt.year
        dim_datetime["month"] = dim_datetime["datetime"].dt.month
        dim_datetime["day"] = dim_datetime["datetime"].dt.day
        dim_datetime["hour"] = dim_datetime["datetime"].dt.hour
        dim_datetime["day_of_week"] = (
            dim_datetime["datetime"].dt.dayofweek
        )

        # --------------------------------------------------
        # 4. Rebuild warehouse dimensions
        # --------------------------------------------------

        with engine.begin() as connection:

            connection.execute(
                text("TRUNCATE warehouse.fact_trips RESTART IDENTITY;")
            )

            connection.execute(
                text("TRUNCATE warehouse.dim_datetime RESTART IDENTITY CASCADE;")
            )

            connection.execute(
                text("TRUNCATE warehouse.dim_location CASCADE;")
            )

        locations.to_sql(
            "dim_location",
            engine,
            schema="warehouse",
            if_exists="append",
            index=False,
        )

        dim_datetime.to_sql(
            "dim_datetime",
            engine,
            schema="warehouse",
            if_exists="append",
            index=False,
        )

        # --------------------------------------------------
        # 5. Get datetime IDs
        # --------------------------------------------------

        datetime_lookup = pd.read_sql(
            """
            SELECT datetime_id, datetime
            FROM warehouse.dim_datetime
            """,
            engine,
        )

        # --------------------------------------------------
        # 6. Add datetime foreign keys
        # --------------------------------------------------

        df = df.merge(
            datetime_lookup,
            left_on="tpep_pickup_datetime",
            right_on="datetime",
            how="left",
        )

        df = df.rename(
            columns={
                "datetime_id": "pickup_datetime_id"
            }
        )

        df = df.drop(columns=["datetime"])

        df = df.merge(
            datetime_lookup,
            left_on="tpep_dropoff_datetime",
            right_on="datetime",
            how="left",
        )

        df = df.rename(
            columns={
                "datetime_id": "dropoff_datetime_id"
            }
        )

        df = df.drop(columns=["datetime"])

        # --------------------------------------------------
        # 7. Create fact_trips
        # --------------------------------------------------

        fact_trips = pd.DataFrame(
            {
                "pickup_location_id": df["PULocationID"].astype(int),
                "dropoff_location_id": df["DOLocationID"].astype(int),
                "passenger_count": df["passenger_count"],
                "trip_distance": df["trip_distance"],
                "fare_amount": df["fare_amount"],
                "tip_amount": df["tip_amount"],
                "total_amount": df["total_amount"],
                "payment_type": df["payment_type"],
                "pickup_datetime_id": df["pickup_datetime_id"],
                "dropoff_datetime_id": df["dropoff_datetime_id"],
            }
        )

        # --------------------------------------------------
        # 8. Load fact table
        # --------------------------------------------------

        fact_trips.to_sql(
            "fact_trips",
            engine,
            schema="warehouse",
            if_exists="append",
            index=False,
            chunksize=5000,
            method="multi",
        )

        logger.info("Transformation completed successfully.")
        logger.info(f"Rows loaded into fact_trips: {len(fact_trips):,}")

    except Exception:
        logger.exception("Error during data transformation")
        raise
if __name__ == "__main__":
    transform_data()