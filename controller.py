from model import * 
import tweepy, re, random, math, copy, discord, numpy as np

# Text processing logic
def get_reply(conversation):
    from texts import entities, intents, errs, requests, statuses, digits, helps, warns, password
    print ("Controller received text:", conversation)

    def check_for_team_name(all_teams):
        found_teams = []
        all_teams = set(all_teams)
        for team in all_teams:
            if team.lower() in conversation.lower():
                print ("Detected keyword(s)", team)
                found_teams += [team]
        for team in found_teams: #remove teams which are substrings of another team
            for team_2 in found_teams:
                if team == team_2: continue
                if team_2 in team:
                    found_teams.remove(team_2)
                    print ("Ignored", team, "for being a substring of intended search target.")
        return found_teams

    def extract_keywords(msg, regex):
        result = re.findall(regex, msg)
        if result: 
            print ("Detected keyword(s) {}".format(result))
        return result

    def map_to_command(entities, intents):
        response = discord.Embed()  
        intent_values = [_ for _ in intents.values() if _]
        entity_values = [_ for _ in entities.values() if _]
        digit_values = [_ for _ in digits.values() if _]

        entity_string = ', '.join([', '.join(l) for l in entity_values])
        intent_string = ', '.join([', '.join(l) for l in intent_values])

        # update db
        if intents['update_db']:
            if entities['confirm']:
                update_db()
                response.add_field(inline=0, name="Alert",value=random.choice(statuses['updated_database']))
            else:
                response.add_field(inline=0, name="Alert",value=random.choice(statuses['confirm_runtime']))
            return response

        # top of leaderboard
        if (entities['leaderboard'] and intents['top']):
            top = 1
            print(digit_values)
            if digit_values:
                top = int(digit_values[0][0])
            teams = get_leaderboard().sort_values(['rating'], ascending=0).head(int(top))[['team_name','rating']].values.tolist()
            description = ''
            for team in teams:
                team_name, rating = team[0], team[1]
                description += '{} - {} rating\n'.format(team_name, rating)
            response.add_field(inline=0, name='The top {} teams are: \n'.format(top), value=description)

        # leaderboard rating/ranking
        if (intents['rank'] or intents['rating'] and entities['team_name']):
            for team_name in entities['team_name']:
                rank = get_from_leaderboard(team_name, column_name='rank')
                rating = get_from_leaderboard(team_name, column_name='rating')
                if intents['rank']:
                    response.add_field(inline=0, name="Tespa Leaderboard", value="The leaderboard rank of {} is {}.\n".format(team_name, rank))
                if intents['rating']:
                    response.add_field(inline=0, name="Tespa Leaderboard", value="The leaderboard rating of {} is {}.\n".format(team_name, rating))

        # team or player SRs
        if intents['skill_rating'] or (intents['top'] and digit_values ):#and intents['players']):
            # team SR
            if entities['team_name']:
                players_sr = []
                for team_name in entities['team_name']:
                    if digit_values and not entities['average']:
                        top = digit_values[0]
                        top = int(list(digits.keys())[list(digits.values()).index(top)][0])
                        team_sr, players_sr = collect_team_sr(team_name, top=top)
                        response.add_field(inline=0, name="Top {} SR".format(top),value="The top {} SR of {} is {}.\n".format(top, team_name, team_sr) if team_sr else random.choice(errs['sr_lookup_team']).format(team_name))
                    else:
                        team_sr, players_sr = collect_team_sr(team_name)
                        response.add_field(inline=0, name="Average SR",value="\nThe average SR of {} is {}.\n".format(team_name, team_sr) if team_sr else random.choice(errs['sr_lookup_team']).format(team_name))
                    if players_sr:
                        title = "{}".format(team_name)
                        content = ''.join(["[{}]({}) - {} SR\n".format(p[0],"https://www.overbuff.com/players/pc/"+p[0], p[1]) if not math.isnan(p[1]) else "[{}]({}) - {}\n".format(p[0],"https://www.overbuff.com/players/pc/"+p[0], "Not Found.") for p in players_sr])
                        response.add_field(inline=0, name=title, value=content)
            # player SR
            if entities['battletag']:
                for btag in entities['battletag']:
                    print(btag)
                    sr = collect_single_sr(btag.replace('#','-'))
                    response.add_field(inline=0, name=btag, value="The SR of {} is {}.\n".format(btag, sr) if sr else random.choice(errs['sr_lookup_player']).format(btag))
            if not entity_values:
                response.add_field(inline=0, name='Error',value=random.choice(requests['no_entity']).format(intent_string))

        elif response.fields != []:
            print (response.fields)
            return response
        elif intents['help'] or intents['greeting']:
            response.add_field(inline=0, name='Help', value=random.choice(helps['default_help']))
        elif intent_values and not entity_values:
            response.add_field(inline=0, name='Error', value=random.choice(requests['no_entity']).format(intent_string))
        elif entity_values and not intent_values:
            response.add_field(inline=0, name='Error', value=random.choice(requests['no_intent']).format(entity_string))
        elif not entity_values and not intent_values:
            response.add_field(inline=0, name='Error', value=random.choice(requests['no_intent_or_entity']) + '\n')
            response.add_field(inline=0, name='Quick Help',value=random.choice(helps['compact_help']))

        return response

    digits = {k: extract_keywords(conversation, v) for k, v in digits.items()}
    entities = {k: extract_keywords(conversation, v) for k, v in entities.items()}
    intents = {k: extract_keywords(conversation, v) for k, v in intents.items()}

    #if not intents['update_db']:
    entities['team_name'] = check_for_team_name(get_teams()['team_name'])
    
    response = map_to_command(entities, intents)
    return response

def get_general_error():
    from texts import errs
    response = discord.Embed()  
    msg = random.choice(errs['default_err'])
    response.add_field(inline=0, name='Error',value=msg)
    return response



