import pytest
from requests.exceptions import HTTPError
from extract import extract_top_five_leagues


def test_extract_top_five_leagues_invalid_url():
    url = "https://fbref.com/en/invalidpage"
    leagues = extract_top_five_leagues(url)
    assert leagues == []


def test_extract_top_five_leagues_no_leagues_section():
    url = "https://fbref.com/en/somepagewithoutleaguesection"
    leagues = extract_top_five_leagues(url)
    assert leagues == []


def test_extract_top_five_leagues_success():
    url = "https://fbref.com/en/"
    leagues = extract_top_five_leagues(url)
    assert isinstance(leagues, list)
    assert len(leagues) <= 5  # Should return at most 5 leagues
    for league in leagues:
        assert "league_name" in league
        assert "fbref_url" in league
        assert "league_country" in league
        assert "league_season" in league


def test_extract_top_five_leagues_correct_leagues():
    leagues = ["Premier League", "La Liga",
               "Bundesliga", "Serie A", "Ligue 1"]
    url = "https://fbref.com/en/"
    extracted_leagues = extract_top_five_leagues(url)
    for league in extracted_leagues:
        assert any(correct_league in league["league_name"]
                   for correct_league in leagues)
