import pandas as pd


def convert_leagues_to_dataframe(leagues: list[dict]) -> pd.DataFrame:
    """Convert a list of league dictionaries to a pandas DataFrame."""
    return pd.DataFrame(leagues)


def transform_league_name(league_name: str) -> str:
    """Transform league name to a standardized format."""
    league_name = league_name.replace("Table", "")
    return league_name.strip().title()
