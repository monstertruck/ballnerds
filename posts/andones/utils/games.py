import pandas as pd
import requests
import base64

def get_schedule(pickteam: str, numberofgames: int, verbose: bool, usern: str, passw: str) -> pd.DataFrame:
    '''
    Given a 'pickteam' code, we can use the mysportsfeeds API to get their schedule.
    '''

    team_url = "https://api.mysportsfeeds.com/v1.1/pull/nba/2018-2019-regular/team_gamelogs.json?team={}".format(pickteam)
        
    team_raw =  requests.get(
                url=team_url,
                headers={"Authorization": "Basic " + base64.b64encode('{}:{}'.format(usern,passw).encode('utf-8')).decode('ascii')}
                )

    if verbose:
        print(team_raw.status_code)

    # Convert to JSON
    team_js = team_raw.json()

    # Now we have the schedule.
    team_sked = pd.DataFrame(team_js['teamgamelogs']['gamelogs'])

    # Loop over the games and get the correct ID (YYYYMMDD-AWAY-HOME)
    for i in range(min(numberofgames,82)):
        team_sked.loc[i,'away'] = team_sked['game'][i]['awayTeam']['Abbreviation']
        team_sked.loc[i,'home'] = team_sked['game'][i]['homeTeam']['Abbreviation']
        team_sked.loc[i,'gamedate'] = team_sked['game'][i]['date'].replace("-","")

    # Make it easier to read!
    team_sked = team_sked.assign( gameid = team_sked['gamedate'] + "-" + team_sked['away'] + "-" + team_sked['home'])
    team_sked = team_sked.drop(['game','stats','team'],1)
    team_sked = team_sked.drop(['away','home','gamedate'],1)

    # let's make a dataframe of the identifiers.
    return team_sked.assign( gameURL = "https://api.mysportsfeeds.com/v1.1/pull/nba/2018-2019-regular/game_playbyplay.json?gameid=" + team_sked['gameid'] )



def get_players(pickteam: str, verbose: bool, usern: str, passw: str) -> pd.DataFrame:
    '''
    Given a pickteam code, we can get the players that played for that team during that year.
    '''

    # player URL
    player_url = "https://api.mysportsfeeds.com/v1.1/pull/nba/2018-2019-regular/cumulative_player_stats.JSON?playerstats=2PA,2PM,3PA,3PM,FTA,FTM"

    # You can pass a parameter with the teamname.
    team_player =  requests.get(
                    url=player_url,
                    params = {"team": pickteam},
                    headers={"Authorization": "Basic " + base64.b64encode('{}:{}'.format(usern,passw).encode('utf-8')).decode('ascii')}
                )

    if verbose:
        print(team_player.status_code)

    # Construct the dataframes!
    team_player = team_player.json()
    team_player = pd.DataFrame(team_player['cumulativeplayerstats']['playerstatsentry'])
    players = pd.DataFrame(team_player['player'])
    # playerstats = pd.DataFrame(team_player['stats'])

    # Loop through player characteristics and build a dataframe.
    for i in range(players.shape[0]): 
        try:
            players.loc[i,'jersey'] = players['player'][i]['JerseyNumber']
        except:
            # A couple players have no jersey numbers?
            players.loc[i,'jersey'] = -1
        players.loc[i,'position'] = players['player'][i]['Position']
        players.loc[i,'ID'] = int(players['player'][i]['ID'])
        players.loc[i,'lastname'] = players['player'][i]['LastName']

    # Make it neater
    return players.drop(['player'],1)