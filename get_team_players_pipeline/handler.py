import logging
from extract import get_team_players, get_player_details
from transform import transform_player_details
from load import get_rds_connection, get_fbref_url_for_team, insert_player_data, check_if_player_exists
from psycopg2.extensions import connection


def extract_team_players(conn: connection, team_names: list[str]) -> dict[str, list[dict]]:
    """Function which extracts players in the teams given and puts them in a dictionary"""
    team_to_player_dict = {}
    for team in team_names:
        print(f"Extracting players for {team}")
        team_url = get_fbref_url_for_team(conn, team)
        team_players = get_team_players(team, team_url)
        team_to_player_dict[team] = team_players
    return team_to_player_dict


def extract_player_details(team_to_player_dict: dict[str, list[dict]]) -> list[dict]:
    """Function which extracts player details from the dictionary of players
         and puts them in a list of dictionaries"""

    player_details_list = []

    for team, players in team_to_player_dict.items():
        print(f"Extracting player info for {team}")
        for i in range(len(players)):
            print("Extracting info for" + " " + players[i].get("player_name"))
            player_details = get_player_details(
                players[i]["player_name"], players[i]["team_name"], players[i]["fbref_url"])
            player_details_list.append(player_details)

    return player_details_list


def transform_players(player_details_list: list[dict]) -> list[dict]:
    """Function for iterating through each player and transforming"""
    transformed_players = []

    for player in player_details_list:
        print("Transforming data for" + " " + player["player_name"])
        transformed_players.append(
            transform_player_details(player)
        )

    return transformed_players


def load_players(conn: connection, transformed_player_details_list: list[dict]) -> int:
    """Function for loading each player into the database"""
    players_inserted = 0
    for transformed_player_details in transformed_player_details_list:
        try:
            exists = check_if_player_exists(
                conn, transformed_player_details["player_name"], transformed_player_details["team_name"])
            if exists:
                print("Skipping existing player: " +
                      transformed_player_details["player_name"])
                continue
            print("Loading " +
                  transformed_player_details["player_name"] + " into database")
            insert_player_data(conn, transformed_player_details)
            players_inserted += 1
        except Exception as e:
            print("Failed to load player: " +
                  transformed_player_details["player_name"])
            continue
    return players_inserted


def run_pipeline():
    print("Starting Pipeline")
    conn = get_rds_connection()
    # only Chelsea and Real Madrid players due to firecrawl limits on scraping
    team_names = ["Chelsea", "Real Madrid"]
    print(f"Found {len(team_names)} teams")
    team_to_player_dict = extract_team_players(conn, team_names)
    player_details_list = extract_player_details(team_to_player_dict)
    transformed_players = transform_players(player_details_list)
    players_inserted = load_players(conn, transformed_players)

    print(f"Inserted {players_inserted} players into the database")


if __name__ == "__main__":
    run_pipeline()
