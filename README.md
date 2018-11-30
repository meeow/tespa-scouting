# Files in this project:

## twitter_frontend.py
    - no longer supported

## discord_frontend.py 
    - interfaces with discord.py rewrite api
    - listens for a specific prefix in servers the bot is invited to and forwards messages to controller.py
    - posts responses from controller.py to discord 

## controller.py
    - extracts intents and entities from message chain (conversation)
    - performs an action depending on extracted intents and entities
        - if this involves db lookup or web scraping, it is handled by model.py
    - returns a message to frontend

## texts.py
    - regexps and error/prompt messages are stored here

## model.py
    - interfaces with "databases" (csv files which are loaded into pandas dataframes)
        - update databases with fresh scrapes if user requests fresh data
    - scrapes overwatch player info website for skill rating if requested

## tespa_leaderboard_spider.py
    - scrapes leaderboard of fall 2018 overwatch league

## tespa_team_spider.py
    - scrapes players participating in fall 2018 overwatch league and the team they are on 

## db/tespa_leaderboard.csv
    - contains tespa teams and their leaderboard rating

## db/tespa_teams.csv
    - contains players' battletags and the team they are on

## db/id_btag_map.csv
    - stores players' battletags associated with the discord name or twitter handle

## credentials.py
    - put your bot's Oauth credentials here