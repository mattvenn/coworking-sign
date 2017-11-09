import time
import alphasign
import subprocess
import logging
from messages import StaticMessage, TimeMessage, BitCoinMessage, AmazingMessage

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

#pi = False
pi = True

if __name__ == "__main__":

    logging.info("starting sign writer")

    if pi:
        sign = alphasign.interfaces.local.Serial(device='/dev/ttyUSB0', baudrate=38400)
        sign.connect()
        sign.clear_memory()


    messages = { 
        'A' : StaticMessage("pull requests to http://bit.ly/cowork-sign"),
        'B' : TimeMessage(),
        'C' : BitCoinMessage(),
        'D' : AmazingMessage(),
        }

    # initial message
    for label in messages.keys():
        text = messages[label].get_text()
        logging.info('%s : %s' % (label, text))
        if pi:
            sign.write(alphasign.Text(text, label=label, mode=alphasign.modes.AUTOMODE))


    # poll and update
    while True:
        time.sleep(1)
        logging.info("sleeping")
        for label in messages.keys():
            if messages[label].update():
                text = messages[label].get_text()
                logging.info('%s : %s' % (label, text))
                if pi:
                    sign.write(alphasign.Text(text, label=label, mode=alphasign.modes.AUTOMODE))
