def validate_league_name(league_name: str) -> str:
    """Transform league name to a standardized format."""
    if not isinstance(league_name, str):
        raise ValueError("League name must be a string.")
    if len(league_name) == 0:
        raise ValueError("League name cannot be empty.")
    league_name = league_name.replace("Table", "")
    return league_name.strip().title()


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


def validate_league_country(league_country: str) -> str:
    """Standardize league country names."""
    if not isinstance(league_country, str):
        raise ValueError("League country must be a string.")
    if len(league_country) == 0:
        raise ValueError("League country cannot be empty.")
    return league_country.strip().title()


def validate_league_season(league_season: str) -> str:
    """Standardize league season format."""
    if not isinstance(league_season, str):
        raise ValueError("League season must be a string.")
    if len(league_season) == 0:
        raise ValueError("League season cannot be empty.")
    return league_season.strip()


def transform_league_data(league_data: dict) -> dict:
    """Transform and validate league data dictionary."""
    league_name = validate_league_name(league_data.get("league_name", ""))
    fbref_url = validate_fbref_url(league_data.get("fbref_url", ""))
    league_country = validate_league_country(
        league_data.get("league_country", ""))
    league_season = validate_league_season(
        league_data.get("league_season", ""))

    return {
        "league_name": league_name,
        "fbref_url": fbref_url,
        "league_country": league_country,
        "league_season": league_season
    }
