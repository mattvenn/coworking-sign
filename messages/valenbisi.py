from messages import is_pi, Message
if is_pi():
    import alphasign

import logging
import requests
from datetime import datetime
from xml.etree import ElementTree

log = logging.getLogger(__name__)

class ValenbisiMessage(Message):

    def __init__(self, label, url):
        self.url = url
        super(ValenbisiMessage, self).__init__(label)
        self.update_period = 10 * 60 # 10 minutes in seconds

    def do_update(self):
        # multiple requests give different results for updated
        response = requests.get(self.url, headers={'Cache-Control': 'no-cache'})
        tree = ElementTree.fromstring(response.content)
        available = tree.find('available').text
        total = tree.find('total').text
        updated = int(tree.find('updated').text)
        updated_time = datetime.fromtimestamp(updated)
        delta = datetime.now() - updated_time
        logging.info(updated)
        logging.info(delta.seconds)
        self.text = "Valenbisi: %s de %s bikes listas hace %d minutos" % (available, total, delta.seconds / 60)

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    # see here for all the stations: http://www.valenbisi.es/service/carto
    m = ValenbisiMessage('A', 'http://www.valenbisi.es/service/stationdetails/valence/75')
        
    logging.info(m.get_plain_text())

    if is_pi():
        sign = alphasign.interfaces.local.Serial(device='/dev/ttyUSB0', baudrate=38400)
        sign.connect()
        sign.clear_memory()
        sign.write(m.get_text())
