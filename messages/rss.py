from messages import is_pi, Message
if is_pi():
    import alphasign

import feedparser
from bs4 import BeautifulSoup
import re
import logging
import datetime

log = logging.getLogger(__name__)

class RSSMessage(Message):

    def __init__(self, label, url):
        self.url = url
        super(RSSMessage, self).__init__(label)
        self.update_period = 6 * 60 * 60 # 6 hours in seconds

    def do_update(self):
        feed = feedparser.parse(self.url)
        item = feed['items'][0] # get first item
        soup = BeautifulSoup(item['summary'], 'lxml')
        text = soup.get_text()
        self.text = text.split('.')[0]
        self.text = self.text.encode('utf-8')

    # override get_text so we can force scroll with high speed
    def get_text(self):
        return alphasign.Text(alphasign.speeds.SPEED_5 + self.text, mode=alphasign.modes.SCROLL, label=self.label)

class TechHistoryMessage(RSSMessage):

    # override to make date easier to understand
    def do_update(self):
        super(TechHistoryMessage, self).do_update()
        logging.info(self.text)
        m = re.search("(\w+) (\d+), (\d{4}) (.*)", self.text)
        if m is not None:
            this_year = int(datetime.datetime.today().strftime("%Y"))
            year = int(m.group(3))
            text = m.group(4)
            self.text = "%d years ago today - %s" % (this_year - year, text)



if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    m = TechHistoryMessage('A', 'http://thisdayintechhistory.com/feed/')
        
    logging.info(m.get_plain_text())

    if is_pi():
        sign = alphasign.interfaces.local.Serial(device='/dev/ttyUSB0', baudrate=38400)
        sign.connect()
        sign.clear_memory()
        sign.write(m.get_text())
