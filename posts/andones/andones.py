import argparse
import pandas as pd
import requests
import base64
import configparser

import utils.plays as plays
import utils.checks as checks
import utils.plotting as plotting
import utils.games as games

def main(**kwargs):

    if kwargs['team']:
        pickteam = checks.check_team(kwargs.get('team'))
    else:
        pickteam = checks.check_team('')

    if kwargs['games']:
        numberofgames = checks.check_games(int(kwargs.get('games')))
    else:
        numberofgames = checks.check_games(0)

    verbose = kwargs.get('verbose')

    # let's be secure and keep authorization details secret.
    APIKEYS = configparser.ConfigParser()
    APIKEYS.read('./APIKeys.ini');

    # Get the keyname (client_id?) and actual API key.
    usern = APIKEYS['mysportsfeeds']['usern']
    passw = APIKEYS['mysportsfeeds']['passw']

    # Use API to get 
    team_urls = games.get_schedule(pickteam, numberofgames, verbose, usern, passw)

    # Now let's loop over the entire season and pick up all of the And-1s from the year.
    and_one_season = pd.DataFrame()

    # Loop over games... the number of games parameter is chosen above.
    for i in range(numberofgames):
        team_games =  requests.get(
                    url=team_urls['gameURL'][i],
                    headers={"Authorization": "Basic " + base64.b64encode('{}:{}'.format(usern,passw).encode('utf-8')).decode('ascii')}
                    )

        if verbose:
            if team_games.status_code != 200:
                print('API Error')

        print('.', end='')

        # These are the and-one plays from this game.
        and_one_plays = plays.get_and_ones(team_games.json(), pickteam)
        and_one_plays['gameno'] = i

        # Append after each game to make a season-long dataset.
        and_one_season = and_one_season.append(and_one_plays, ignore_index=True)

    # Now, let's identify these players.
    players = games.get_players(pickteam, verbose, usern, passw)

    # Let's merge on the season data:
    andoneplayer = and_one_season.merge(players, left_on='shooter_ID', right_on='ID')

    # How many And-ones?
    howmany = andoneplayer.groupby(['ID','lastname','jersey']).size().reset_index(name="andones")
    howmany = howmany.sort_values(by='andones',ascending=False)

    # We concatenate the player name with how many and-ones (for the legend).
    for i in range(howmany.shape[0]):
        howmany.loc[i,'last2'] = howmany['lastname'][i] + "   (" + str(howmany['andones'][i]) + ")"
        
    # Merge (back) together.
    andoneplayer = andoneplayer.merge(howmany, on=['ID'])

    plotting.plot_results(pickteam, andoneplayer, numberofgames)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--team', help="pick team from standard NBA abbreviations")
    parser.add_argument('--verbose', action='store_true', help="return API statuses")
    parser.add_argument('--season', action='store_true', help="run entire season")
    parser.add_argument('--games', type=int, help="pick number of games (from start of season)")
    args = parser.parse_args()

    main(**vars(args))