from messages import TwoLineMessage, is_pi
import alphasign
import logging
import re
import requests

class KickstarterMessage(TwoLineMessage):

    def __init__(self, label, name, url, fake=False):
        self.url = url
        self.fake = fake
        self.name = name
        self.top = "name      day bkrs $total  % " # top line is actually only 29 chars - off by one bug in the sign's firmware?
        super(KickstarterMessage, self).__init__(label)
        self.update_period = 60 * 60 # 60 minutes in seconds

    def do_update(self):
        if self.fake:
            self.bot = "%-9s %-3d %-4d %-7d %-3d" % (self.name[0:9], 23, 409, 126186, 126)
            return

        # fetch page
        logging.info("fetching kickstarter information for %s" % self.name)
        result = requests.get(self.url)
        if result.status_code != 200:
            self.text = "failed to fetch stats for %s" % self.name
            return

        m = re.search('data-pledged="([0-9.]+)"', result.content)
        pledged = float(m.group(1))
        
        m = re.search('data-backers-count="([0-9.]+)"', result.content)
        backers = int(m.group(1))

        m = re.search('data-hours-remaining="([0-9.]+)"', result.content)
        duration = int(m.group(1))

        m = re.search('data-percent-raised="([0-9.]+)"', result.content)
        percent_raised = float(m.group(1))

        # assemble text
                    ##############################  30 chars wide
        self.bot = "%-9s %-3d %-4d %-7d %-3d" % (self.name[0:9], duration/24, backers, pledged, percent_raised*100)
    

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
   
    project_name = 'IOToilets'
    project_url = 'http://iotoilets.com'
    project_url = 'https://www.kickstarter.com/projects/deilor/dygma-raise-the-worlds-most-advanced-gaming-keyboa'
    ks = KickstarterMessage('A', project_name, project_url, fake=False) # fake to avoid the overhead of actually parsing
    logging.info(ks.get_plain_text())

    if is_pi():
        sign = alphasign.interfaces.local.Serial(device='/dev/ttyUSB0', baudrate=38400)
        sign.connect()
        sign.clear_memory()
        sign.write(ks.get_text())
