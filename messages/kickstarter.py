from messages import Message, is_pi
import alphasign
import logging

from bs4 import BeautifulSoup, SoupStrainer
import requests

class KickstarterMessage(Message):

    def __init__(self, label, name, url, fake=False):
        self.url = url
        self.fake = fake
        self.name = name
        self.top = "name      day bkrs total   % " # top line is actually only 29 chars - off by one bug in the sign's firmware?
        super(KickstarterMessage, self).__init__(label)
        self.update_period = 60 * 60 # 60 minutes in seconds

    def do_update(self):
        if self.fake:
            self.bot = "%-9s %-3d %-4d %-7d %-3d" % (self.name[0:9], 5, 1581, 1000000, 199)
            return

        # fetch page
        logging.info("fetching kickstarter information for %s" % self.name)
        result = requests.get(self.url)
        if result.status_code != 200:
            self.text = "failed to fetch stats for %s" % self.name
            return

        # parse
        logging.info("parsing - takes a long time on the Pi!")
        strainer = SoupStrainer('div', attrs={'class': "NS_campaigns__stats"})
        soup = BeautifulSoup(result.content, 'lxml', parse_only=strainer)
        pledged = soup.find("div", {"id": "pledged"})
        backers = soup.find("div", {"id": "backers_count"})
        duration = soup.find("span", {"id": "project_duration_data"})

        # assemble text
                    ##############################  30 chars wide
        self.top = "name    days #    total    %  "
        self.bot = "%-9s %-4d %-4d %-7d %-3d" % (self.name[0:9], int(duration.attrs['data-hours-remaining'])/24,
            int(backers.attrs['data-backers-count']),
            float(pledged.attrs['data-pledged']),
            float(pledged.attrs['data-percent-raised'])*100)
    
    def get_plain_text(self):
        logging.info("[" + self.top + "]")
        logging.info("[" + self.bot + "]")

    # override get_text so we can show stuff on the top and bottom lines at once
    def get_text(self):
        return alphasign.Text(alphasign.charsets.FIXED_WIDTH_ON + self.top + self.bot, mode=alphasign.modes.AUTOMODE, position=alphasign.positions.FILL, label=self.label)

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
   
    project_name = 'IOToilets'
    project_url = 'http://iotoilets.com'
    ks = KickstarterMessage('A', project_name, project_url, fake=True) # fake to avoid the overhead of actually parsing
    logging.info(ks.get_plain_text())

    if is_pi():
        sign = alphasign.interfaces.local.Serial(device='/dev/ttyUSB0', baudrate=38400)
        sign.connect()
        sign.clear_memory()
        sign.write(ks.get_text())
