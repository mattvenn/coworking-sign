import time
import logging
from abc import ABCMeta, abstractmethod

log = logging.getLogger(__name__)

class Message(object):
    def __init__(self):
        self.last_updated = 0
        self.update_period = 120
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

    # return text
    def get_text(self):
        return self.text


class StaticMessage(Message):
    
    def __init__(self, text):
        super(StaticMessage, self).__init__()
        self.update_period = 0
        self.text = text

    def do_update(self):
        pass
      

class AmazingMessage(Message):

    def __init__(self):
        self.people = [ 'Guillem Cabo Engineering', 'Fumblau','SimracingCoach', 'Syrius Prototypes', 'Matt Venn Engineering', 'YOU' ]
        self.index = 0
        super(AmazingMessage, self).__init__()

    def do_update(self):
        self.text = "%s is AMAZING!" % self.people[self.index]
        self.index += 1
        if self.index > len(self.people):
            self.index = 0

class TimeMessage(Message):
    
    def do_update(self):
        from datetime import datetime
        self.text = str(datetime.now())

class BitCoinMessage(Message):

    def do_update(self):
        from forex_python.bitcoin import BtcConverter
        bitcoin = BtcConverter() 
        self.text = "1 Bitcoin = %d EUR" % bitcoin.get_latest_price('EUR')

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    
    sm = StaticMessage("hello")
    tm = TimeMessage()
    bm = BitCoinMessage()

    messages = [ sm, tm, bm ]

    # initial message
    for m in messages:
        logging.info(m.get_text())

    # poll and update
    while True:
        time.sleep(1)
        logging.info("sleeping")
        for m in messages:
            if m.update():
                logging.info(m.get_text())
