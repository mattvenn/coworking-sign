import time
import logging
from abc import ABCMeta, abstractmethod

log = logging.getLogger(__name__)

def is_pi():
    import socket
    hostname = socket.gethostname()
    #logging.info(hostname) # if this line is commented, log level is forced to warning?!
    if hostname == "raspberrypi":
        return True
    return False

import alphasign

class Message(object):
    def __init__(self, label):
        self.last_updated = 0
        self.label = label
        self.update_period = 5 * 60 # 5 minutes in seconds
        self.setup()
        self.update()
    
    # is update necessary
    def update(self):
        if self.update_period and (time.time() > self.last_updated + self.update_period):
            self.last_updated = time.time()
            self.do_update()
            return True
        return False
    
    # do the work
    @abstractmethod
    def do_update(self):
        pass

    # hook for any setup required before update is called
    def setup(self):
        pass

    # return text for the sign
    def get_text(self):
        return alphasign.Text(self.text, mode=alphasign.modes.AUTOMODE, label=self.label)

    # return plain text for logging/debugging
    def get_plain_text(self):
        return '[%s] %s' % (self.label, self.text)

    # in case any message needs to do anything at shutdown
    def finish(self):
        pass

    def get_color_compare(self, a, b):
        if a > b:
            color = alphasign.colors.GREEN
        elif a < b:
            color = alphasign.colors.RED
        else:
            color = alphasign.colors.YELLOW
        return color

class TwoLineMessage(Message):

    def get_plain_text(self):
        log.info("[" + self.top + "]")
        log.info("[" + self.bot + "]")

    def get_text(self):
        # fixed width to allow matching things up across the two lines
        return alphasign.Text(alphasign.charsets.FIXED_WIDTH_ON + self.top + self.bot, mode=alphasign.modes.AUTOMODE, position=alphasign.positions.FILL, label=self.label)

class StaticMessage(Message):
    
    def __init__(self, label, text):
        super(StaticMessage, self).__init__(label)
        self.update_period = 0
        self.text = text

    def do_update(self):
        pass
      

class AmazingMessage(Message):

    def setup(self):
        self.people = [ 'Guillem Cabo Engineering', 'Fumblau','SimracingCoach', 'Sirius Prototypes', 'Matt Venn Engineering', 'YOU', 'Seku' ]
        self.index = 0

    def do_update(self):
        self.text = "%s is %sAMAZING!" % (self.people[self.index], alphasign.charsets.WIDE_ON)
        self.index += 1
        if self.index >= len(self.people):
            self.index = 0

class TimeMessage(Message):
    
    def do_update(self):
        from datetime import datetime
        self.text = time.strftime("%c", time.localtime())
    
class CurrencyMessage(Message):

    def __init__(self, label, conv_from, conv_to='EUR'):
        self.conv_from = conv_from
        self.conv_to = conv_to
        self.last_conv = 0
        super(CurrencyMessage, self).__init__(label)

    def do_update(self):
        from forex_python.converter import CurrencyRates
        cr = CurrencyRates()
        log.info("fetching currency update %s to %s" % (self.conv_from, self.conv_to))
        try:
            conv = cr.get_rate(self.conv_from, self.conv_to)
            self.text = "1 %s = %s%.2f %s" % (self.conv_from, self.get_color_compare(conv, self.last_conv), conv , self.conv_to)
            self.last_conv = conv
        except requests.exceptions.RequestException as e:
            logging.warning("couldn't get update: %s" % e)


class BitcoinMessage(Message):

    def setup(self):
        self.last_btc = 0

    def do_update(self):
        from forex_python.bitcoin import BtcConverter
        log.info("fetching currency update")
        bitcoin = BtcConverter() 
        try:
            btc = bitcoin.get_latest_price('EUR')

            self.text = "1 Bitcoin = %s%.2f EUR" % (self.get_color_compare(btc, self.last_btc), btc)
            self.last_btc = btc
        except requests.exceptions.RequestException as e:
            logging.warning("couldn't get update: %s" % e)


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    
    sm = StaticMessage('A', "hello")
    tm = TimeMessage('B')
    cm = CurrencyMessage('C', 'GBP')
    bc = BitcoinMessage('D')
    am = AmazingMessage('E')

    messages = [ sm, tm, cm, bc, am ]

    # initial message
    for m in messages:
        logging.info(m.get_plain_text())

    # poll and update
    while True:
        time.sleep(1)
        logging.info("sleeping")
        for m in messages:
            if m.update():
                logging.info(m.get_text())
