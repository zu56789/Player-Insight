from extract import get_league_teams
import pytest


def test_get_league_teams_invalid_url():
    url = "https://fbref.com/en/comps/999/Non-Existent-League-Stats"
    league_name = "Non Existent League"
    with pytest.raises(Exception):
        get_league_teams(url, league_name)


def test_get_league_teams_empty_inputs():
    with pytest.raises(ValueError):
        get_league_teams("", "")


def test_get_league_teams_valid():
    url = "https://fbref.com/en/comps/13/2025-2026-Ligue-1-Stats"
    league_name = "Ligue 1"
    teams = get_league_teams(url, league_name)
    assert isinstance(teams, dict)
    assert len(teams) > 0
    assert "Metz" in teams
    assert teams["Metz"] == "https://fbref.com/en/squads/f83960ae/Metz-Stats"


def test_get_league_teams_no_table():
    url = "https://fbref.com/en/comps/13/2025-2026-Ligue-1-Stats"
    league_name = "Non Existent League"
    with pytest.raises(AttributeError):
        get_league_teams(url, league_name)
