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


def get_league_names(conn: connection) -> list[str]:
    """Retrieve all league names from the league table."""
    with conn.cursor() as cursor:
        cursor.execute("SELECT league_name FROM league;")
        results = cursor.fetchall()
        return [row[0] for row in results]


def get_fbref_url_for_league(conn: connection, league_name: str) -> str:
    """Retrieve the fbref URL for a given league name."""
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT fbref_url FROM league WHERE league_name = %s;",
            (league_name,)
        )
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            raise ValueError(
                f"FBRef URL for league '{league_name}' not found in the database.")


def insert_team_data(conn: connection, team_data: dict) -> bool:
    """Insert team data into the teams table."""
    league_id = get_league_id_for_league(conn, team_data["league_name"])
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO team (team_name, league_id, fbref_url)
                VALUES (%s, %s, %s);
                """,
                (team_data["team_name"],
                 league_id,
                 team_data["fbref_url"])
            )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e


if __name__ == "__main__":
    conn = get_rds_connection()
    print("Connection to RDS database established successfully.")
    league_names = get_league_names(conn)
    for league_name in league_names:

        try:
            league_id = get_league_id_for_league(conn, league_name)
            print(f"League ID for '{league_name}': {league_id}")
        except ValueError as e:
            print(e)
    conn.close()
