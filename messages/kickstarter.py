from messages import Message
import alphasign
import logging

from bs4 import BeautifulSoup, SoupStrainer
import requests

class KickstarterMessage(Message):

    def __init__(self, label, name, url):
        self.url = url
        self.name = name
        super(KickstarterMessage, self).__init__(label)
        self.update_period = 10 * 60 # 10 minutes

    def do_update(self):
        # fetch page
        logging.info("fetching kickstarter information for %s" % self.name)
        result = requests.get(self.url)
        if result.status_code != 200:
            self.text = "failed to fetch stats for %s" % self.name
            return

        # parse
        logging.info("parsing")
        strainer = SoupStrainer('div', attrs={'class': "NS_campaigns__stats"})
        soup = BeautifulSoup(result.content, 'lxml', parse_only=strainer)
        pledged = soup.find("div", {"id": "pledged"})
        backers = soup.find("div", {"id": "backers_count"})
        duration = soup.find("span", {"id": "project_duration_data"})
        logging.info(pledged)
        logging.info(backers)
        logging.info(duration)

        # assemble text
                    ##############################  30 chars wide
        self.top = "name    days #    total    %  "
        self.bot = "%-7s %-4d %-4d %-8d %-3d" % (self.name, int(duration.attrs['data-hours-remaining'])/24,
            int(backers.attrs['data-backers-count']),
            float(pledged.attrs['data-pledged']),
            float(pledged.attrs['data-percent-raised'])*100)
    
    def get_plain_text(self):
        logging.info("[" + self.top + "]")
        logging.info("[" + self.bot + "]")

    # override get_text so we can show stuff on the top and bottom lines at once
    def get_text(self):
        return alphasign.Text(self.top + self.bot, mode=alphasign.modes.AUTOMODE, position=alphasign.positions.FILL, label=self.label)

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
   
    project_name = 'Reflex'
    project_url = 'https://www.kickstarter.com/projects/reflexcamera/reflex-bringing-back-the-analogue-slr-camera'
    ks = KickstarterMessage('A', project_name, project_url)
    logging.info(ks.get_plain_text())
