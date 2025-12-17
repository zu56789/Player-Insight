import os
from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.extensions import connection

load_dotenv()  # Load environment variables from .env file


def get_rds_connection() -> connection:
    """Establish a connection to the PostgreSQL RDS database."""

    conn = connect(
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST")
    )
    return conn


def get_league_id_for_league(conn: connection, league_name: str) -> int:
    """Retrieve the league ID for a given league name."""
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT league_id FROM league WHERE league_name = %s;",
            (league_name,)
        )
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            raise ValueError(
                f"League '{league_name}' not found in the database.")


if __name__ == "__main__":
    conn = get_rds_connection()
    print("Connection to RDS database established successfully.")
    league_names = ["Premier League", "La Liga",
                    "Bundesliga", "Serie A", "Ligue 1"]
    for league_name in league_names:

        try:
            league_id = get_league_id_for_league(conn, league_name)
            print(f"League ID for '{league_name}': {league_id}")
        except ValueError as e:
            print(e)
    conn.close()
