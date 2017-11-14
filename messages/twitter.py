from messages import TwoLineMessage, is_pi
import logging
import alphasign
import tweepy
from twitter_secrets import *


class TwitterMessage(TwoLineMessage):

    def __init__(self, label, name):
        self.name = name
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        self.api = tweepy.API(auth)
        # top line is actually only 29 chars - off by one bug in the sign's firmware? - also needs a space at the end..
                    #############################  
        self.top = "twitter    tweets favs folows "

        super(TwitterMessage, self).__init__(label)

    def do_update(self):
        dygma = self.api.get_user('dygmalab')
        self.bot = "%-12s %-5d %-5d %-5d" % (self.name[0:12], dygma.followers_count, dygma.statuses_count, dygma.favourites_count)


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
   
    tm = TwitterMessage('A', "dygmalab")
    logging.info(tm.get_plain_text())

    if is_pi():
        sign = alphasign.interfaces.local.Serial(device='/dev/ttyUSB0', baudrate=38400)
        sign.connect()
        sign.clear_memory()
        sign.write(tm.get_text())
