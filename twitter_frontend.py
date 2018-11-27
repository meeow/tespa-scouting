from credentials import consumer_key, consumer_secret, access_token, access_token_secret
from controller import get_reply, get_general_error
import tweepy, traceback

# Authenticate
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Twitter listener
class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print("Received tweet:", status.text)
        try:
            reply = get_reply(status_to_conversation(status))
        except Exception as e:
            print ("Error when replying to tweet: {}".format(status.text), '\n', traceback.format_exc())
            reply = get_general_error()
        send_reply(status, reply)

user = api.me()
myStream = tweepy.Stream(auth=api.auth, listener=StreamListener())
myStream.filter(track=['@'+user.screen_name], async=True)

def send_reply(status, msg):
    print ("Sending reply:", msg)
    tweet_length = 270 - len(status.author.screen_name)
    tweets = [msg[i:i+tweet_length] for i in range(0, len(msg), tweet_length)]
    tweets.reverse()
    prefix = '@{}\n'.format(status.author.screen_name)
    for tweet in tweets:
        api.update_status(prefix + tweet, status.id)

def status_to_conversation(status):
    conversation = '\n > ' + status.text

    parent_id = status.in_reply_to_status_id
    has_previous = False
    while parent_id and not has_previous:
        #print(parent_id)
        status = api.get_status(parent_id)
        parent_id = status.in_reply_to_status_id
        if user.screen_name in status.text:
            conversation += '\n > ' + status.text
            has_previous = True

    print("Conversation:", conversation)
    return conversation

# Debug
print ("Authenticated as:", user.name)
print ("Listening for keyword:", '@'+user.screen_name)

