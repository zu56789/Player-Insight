from datetime import date
from transform import transform_player_dob, transform_player_details
import pytest


def test_invalid_player_dob():
    dob_str = "sfdsdffsfs"
    with pytest.raises(ValueError):
        transform_player_dob(dob_str)


def test_transform_player_details():
    player = {'player_name': 'Dario Essugo  ', 'player_position': ' MF', 'player_nationality': 'Portugal ', 'player_dob': '2005-03-14',
              'player_height': 'Unknown', 'player_strong_foot': 'Unknown',
              'team_name': 'Chelsea', 'fbref_url': 'https://fbref.com/en/players/1e4319ac/Dario-Essugo'}
    assert transform_player_details(player) == {'player_name': 'Dario Essugo', 'player_position': 'MF',
                                                'player_nationality': 'Portugal', 'player_dob': date(
                                                    2005, 3, 14), 'player_height': 'Unknown',
                                                'player_strong_foot': 'Unknown', 'team_name': 'Chelsea',
                                                'fbref_url': 'https://fbref.com/en/players/1e4319ac/Dario-Essugo'}
