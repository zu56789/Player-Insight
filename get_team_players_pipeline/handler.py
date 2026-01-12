import logging
from extract import get_team_players, get_player_details
from transform import transform_player_details
from load import get_rds_connection, get_team_id_for_team, get_team_names_pl, get_fbref_url_for_team, insert_player_data


def run_pipeline():
    print("Starting Pipeline")
    conn = get_rds_connection()
    # only Chelsea and Real Madrid players due to firecrawl limits on scraping
    team_names = ["Chelsea", "Real Madrid"]
    print(f"Found {len(team_names)} teams")
    team_to_player_dict = {}
    player_details_list = []
    transformed_player_details_list = []
    players_inserted = 0
    # EXTRACT
    for team in team_names:
        print(f"Extracting players for {team}")
        team_url = get_fbref_url_for_team(conn, team)
        team_players = get_team_players(team, team_url)
        # put player stuff into a dictionary of dictionaries
        team_to_player_dict[team] = team_players
        # {Arsenal: [{player_name: hi}, {player_name: hi2}], Chelsea: [{player_name: Sanchez}]}
    for team, players in team_to_player_dict.items():
        print(f"Extracting player info for {team}")
        for i in range(len(players)):
            print("Extracting info for" + " " + players[i].get("player_name"))
            player_details = get_player_details(
                players[i]["player_name"], players[i]["team_name"], players[i]["fbref_url"])
            # put player details into a list of dictionaries
            player_details_list.append(player_details)
    # TRANSFORM
    for player in player_details_list:
        print("Transforming data for" + " " + player["player_name"])
        transformed_player = transform_player_details(player)
        # put transformed player details into a list of dictionaries
        transformed_player_details_list.append(transformed_player)
    # LOAD
    for transformed_player_details in transformed_player_details_list:
        try:
            print("Loading " +
                  transformed_player_details["player_name"] + " into database")
            insert_player_data(conn, transformed_player_details)
            players_inserted += 1
        except Exception as e:
            print("Failed to load player: " +
                  transformed_player_details["player_name"])
            continue
    print(f"Inserted {players_inserted} players into the database")


if __name__ == "__main__":
    run_pipeline()
