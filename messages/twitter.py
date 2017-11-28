from messages import TwoLineMessage, is_pi
if is_pi():
    import alphasign
import tweepy
from twitter_secrets import *
import pickle
import logging

log = logging.getLogger(__name__)

class TwitterMessage(TwoLineMessage):

    def __init__(self, label, name, fake=False):
        self.name = name
        self.fake = fake
        log.info("tweepy oauth")
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        self.api = tweepy.API(auth)
        # top line is actually only 29 chars - off by one bug in the sign's firmware? - also needs a space at the end..
                    #############################
        self.top = "twitter   twts fols favs rts "

        self.stats = dict( statuses = 0, followers = 0, favs = 0, retweets = 0 )
        self.last_stats = self.stats

        super(TwitterMessage, self).__init__(label)
        self.update_period = 60 * 60 # 60 minutes in seconds - as the update takes so long

    def do_update(self):
        log.info("fetching history... this will take some time")

        # bit silly having to fetch entire history, but there seems no way to easily cache it
        # and only get updates. The streaming api seems to only accept new tweets from the user
        # we could fetch entire history, cache it and then only fetch updates on most recent tweets
        # but easier to just get it all, and it's not like theres a rush...
        
        self.stats['favs'] = 0
        self.stats['retweets'] = 0
        if self.fake == False:
            for status in tweepy.Cursor(self.api.user_timeline, id=self.name).items():
                self.stats['favs'] += status.favorite_count
                self.stats['retweets'] += status.retweet_count

        user = self.api.get_user(self.name)
        self.stats['statuses'] = user.statuses_count
        self.stats['followers'] = user.followers_count

        self.bot = "%-9s %s%-4d %s%-4d %s%-4d %s%-4d" % (self.name[0:9],
            self.get_color_compare(self.stats['statuses'], self.last_stats['statuses']), self.stats['statuses'],
            self.get_color_compare(self.stats['followers'], self.last_stats['followers']), self.stats['followers'],
            self.get_color_compare(self.stats['favs'], self.last_stats['favs']), self.stats['favs'],
            self.get_color_compare(self.stats['retweets'], self.last_stats['retweets']), self.stats['retweets'])

        self.last_stats = self.stats

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    tm = TwitterMessage('A', "fumblau", fake=False)
    logging.info(tm.get_plain_text())

    if is_pi():
        sign = alphasign.interfaces.local.Serial(device='/dev/ttyUSB0', baudrate=38400)
        sign.connect()
        sign.clear_memory()
        sign.write(tm.get_text())
