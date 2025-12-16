import pytest
from transform import (validate_league_name, validate_fbref_url,
                       validate_league_country, validate_league_season, transform_league_data)


def test_validate_league_name():
    assert validate_league_name("Premier League Table") == "Premier League"
    assert validate_league_name("  la liga  ") == "La Liga"
    with pytest.raises(ValueError):
        validate_league_name("")
    with pytest.raises(ValueError):
        validate_league_name(123)


def test_validate_fbref_url():
    assert validate_fbref_url(
        "/en/comps/9/Premier-League-Stats") == "https://fbref.com/en/comps/9/Premier-League-Stats"
    assert validate_fbref_url(
        " https://fbref.com/en/comps/10/La-Liga-Stats ") == "https://fbref.com/en/comps/10/La-Liga-Stats"
    with pytest.raises(ValueError):
        validate_fbref_url("")
    with pytest.raises(ValueError):
        validate_fbref_url(456)


def test_validate_league_country():
    assert validate_league_country(" england ") == "England"
    assert validate_league_country("SPAIN") == "Spain"
    with pytest.raises(ValueError):
        validate_league_country("")
    with pytest.raises(ValueError):
        validate_league_country(789)


def test_validate_league_season():
    assert validate_league_season(" 2022-2023 ") == "2022-2023"
    assert validate_league_season("2021-2022") == "2021-2022"
    with pytest.raises(ValueError):
        validate_league_season("")
    with pytest.raises(ValueError):
        validate_league_season(1011)


def test_transform_league_data():
    raw_data = {
        "league_name": " premier league table ",
        "fbref_url": "/en/comps/9/Premier-League-Stats",
        "league_country": " england ",
        "league_season": " 2022-2023 "
    }
    transformed = transform_league_data(raw_data)
    assert transformed == {
        "league_name": "Premier League",
        "fbref_url": "https://fbref.com/en/comps/9/Premier-League-Stats",
        "league_country": "England",
        "league_season": "2022-2023"
    }
