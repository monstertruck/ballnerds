import pandas as pd
import numpy as np

def get_and_ones(game_js: dict, pickteam: str) -> pd.DataFrame:
    '''
    For a given set of game_urls, return a dataframe with the collection of
    and-one plays during those games.
    '''

    # A game is a list of plays
    play_list = game_js['gameplaybyplay']['plays']['play']

    # Currently only interested in plays that are shots or fouls
    shot_or_foul = [play for play in play_list if (['fieldGoalAttempt', 'freeThrowAttempt', 'foul'] & play.keys())]

    # 'flattening' the dict format to import into dataframe
    for play in shot_or_foul:
        fg_att = play.pop('fieldGoalAttempt', None)
        if fg_att:
            play = process_fg_att(play, fg_att, pickteam)

        ft_att = play.pop('freeThrowAttempt', None)
        if ft_att:
            play = process_ft_att(play, ft_att, pickteam)

        foul = play.pop('foul', None)
        if foul:
            # technical fouls cause problems (since they can be assigned to bench)
            if foul['foulType'] == 'S.FOUL':
                play = process_foul(play, foul)

    play_df = pd.DataFrame(shot_or_foul)

    # Cast ID variables as floats (since they have NaNs) so we can use them in our groupby
    for id_var in [x for x in play_df.columns if 'ID' in x]:
        play_df[id_var] = play_df[id_var].astype(float)

    # Time is split into quarters - translate to one "seconds since beginning" measure
    time_split = play_df['time'].str.split(':')
    play_df['secs'] = (play_df['quarter'].astype(int) - 1)*720 + time_split.map(lambda x: x[0]).astype(int)*60 + time_split.map(lambda x: x[1]).astype(int)

    # collect and-one candidates
    plays_by_second = play_df.groupby('secs', as_index=False).sum()
    and_one_plays = plays_by_second.loc[(plays_by_second['fg_made'] == 1) & (plays_by_second['ft_made'] == 1) & (plays_by_second['fl_type'] == 1) ]

    and_one_plays = and_one_plays.assign( teammate = (and_one_plays['shooter_ID'] != and_one_plays['ft_shooter_ID']).astype(int))

    return and_one_plays



def process_fg_att(play: dict, fg_att: dict, pickteam: str) -> dict:
    '''
    Process the field goal attempts.
    '''

    play['fg_val'] = fg_att['Points']
    play['fg_made'] = int(fg_att['outcome'] == "SCORED")
    play['fg_type'] = fg_att['shotType']

    try:
        loc_x = int(fg_att['shotLocation']['x'])
        loc_y = int(fg_att['shotLocation']['y'])

        # we have to translate the coordinates to plot them correctly
        play['fg_loc_x_original'] = loc_x
        play['fg_loc_y_original'] = loc_y
        play['fg_loc_x'] = loc_x*(loc_x < 470) + (940 - loc_x)*(loc_x >= 470) - 470
        play['fg_loc_y'] = loc_y - 250
    except:
        # occastionally locations are nonsense
        play['fg_loc_x'] = np.NaN
        play['fg_loc_y'] = np.NaN

    if type(pickteam) is str:
        play['fg_team'] = int(fg_att['teamAbbreviation'].upper() == pickteam.upper())

    # get information on the shooter
    for key in fg_att['shootingPlayer']:
        play['shooter_' + key] = fg_att['shootingPlayer'][key]

    return play



def process_ft_att(play:dict, ft_att: dict, pickteam: str) -> dict:
    '''
    Process the plays that are free throw attempts.
    '''
    
    play['ft_att'] = ft_att['totalAttempts']
    play['ft_made'] = int(ft_att['outcome'] == "SCORED")

    if type(pickteam) is str:
        play['ft_team'] = int(ft_att['teamAbbreviation'].upper() == pickteam.upper())

    # get information on the shooter
    for key in ft_att['shootingPlayer']:
        play['ft_shooter_' + key] = ft_att['shootingPlayer'][key]

    return play



def process_foul(play: dict, foul: dict) -> dict:
    '''
    '''

    play['fl_fouling_team'] = foul['teamAbbreviation']
    play['fl_type'] = int(foul['foulType'] == 'S.FOUL')

    if foul['isPersonal'] == 'true':
        for key in foul['drawnByPlayer']:
            play['fouled_' + key] = foul['drawnByPlayer'][key]

    for key in foul['penalizedPlayer']:
        play['fouler_' + key] = foul['penalizedPlayer'][key]
        
    try:
        play['fl_loc_x_original'] = int(foul['foulLocation']['x'])
        play['fl_loc_y_original'] = int(foul['foulLocation']['y'])
    except:
        play['fl_loc_x'] = np.NaN
        play['fl_loc_y'] = np.NaN
    
    return play

