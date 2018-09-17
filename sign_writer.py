import time
import alphasign
import subprocess
import logging
from messages import StaticMessage, TimeMessage, BitcoinMessage, CurrencyMessage, AmazingMessage, KickstarterMessage, is_pi, TwitterMessage, RSSMessage, ValenbisiMessage

# get logging started
log_format = logging.Formatter('%(asctime)s - %(name)-12s - %(levelname)-8s - %(message)s')
log = logging.getLogger('')
log.setLevel(logging.DEBUG)

# create console handler and set level to info
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter for console
ch.setFormatter(log_format)
log.addHandler(ch)

# create file handler and set to debug
fh = logging.FileHandler('sign.log')
fh.setLevel(logging.INFO)
fh.setFormatter(log_format)
log.addHandler(fh)

if __name__ == "__main__":

    logging.info("starting sign writer")

    if is_pi():
        sign = alphasign.interfaces.local.Serial(device='/dev/ttyUSB0', baudrate=38400)
        sign.connect()
        sign.clear_memory()
        logging.info("connected to sign via serial")
    else:
        logging.warning("not on a pi, so not using sign")


    messages = [
        StaticMessage('A', "http://bit.ly/cowork-sign"),
        TimeMessage('B'),
        CurrencyMessage('C', 'GBP'),
        BitcoinMessage('D'),
        AmazingMessage('E'),
        RSSMessage('F', 'http://thisdayintechhistory.com/feed/'),
#        TwitterMessage('G', 'dygmalab'),
#        TwitterMessage('H', 'fumblau'),
#        TwitterMessage('I', 'simracingcoach'),
        ValenbisiMessage('J', 'http://www.valenbisi.es/service/stationdetails/valence/75')
#        KickstarterMessage('J', 'Dygma', 'https://www.kickstarter.com/projects/deilor/dygma-raise-the-worlds-most-advanced-gaming-keyboa'),
        ]

    logging.info("done setup - writing")
    # initial message
    for m in messages:
        logging.info(m.get_plain_text())
        if is_pi():
            sign.write(m.get_text())

    logging.info("main loop")
    # poll and update
    try:
        while True:
            time.sleep(5)
            logging.debug("sleeping")
            for m in messages:
                if m.update():
                    logging.info(m.get_plain_text())
                    if is_pi():
                        sign.write(m.get_text())

    except KeyboardInterrupt as e:
        logging.info("shutdown")
        for m in messages:
            m.finish()
        
