# test_basics.py

import pytest

from utils.plays import process_fg_att
from utils.plays import process_ft_att
from utils.plays import process_foul


def test_process_foul():

    play1 = {'quarter': '1',
            'time': '0:15',
            'foul': {'teamAbbreviation': 'DET',
                'penalizedPlayer': {'ID': '13740',
                'LastName': 'Kennard',
                'FirstName': 'Luke',
                'JerseyNumber': '5',
                'Position': 'SG'},
            'drawnByPlayer': {'ID': '9659',
                'LastName': 'Levert',
                'FirstName': 'Caris',
                'JerseyNumber': '22',
                'Position': 'SG'},
            'foulType': 'L.B.FOUL',
            'isPersonal': 'true',
            'isTechnical': 'false',
            'isFlagrant1': 'false',
            'isFlagrant2': 'false',
            'foulLocation': {'x': '683', 'y': '451'}}}
    
    foul1 = {'teamAbbreviation': 'DET',
                'penalizedPlayer': {'ID': '13740',
                'LastName': 'Kennard',
                'FirstName': 'Luke',
                'JerseyNumber': '5',
                'Position': 'SG'},
            'drawnByPlayer': {'ID': '9659',
                'LastName': 'Levert',
                'FirstName': 'Caris',
                'JerseyNumber': '22',
                'Position': 'SG'},
            'foulType': 'L.B.FOUL',
            'isPersonal': 'true',
            'isTechnical': 'false',
            'isFlagrant1': 'false',
            'isFlagrant2': 'false',
            'foulLocation': {'x': '683', 'y': '451'}}

    result1 = {'quarter': '1',
            'time': '0:15',
            'foul': {'teamAbbreviation': 'DET',
            'penalizedPlayer': {'ID': '13740',
            'LastName': 'Kennard',
            'FirstName': 'Luke',
            'JerseyNumber': '5',
            'Position': 'SG'},
            'drawnByPlayer': {'ID': '9659',
            'LastName': 'Levert',
            'FirstName': 'Caris',
            'JerseyNumber': '22',
            'Position': 'SG'},
            'foulType': 'L.B.FOUL',
            'isPersonal': 'true',
            'isTechnical': 'false',
            'isFlagrant1': 'false',
            'isFlagrant2': 'false',
            'foulLocation': {'x': '683', 'y': '451'}},
            'fl_fouling_team': 'DET',
            'fl_type': 0,
            'fouled_ID': '9659',
            'fouled_LastName': 'Levert',
            'fouled_FirstName': 'Caris',
            'fouled_JerseyNumber': '22',
            'fouled_Position': 'SG',
            'fouler_ID': '13740',
            'fouler_LastName': 'Kennard',
            'fouler_FirstName': 'Luke',
            'fouler_JerseyNumber': '5',
            'fouler_Position': 'SG',
            'fl_loc_x_original': 683,
            'fl_loc_y_original': 451}

    assert process_foul(play1, foul1) == result1



def test_process_fg_att():

    play1 = {'quarter': '1',
        'time': '0:32',
        'fieldGoalAttempt': {'teamAbbreviation': 'BRO',
        'shootingPlayer': {'ID': '13749',
        'LastName': 'Allen',
        'FirstName': 'Jarrett',
        'JerseyNumber': '31',
        'Position': 'C'},
        'assistingPlayer': {'ID': '9285',
        'LastName': 'Russell',
        'FirstName': "D'Angelo",
        'JerseyNumber': '1',
        'Position': 'SG'},
        'shotType': 'Dunk',
        'distanceFeet': '0',
        'Points': '2',
        'shotLocation': {'x': '887', 'y': '255'},
        'outcome': 'SCORED'}}

    shot1 = {'teamAbbreviation': 'BRO',
        'shootingPlayer': {'ID': '13749',
        'LastName': 'Allen',
        'FirstName': 'Jarrett',
        'JerseyNumber': '31',
        'Position': 'C'},
        'assistingPlayer': {'ID': '9285',
        'LastName': 'Russell',
        'FirstName': "D'Angelo",
        'JerseyNumber': '1',
        'Position': 'SG'},
        'shotType': 'Dunk',
        'distanceFeet': '0',
        'Points': '2',
        'shotLocation': {'x': '887', 'y': '255'},
        'outcome': 'SCORED'}

    result1 = {'quarter': '1',
        'time': '0:32',
        'fieldGoalAttempt': {'teamAbbreviation': 'BRO',
        'shootingPlayer': {'ID': '13749',
        'LastName': 'Allen',
        'FirstName': 'Jarrett',
        'JerseyNumber': '31',
        'Position': 'C'},
        'assistingPlayer': {'ID': '9285',
        'LastName': 'Russell',
        'FirstName': "D'Angelo",
        'JerseyNumber': '1',
        'Position': 'SG'},
        'shotType': 'Dunk',
        'distanceFeet': '0',
        'Points': '2',
        'shotLocation': {'x': '887', 'y': '255'},
        'outcome': 'SCORED'},
        'fg_val': '2',
        'fg_made': 1,
        'fg_type': 'Dunk',
        'fg_loc_x_original': 887,
        'fg_loc_y_original': 255,
        'fg_loc_x': -417,
        'fg_loc_y': 5,
        'fg_team': 1,
        'shooter_ID': '13749',
        'shooter_LastName': 'Allen',
        'shooter_FirstName': 'Jarrett',
        'shooter_JerseyNumber': '31',
        'shooter_Position': 'C'}


    assert process_fg_att(play1, shot1, 'BRO') == result1


def test_process_ft_att():

    play1 = {'quarter': '1',
        'time': '3:57',
        'freeThrowAttempt': {'teamAbbreviation': 'BRO',
        'shootingPlayer': {'ID': '9528',
        'LastName': 'Dudley',
        'FirstName': 'Jared',
        'JerseyNumber': '3',
        'Position': 'SF'},
        'attemptNum': '1',
        'totalAttempts': '2',
        'outcome': 'MISSED'}}


    shot1 = {'teamAbbreviation': 'BRO',
        'shootingPlayer': {'ID': '9528',
        'LastName': 'Dudley',
        'FirstName': 'Jared',
        'JerseyNumber': '3',
        'Position': 'SF'},
        'attemptNum': '1',
        'totalAttempts': '2',
        'outcome': 'MISSED'}

    result1 = {'quarter': '1',
        'time': '3:57',
        'freeThrowAttempt': {'teamAbbreviation': 'BRO',
        'shootingPlayer': {'ID': '9528',
        'LastName': 'Dudley',
        'FirstName': 'Jared',
        'JerseyNumber': '3',
        'Position': 'SF'},
        'attemptNum': '1',
        'totalAttempts': '2',
        'outcome': 'MISSED'},
        'ft_att': '2',
        'ft_made': 0,
        'ft_team': 1,
        'ft_shooter_ID': '9528',
        'ft_shooter_LastName': 'Dudley',
        'ft_shooter_FirstName': 'Jared',
        'ft_shooter_JerseyNumber': '3',
        'ft_shooter_Position': 'SF'}


    assert process_ft_att(play1, shot1, 'BRO') == result1