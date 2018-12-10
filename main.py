import time
from twitter import Twitter, OAuth
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from requests.sessions import Session
import os

try:
    from dev_values import *
except:
    pass

token = os.environ.get("TOKEN")
token_secret = os.environ.get("TOKEN_SECRET")
consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK")
TELEGRAM_WEBHOOK = os.environ.get("TELEGRAM_WEBHOOK")
TELEGRAM_CHATID = os.environ.get("TELEGRAM_CHATID")
tg_sendmessage = "{}/sendMessage".format(TELEGRAM_WEBHOOK)

t = Twitter(auth=OAuth(token, token_secret, consumer_key, consumer_secret))

s = Session()


def send_slack_msg(txt):
    if SLACK_WEBHOOK is not None:
        s.post(
            url=SLACK_WEBHOOK,
            json={
                "text": txt
            }
        )


def send_telegram_msg(txt):
    if TELEGRAM_WEBHOOK is not None:
        s.post(
            url=tg_sendmessage,
            json={'chat_id': TELEGRAM_CHATID, 'text': txt}
        )


class Listener(StreamListener):
    def on_data(self, data):
        msg = "https://twitter.com/_/status/{}".format(json.loads(data)['id'])
        send_telegram_msg(msg)
        send_slack_msg(msg)
        return True


with open("words.txt", mode='r') as watchlist_items:
    watchlist = list(map(lambda x: str(x).strip(), watchlist_items.read().split("\n")))

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(token, token_secret)

twitterStream = Stream(auth, Listener())
twitterStream.filter(track=watchlist, languages=['fa', ], is_async=True)

while True:
    send_telegram_msg("I'm alive")
    print("waiting for the next")
    time.sleep(3600 * 6)
