import time
import alphasign
import subprocess
import SocketServer
import logging

HOST, PORT = "0.0.0.0", 9999

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

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        logging.info("{} wrote: {}".format(self.client_address[0], self.data))
        msg = alphasign.Text(self.data)
        sign.write(msg)

        # ack
        self.request.sendall("sign set to %s" % self.data)

if __name__ == "__main__":

    public_ip = subprocess.check_output(['hostname', '-I']).strip()
    logging.info("starting server on %s:%s" % (HOST, PORT))

    sign = alphasign.interfaces.local.Serial(device='/dev/ttyUSB0', baudrate=38400)
    sign.connect()
    sign.clear_memory()

    msg = alphasign.Text("%sserver %s:%s" % (alphasign.colors.RED, public_ip, PORT),
        label="A",
        mode=alphasign.modes.HOLD)

    sign.write(msg)

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
