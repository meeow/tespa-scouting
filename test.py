import pandas as pd
from requests_futures.sessions import FuturesSession
from urllib.parse import quote



def normalize_teams():
    teams_path = './db/tespa_teams.csv'
    
    leaderboard_path = './db/tespa_leaderboard.csv'
    df_raw = pd.read_csv(leaderboard_path) 
    print(df_raw)
    df_raw['btag'] = df_raw['btag'].str.split(',')
    s = df_raw.apply(lambda x: pd.Series(x['btag']),axis=1).stack().reset_index(level=1, drop=True)
    s.name = 'btag'
    df_btags = df_raw.drop('btag', axis=1).join(s).reset_index(drop=True)
    df_btags = df_btags[['btag', 'team_name']]
    rm(leaderboard_path)
    df_btags.to_csv(leaderboard_path)
    print ('done')

def get_from_leaderboard(team_name, column_name='rank'):
    leaderboard_path = './db/tespa_leaderboard.csv'
    df = pd.read_csv(leaderboard_path)
    row = df.loc[df['team_name'] == team_name]
    print(row[column_name].values[0])
    return row[column_name].values[0]


re_sr = r'u-align-center h5">(\d{3,4})<'    


def collect_html(btags):
    session = FuturesSession()

    url_prefix = 'http://playoverwatch.com/en-us/career/pc/'
    btag_urls = [url_prefix + quote(btag) for btag in btags]
    btag_htmls = [session.get(url).result().text[241780:241850] for url in btag_urls]

    return btag_htmls[0].find('u-align-center h5">3685<')

    #return btag_htmls

print ( collect_html(['Bato-11908']*1) )



