import pandas as pd

from src.config.database import engine


def daily_trips():
    query = """
        SELECT
            d.date,
            COUNT(*) AS total_trips
        FROM warehouse.fact_trips f
        JOIN warehouse.dim_datetime d
            ON f.pickup_datetime_id = d.datetime_id
        GROUP BY d.date
        ORDER BY d.date;
    """

    return pd.read_sql(query, engine)


def daily_revenue():
    query = """
        SELECT
            d.date,
            ROUND(SUM(f.total_amount)::numeric, 2) AS total_revenue
        FROM warehouse.fact_trips f
        JOIN warehouse.dim_datetime d
            ON f.pickup_datetime_id = d.datetime_id
        GROUP BY d.date
        ORDER BY d.date;
    """

    return pd.read_sql(query, engine)


def average_trip_metrics():
    query = """
        SELECT
            ROUND(AVG(trip_distance)::numeric, 2) AS avg_distance,
            ROUND(AVG(total_amount)::numeric, 2) AS avg_total_amount,
            ROUND(AVG(tip_amount)::numeric, 2) AS avg_tip,
            ROUND(AVG(passenger_count)::numeric, 2) AS avg_passengers
        FROM warehouse.fact_trips;
    """

    return pd.read_sql(query, engine)


def trips_by_hour():
    query = """
        SELECT
            d.hour,
            COUNT(*) AS total_trips
        FROM warehouse.fact_trips f
        JOIN warehouse.dim_datetime d
            ON f.pickup_datetime_id = d.datetime_id
        GROUP BY d.hour
        ORDER BY d.hour;
    """

    return pd.read_sql(query, engine)


def top_pickup_locations(limit=10):
    query = """
        SELECT
            pickup_location_id,
            COUNT(*) AS total_trips
        FROM warehouse.fact_trips
        GROUP BY pickup_location_id
        ORDER BY total_trips DESC
        LIMIT %(limit)s;
    """

    return pd.read_sql(
        query,
        engine,
        params={"limit": limit},
    )


def trips_by_payment_type():
    query = """
        SELECT
            payment_type,
            COUNT(*) AS total_trips
        FROM warehouse.fact_trips
        GROUP BY payment_type
        ORDER BY total_trips DESC;
    """

    return pd.read_sql(query, engine)