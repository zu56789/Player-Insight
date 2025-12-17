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


def upload_league_data(conn: connection, league_data: dict) -> bool:
    """Upload league data to the PostgreSQL RDS database."""
    check_query = """
        SELECT * FROM league
        WHERE league_name = %s AND league_season = %s;
        """
    with conn.cursor() as cursor:

        cursor.execute(check_query, (
            league_data['league_name'],
            league_data['league_season']
        ))
        existing_league = cursor.fetchone()
        if existing_league:
            return False  # League data already exists

        insert_query = """
        INSERT INTO league (league_name, league_country, league_season, fbref_url)
        VALUES (%s, %s, %s, %s);
        """

        cursor.execute(insert_query, (
            league_data['league_name'],
            league_data['league_country'],
            league_data['league_season'],
            league_data['fbref_url']
        ))
        conn.commit()
        return True
