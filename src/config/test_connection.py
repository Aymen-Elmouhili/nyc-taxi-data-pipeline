from sqlalchemy import text

from src.config.database import engine


def test_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        print(result.fetchone())


if __name__ == "__main__":
    test_connection()