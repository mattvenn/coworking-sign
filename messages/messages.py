import time
import logging
import alphasign
from abc import ABCMeta, abstractmethod

log = logging.getLogger(__name__)

def is_pi():
    import socket
    hostname = socket.gethostname()
    logging.info(hostname)
    if hostname == "raspberrypi":
        return True
    return False

class Message(object):
    def __init__(self, label):
        self.last_updated = 0
        self.label = label
        self.update_period = 5 * 60 # 5 minutes in seconds
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

    # return text for the sign
    def get_text(self):
        return alphasign.Text(self.text, mode=alphasign.modes.AUTOMODE, label=self.label)

    # return plain text for logging/debugging
    def get_plain_text(self):
        return '[%s] %s' % (self.label, self.text)

class StaticMessage(Message):
    
    def __init__(self, label, text):
        super(StaticMessage, self).__init__(label)
        self.update_period = 0
        self.text = text

    def do_update(self):
        pass
      

class AmazingMessage(Message):

    def __init__(self, label):
        self.people = [ 'Guillem Cabo Engineering', 'Fumblau','SimracingCoach', 'Syrius Prototypes', 'Matt Venn Engineering', 'YOU' ]
        self.index = 0
        super(AmazingMessage, self).__init__(label)

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
        super(CurrencyMessage, self).__init__(label)

    def do_update(self):
        from forex_python.converter import CurrencyRates
        cr = CurrencyRates()
        logging.info("fetching currency update %s to %s" % (self.conv_from, self.conv_to))
        self.text = "1 %s = %.2f %s" % (self.conv_from, cr.get_rate(self.conv_from, self.conv_to), self.conv_to)

class BitcoinMessage(Message):

    def do_update(self):
        from forex_python.bitcoin import BtcConverter
        logging.info("fetching currency update")
        bitcoin = BtcConverter() 
        self.text = "1 Bitcoin = %.2f EUR" % bitcoin.get_latest_price('EUR')

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    
    sm = StaticMessage('A', "hello")
    tm = TimeMessage('B')
    cm = CurrencyMessage('C', 'GBP')
    bc = BitcoinMessage('D')

    messages = [ sm, tm, cm, bc ]

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
