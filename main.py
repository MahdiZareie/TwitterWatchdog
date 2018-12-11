import time
from twitter import Twitter, OAuth
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from requests.sessions import Session
import threading
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
WORDLIST = os.environ.get("WORDLIST")


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


def watch():
    watchlist = list(map(lambda x:str(x).strip(), str(WORDLIST).split(",")))
    while True:
        try:
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(token, token_secret)
            twitterStream = Stream(auth, Listener())
            twitterStream.filter(track=watchlist, languages=['fa', ])
        except Exception as exp:
            print("{} happened, but let's continue".format(exp))


def main():
    t = threading.Thread(target=watch, )
    t.start()
    while True:
        print("waiting for the next")
        time.sleep(6 * 3600)
        send_telegram_msg("I'm alive")


if __name__ == "__main__":
    main()
