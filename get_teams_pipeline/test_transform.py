import pytest
from transform import (validate_team_name, validate_fbref_url,
                       transform_team_data)


def test_validate_team_name():
    assert validate_team_name(" Manchester United ") == "Manchester United"
    assert validate_team_name("real madrid") == "Real Madrid"
    with pytest.raises(ValueError):
        validate_team_name("")
    with pytest.raises(ValueError):
        validate_team_name(123)


def test_validate_fbref_url():
    assert validate_fbref_url(
        "/en/squads/19538871/Manchester-United-Stats") == "https://fbref.com/en/squads/19538871/Manchester-United-Stats"
    assert validate_fbref_url(
        " https://fbref.com/en/squads/86/Real-Madrid-Stats ") == "https://fbref.com/en/squads/86/Real-Madrid-Stats"
    with pytest.raises(ValueError):
        validate_fbref_url("")
    with pytest.raises(ValueError):
        validate_fbref_url(456)


def test_transform_team_data():
    raw_data = {
        "team_name": " manchester united ",
        "fbref_link": "/en/squads/19538871/Manchester-United-Stats"
    }
    transformed = transform_team_data(raw_data)
    assert transformed == {
        "team_name": "Manchester United",
        "fbref_link": "https://fbref.com/en/squads/19538871/Manchester-United-Stats"
    }
