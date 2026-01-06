import logging
from extract import get_team_players, get_player_details
from transform import transform_player_details
from load import get_rds_connection, get_team_id_for_team, get_team_names, get_fbref_url_for_team, insert_player_data


def run_pipeline():
    print("start")
    conn = get_rds_connection()
    team_names = get_team_names(conn)
    print(f"{len(team_names)} teams")
    team_to_player_dict = {}
    for team in team_names:
        team_url = get_fbref_url_for_team(conn, team)
        team_players = get_team_players(team, team_url)
        team_to_player_dict[team] = team_players
        # for player in team_players:
        #     player_details = get_player_details(
        #         player["player_name"], player["team_name"], player["fbref_url"])
    print(team_to_player_dict)


if __name__ == "__main__":
    run_pipeline()
