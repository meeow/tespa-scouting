import os, time, re, requests, math
import pandas as pd
import numpy as np
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
from urllib.parse import quote
from urllib.request import urlopen  
from twisted.internet import reactor, defer
from requests_futures.sessions import FuturesSession
from tespa_leaderboard_spider import CollectLeaderboard
from tespa_team_spider import CollectTeams


def get_btag(id):
    df = pd.read_csv('db/id_btag_map.csv')
    print(df)
    if id in df['discord_id'].values.tolist():
        btag = df.loc[df['discord_id'] == id]['btag'].values.tolist()
        print(btag)
        return btag
    else:
        return None

def store_btag(id, btag):
    f = open('db/id_btag_map.csv', 'a')
    f.write('\n'+id+','+btag[0])

# Btag scraper
def parse_re(reg, rawhtml):
    matchObj = re.search(reg, rawhtml)
    if matchObj == None: 
        #print ("Failed to match", reg)
        return np.nan
    elif matchObj.group(1).isdigit():
        return int(matchObj.group(1))
    else:
        return str(matchObj.group(1))

def collect_single_sr(btag):
    print("Parsing", btag)
    re_sr = r'u-align-center h5">(\d{3,4})<'    
    url_prefix = 'https://playoverwatch.com/en-us/career/pc/'
    url = url_prefix + quote(btag)

    try:
        rawhtml = urlopen(url).read().decode('utf-8')
    except:
        print ("[ERROR] Failed to connect to playoverwatch")
        return None

    time.sleep(0.10) # add delay between requests
    return parse_re(re_sr, rawhtml)

def session_get(url):
    s = requests.session()
    s.keep_alive = False

    ret = s.get(url).result().text[241600:241900]
    return ret

def collect_sr(btags):
    print ("Collecting SR of", ', '.join(btags))

    btags = [btag.replace('#', '-') for btag in btags]
    session = FuturesSession()
    re_sr = r'u-align-center h5">(\d{3,4})<'  
    #re_sr = r'>(\d{3,4})</div>'
    url_prefix = 'http://playoverwatch.com/en-us/career/pc/'

    btag_urls = [url_prefix + quote(btag) for btag in btags]
    btag_htmls = [session.get(url).result().text for url in btag_urls]
    btag_srs = [(btags[i], parse_re(re_sr, btag_htmls[i])) for i in range(len(btags))]

    return btag_srs

def collect_team_sr(team_name, top=9):
    df_btags = pd.read_csv('./db/tespa_teams.csv')
    
    target = df_btags['team_name'] == team_name
    target = df_btags[target][['btag']]

    btags = list(target['btag'])
    combined = collect_sr(btags)
    avg_sr = np.mean([s[1] for s in combined if s[1] if not math.isnan(s[1])][:top])
    if avg_sr == np.nan:
        avg_sr = "Not found."

    print ("Top {} SR:".format(top), avg_sr)
    return avg_sr, combined

def rm(fp):
    try:
        os.remove(fp)
    except:
        print("Failed to remove", fp)

def update_db():
    teams_path = './db/tespa_teams.csv'
    leaderboard_path = './db/tespa_leaderboard.csv'

    def destroy_old_db():
        rm(teams_path)
        rm(leaderboard_path)

    def normalize_leaderboard():
        df_leaderboard = pd.read_csv(leaderboard_path) 
        df_leaderboard['team_name'] = df_leaderboard['team_name'].apply(lambda x: x[x.find('] ') + 2:])
        rm(leaderboard_path)
        df_leaderboard.to_csv(leaderboard_path)

    def normalize_teams():
        df_raw = pd.read_csv(teams_path) 
        df_raw['btag'] = df_raw['btag'].str.split(',')
        s = df_raw.apply(lambda x: pd.Series(x['btag']),axis=1).stack().reset_index(level=1, drop=True)
        s.name = 'btag'
        df_btags = df_raw.drop('btag', axis=1).join(s).reset_index(drop=True)
        df_btags = df_btags[['btag', 'team_name']]
        rm(teams_path)
        df_btags.to_csv(teams_path)

    destroy_old_db()
    runner = CrawlerRunner()
    runner.crawl(CollectLeaderboard)
    runner.crawl(CollectTeams)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    print("Running crawlers...")
    reactor.run(0)
    print("Crawlers finished.")

    normalize_leaderboard()
    normalize_teams()
    print("DB refresh success.")

def get_teams():
    fp = './db/tespa_teams.csv'
    try:
        return pd.read_csv(fp)
    except:
        update_db()


def get_leaderboard():
    fp = './db/tespa_leaderboard.csv'
    try:
        return pd.read_csv(fp)
    except:
        update_db()

def get_from_leaderboard(team_name, column_name='rank'):
    leaderboard_path = './db/tespa_leaderboard.csv'
    df = pd.read_csv(leaderboard_path)
    row = df.loc[df['team_name'] == team_name]
    return row[column_name].values[0]


