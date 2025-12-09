from extract import get_league_teams
import pytest


def test_get_league_teams_invalid_url():
    url = "https://fbref.com/en/comps/999/Non-Existent-League-Stats"
    league_name = "Non Existent League"
    with pytest.raises(Exception):
        get_league_teams(url, league_name)
