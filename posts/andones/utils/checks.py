import random

def check_team(team: str) -> str:
    '''
    Since we are making calls to an external API, we want to make sure all of our
    team calls are for teams that actually exist.
    '''

    if team == 'OKC':
        print('For our purposes, OKC is OKL.')
        team = 'OKL'
    if team == 'BKN':
        print('For our purposes, BKN is BRO.')
        team = 'BRO'

    team_abbrevs = ['ATL', 'BOS', 'BRO', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW',  
                'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK',  
                'OKL', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']

    if team not in team_abbrevs:
        print('Team not in list... picking one at random for you... ', end='')
        team = random.choice(team_abbrevs)
        print('that team is ' + team)
        return team
    else:
        return team


def check_games(numberofgames: int) -> int:
    '''
    Regular seasons usually have 82 games, so we check to make sure
    that you pick 0 < numberofgames <= 82.
    '''

    if (0 < numberofgames <= 82):
        return numberofgames
    else:
        print('Not a valid number of games... we will look at the whole season.')
        return 82