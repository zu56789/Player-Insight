def validate_team_name(team_name: str) -> str:
    """Transform team name to a standardized format."""
    if not isinstance(team_name, str):
        raise ValueError("Team name must be a string.")
    if len(team_name) == 0:
        raise ValueError("Team name cannot be empty.")
    return team_name.strip().title()


def validate_fbref_url(fbref_url: str) -> str:
    """Ensure the fbref URL is complete and valid."""
    if not isinstance(fbref_url, str):
        raise ValueError("FBRef URL must be a string.")
    if len(fbref_url) == 0:
        raise ValueError("FBRef URL cannot be empty.")
    fbref_url = fbref_url.strip()
    if not fbref_url.startswith("https://fbref.com"):
        fbref_url = "https://fbref.com" + fbref_url
    return fbref_url


def transform_team_data(team_data: dict) -> dict:
    """Transform and validate team data dictionary."""
    team_name = validate_team_name(team_data.get("team_name", ""))
    fbref_url = validate_fbref_url(team_data.get("fbref_link", ""))

    return {
        "team_name": team_name,
        "fbref_link": fbref_url
    }
