import time
import alphasign
import subprocess
import logging
from messages import StaticMessage, TimeMessage, BitcoinMessage, CurrencyMessage, AmazingMessage, KickstarterMessage

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

pi = True
#pi = False

if __name__ == "__main__":

    logging.info("starting sign writer")

    if pi:
        sign = alphasign.interfaces.local.Serial(device='/dev/ttyUSB0', baudrate=38400)
        sign.connect()
        sign.clear_memory()


    messages = [
        StaticMessage('A', "pull requests to http://bit.ly/cowork-sign"),
        TimeMessage('B'),
        CurrencyMessage('C', 'GBP'),
        BitcoinMessage('D'),
        AmazingMessage('E'),
        KickstarterMessage('F', 'Reflex', 'https://www.kickstarter.com/projects/reflexcamera/reflex-bringing-back-the-analogue-slr-camera'),
        ]

    # initial message
    for m in messages:
        logging.info(m.get_plain_text())
        if pi:
            sign.write(m.get_text())


    # poll and update
    while True:
        time.sleep(1)
        logging.info("sleeping")
        for m in messages:
            if m.update():
                logging.info(m.get_plain_text())
                if pi:
                    sign.write(m.get_text())
