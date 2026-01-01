from datetime import datetime


def transform_player_dob(player_dob: str) -> datetime.date:
    """Transform player date of birth to a standardized format."""
    try:
        return datetime.strptime(player_dob, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(
            "Player date of birth must be in 'YYYY-MM-DD' format.")


def transform_player_height(player_height: str) -> int:
    """Transform player height from string in cm to integer."""
    try:
        return int(player_height)
    except ValueError:
        raise ValueError("Player height must be an integer representing cm.")


def transform_player_details(player_data: dict) -> dict:
    """Transform and validate player data dictionary."""
    player_dob = player_data.get("player_dob")
    if player_dob != "Unknown":
        player_dob = transform_player_dob(player_dob)
    player_height = player_data.get("player_height")
    if player_height != "Unknown":
        player_height = transform_player_height(
            player_height)

    return {
        "player_name": player_data.get("player_name"),
        "player_position": player_data.get("player_position"),
        "player_nationality": player_data.get("player_nationality"),
        "player_dob": player_dob,
        "player_height": player_height,
        "player_strong_foot": player_data.get("player_strong_foot"),
        "team_name": player_data.get("team_name"),
        "fbref_url": player_data.get("fbref_url")

    }


if __name__ == "__main__":
    player = {'player_name': 'Dario Essugo', 'player_position': 'MF', 'player_nationality': 'Portugal', 'player_dob': '2005-03-14',
              'player_height': 'Unknown', 'player_strong_foot': 'Unknown',
              'team_name': 'Chelsea', 'fbref_url': 'https://fbref.com/en/players/1e4319ac/Dario-Essugo'}
    transformed_player = transform_player_details(player)
    print(transformed_player)
