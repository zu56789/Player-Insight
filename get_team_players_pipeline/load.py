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


def get_team_names_pl(conn: connection, league_name="Premier League", league_season="2025-2026") -> list[str]:
    """Retrieve all team names from the pl table."""
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT t.team_name
            FROM team t
            JOIN league l ON t.league_id = l.league_id
            WHERE l.league_name = %s
            AND l.league_season = %s;
            """,
            (league_name, league_season))
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


def insert_player_data(conn: connection, player_data: dict) -> bool:
    team_id = get_team_id_for_team(conn, player_data["team_name"])
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO player (player_name, player_position, player_nationality, player_dob,
                  player_height, player_strong_foot, team_id, fbref_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (player_data["player_name"],
                 player_data["player_position"],
                 player_data["player_nationality"],
                 player_data["player_dob"],
                 player_data["player_height"],
                 player_data["player_strong_foot"],
                 team_id,
                 player_data["fbref_url"])
            )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e


def check_if_player_exists(conn: connection, player_name: str, team_name: str) -> bool:
    """Function used to check if a player already exists in the database"""
    team_id = get_team_id_for_team(conn, team_name)
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM player WHERE player_name = %s AND team_id = %s", (player_name, team_id))
        result = cursor.fetchone()
        if result:
            return True
        return False


if __name__ == "__main__":
    conn = get_rds_connection()
    teams = get_team_names(conn)
    for team in teams:
        team_id = get_team_id_for_team(conn, team)
        fbref_url = get_fbref_url_for_team(conn, team)
        print(
            f"Team ID is: {team_id}, Team name is {team}, fbref URL for team is: {fbref_url}")
