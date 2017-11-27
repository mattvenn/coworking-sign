from messages import TwoLineMessage, is_pi
if is_pi():
    import alphasign
import tweepy
from twitter_secrets import *
import pickle

class TwitterMessage(TwoLineMessage):

    def __init__(self, label, name, fake=False):
        self.name = name
        self.fake = fake
        logging.info("tweepy oauth")
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        self.api = tweepy.API(auth)
        # top line is actually only 29 chars - off by one bug in the sign's firmware? - also needs a space at the end..
                    #############################
        self.top = "twitter   twts fols favs rts "

        super(TwitterMessage, self).__init__(label)
        self.update_period = 60 * 60 # 60 minutes in seconds - as the update takes so long

    def do_update(self):
        logging.info("fetching history... this will take some time")
        favs = 0
        retweets = 0

        # bit silly having to fetch entire history, but there seems no way to easily cache it
        # and only get updates. The streaming api seems to only accept new tweets from the user
        # we could fetch entire history, cache it and then only fetch updates on most recent tweets
        # but easier to just get it all, and it's not like theres a rush...

        if self.fake == False:
            for status in tweepy.Cursor(self.api.user_timeline, id=self.name).items():
                favs += status.favorite_count
                retweets += status.retweet_count

        user = self.api.get_user(self.name)
        self.bot = "%-9s %-4d %-4d %-4d %-4d" % (self.name[0:9], user.followers_count, user.statuses_count, favs, retweets)

if __name__ == "__main__":

    import logging
    logging.basicConfig(level=logging.DEBUG)

    tm = TwitterMessage('A', "dygmalab", fake=False)
    logging.info(tm.get_plain_text())

    if is_pi():
        sign = alphasign.interfaces.local.Serial(device='/dev/ttyUSB0', baudrate=38400)
        sign.connect()
        sign.clear_memory()
        sign.write(tm.get_text())
