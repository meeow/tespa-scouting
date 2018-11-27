
password = "secret"

digits = {
    '1': r'(1|[oO]ne)',
    '2': r'(2|[tT]wo)',
    '3': r'(3|[tT]hree)',
    '4': r'(4|[fF]our)',
    '5': r'(5|[fF]ive)',
    '6': r'(6|[sS]ix)',
    '7': r'(7|[sS]even)',
    '8': r'(8|[eE]ight)',
    '9': r'(9|[nN]ine)'
}

entities = {
    # team_name added in controller.py
    'battletag': r'([^ ]+#\d{4,5})',
    'confirm': r'([yY]es|[yY]eah|[sS]ure|[cC]onfirm|[yY]up)',
    'average': r'([aA]vg|[aA]verage|[mM]ean)',
    'player': r'([pP]layer|[mM]ember)',
    'leaderboard': r'([lL]eaderboard|[tT]eam)',
}

intents = {
    'players': r'([pP]layers)',
    'my': r'([mM]y\s)',
    'skill_rating': r'([sS][rR][\s\b]|[sS][rR]$|[sS]kill [rR]ating|[eE]lo\s)',
    'update_db': r'([rR]efresh|[uU]pdate|[lL]atest|[nN]ewest)',
    'help': r'([hH]elp|[aA]ssist|[wW]\D+\ can [uyU]\D*)',
    'greeting': r'([hH]i\b|[hH]ello\b|[hH]ey\b|[sS]up\b)',
    'top': r'([bB]est\s|[tT]op\s|[hH]ighest\s)',
    'rank': r'([rR]ank|[pP]osition)',
    'rating': r'([lL]eaderboard [rR]ating)',
}

helps = {
    'default_help': [
        '''Hi 🐱 I can help you do some Overwatch-y stuff like lookup a player's SR or even
 an entire Tespa team's average (or top [n]) SR! Additionally, I can find out the leaderboard 
 rank and rating of a particular team. Lastly, if you feel like my data is old (team not found
 but should be, or leaderboard rating is old), tell me to fetch new data!
 Sometimes I take a while to process your request because my creator made me slow and dumb,
 so don't always expect instant results.'''.replace('\n','')
    ],
    'compact_help': [
        '''Hint: I can lookup team (top, avg) or battletag SR, team leaderboard rating, or update database (admin). For more detailed help, ask for help.'''
    ]
}

errs = {
    'default_err': [
        "Sorry, I can't do this right now...",
        "I don't know the answer right now.",
        "Something went wrong :(. Maybe you can do a better job searching for the answer than me.",
        "I broke. Maybe my creator will fix me one day :,(",
        "I can't do that now, sorry...talk to my creator, maybe he can repair me..."
    ],
    'sr_lookup_player':[
        "Sorry, I couldn't find the information of {} ;-; Is the profile hidden??\n",
        "Are you sure {} has a public profile? I can't find the SR...\n"
    ],
    "sr_lookup_team": [
        "Sorry, I couldn't find the information of {} ;-;",
        "I think you specified a team called {} but I couldn't find data on it :/"
    ],
    "personal_sr_lookup": [
        "Sorry, I couldn't find a battletag associated with {}.\n"
    ]

}

warns = {
    "player_not_found": [

    ],
    "runtime": [
        "Sit back and relax for a minute because I'm dumb and scrape sequentially :("
    ]
}

requests = {
    'no_entity': [
        "Could you tell me a bit more? You said something about {}, but a valid team name or battletag might help :)",
        "I think you want me to do something involving {}, but I'm missing some necessary information...maybe a valid battletag or team name??"
    ],
    'no_intent': [
        "You told me about {} but I don't know what to do! >.< (maybe try looking up the SR?)",
        "What am I supposed to do with {}?? (maybe try looking up the SR?)"
    ],
    'no_intent_or_entity': [
        "My creator made me too dumb to understand what you just said ;-;",
        "I don't get it...",
        "Huh?",
        "U wot m8",
        "I wish I had basic social skills but my creator didn't give me any :("
    ]
}

statuses = {
    "confirm_runtime": [
        "It would take a while for me to do this...are you sure you want to continue?"
    ],
    "updated_database": [
        "I'm done updating my database!",
        "All done!~",
        "My data is fresh now =]"
    ]
}

