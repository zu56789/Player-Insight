from extract import get_league_teams
import pytest


def test_get_league_teams_invalid_url():
    url = "https://fbref.com/en/comps/999/Non-Existent-League-Stats"
    with pytest.raises(ValueError):
        get_league_teams(url)


def test_get_league_teams_empty_inputs():
    with pytest.raises(ValueError):
        get_league_teams("")


def test_get_league_teams_valid():
    url = "https://fbref.com/en/comps/13/2025-2026-Ligue-1-Stats"
    teams = get_league_teams(url)
    assert isinstance(teams, list)
    assert len(teams) > 0
    assert any(team["team_name"] == "Metz" for team in teams)
    assert any(team["fbref_url"] ==
               "https://fbref.com/en/squads/f83960ae/Metz-Stats" for team in teams)
