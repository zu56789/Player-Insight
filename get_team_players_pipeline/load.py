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


def get_team_id_for_team(conn: connection, team_name: str):
    """Retrieve the team ID for a given team name."""
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT team_id FROM team WHERE team_name = %s;",
            (team_name,)
        )
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            raise ValueError(
                f"Team '{team_name}' not found in the database.")


def get_team_names(conn: connection) -> list[str]:
    """Retrieve all team names from the team table."""
    with conn.cursor() as cursor:
        cursor.execute("SELECT team_name FROM team;")
        results = cursor.fetchall()
        return [row[0] for row in results]


def get_fbref_url_for_team(conn: connection, team_name: str) -> str:
    """Retrieve the fbref URL for a given team name."""
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT fbref_url FROM team WHERE team_name = %s;",
            (team_name,)
        )
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            raise ValueError(
                f"FBRef URL for team '{team_name}' not found in the database.")


if __name__ == "__main__":
    conn = get_rds_connection()
    teams = get_team_names(conn)
    for team in teams:
        team_id = get_team_id_for_team(conn, team)
        fbref_url = get_fbref_url_for_team(conn, team)
        print(
            f"Team ID is: {team_id}, Team name is {team}, fbref URL for team is: {fbref_url}")
