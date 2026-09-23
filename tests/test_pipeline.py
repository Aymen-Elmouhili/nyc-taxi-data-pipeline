from sqlalchemy import text

from src.config.database import engine


def test_raw_table_exists():
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_schema = 'raw'
                    AND table_name = 'yellow_taxi_trips'
                );
            """)
        )

        assert result.scalar() is True


def test_fact_trips_contains_data():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT COUNT(*) FROM warehouse.fact_trips;")
        )

        count = result.scalar()

        assert count > 0


def test_dimensions_contain_data():
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT
                    (SELECT COUNT(*) FROM warehouse.dim_datetime),
                    (SELECT COUNT(*) FROM warehouse.dim_location);
            """)
        )

        datetime_count, location_count = result.fetchone()

        assert datetime_count > 0
        assert location_count > 0