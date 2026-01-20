from extract import get_team_players, get_player_details
import pytest


def test_get_team_players_empty_inputs():
    with pytest.raises(ValueError):
        get_team_players("", "")


def test_get_team_players_valid_input():
    url = "https://fbref.com/en/squads/cff3d9bb/Chelsea-Stats"
    team_name = "Chelsea"
    players = get_team_players(team_name, url)
    assert isinstance(players, list)
    assert len(players) > 0
    assert all(
        "player_name" in player and "fbref_url" in player and "team_name" in player for player in players)


def test_get_player_details_empty_url():
    with pytest.raises(ValueError):
        get_player_details("Player Name", "Team Name", "")


def test_get_player_details_valid_input():
    url = "https://fbref.com/en/players/2eda11b1/Estevao-Willian"
    team_name = "Chelsea"
    player_name = "Player Name"
    details = get_player_details(player_name, team_name, url)
    assert isinstance(details, dict)
    assert details["player_name"] == player_name
    assert details["team_name"] == team_name
    assert details["fbref_url"] == url
    assert "player_position" in details
