from udpgen import settings
import logging
log = logging.getLogger(__name__)

import select
import socket

open_sockets = []
def listen(family=socket.AF_INET, port=settings.UDPGEN_LISTEN_PORT):
    s = socket.socket(family, socket.SOCK_DGRAM)
    s.bind(("", port))
    log.info("Listening on %s:%d" % (s.getsockname()[0], s.getsockname()[1]))

    global open_sockets
    open_sockets.append(s)

def receive_data(addr, data):
    log.debug("%s: %s" % (addr,
        ''.join([hex(ord(c))[2:] for c in data])
    ))


if __name__ == '__main__':
    listen(socket.AF_INET)
    listen(socket.AF_INET6)

    while True:
        r, w, x = select.select(open_sockets, [], [])
	data, addr = r[0].recvfrom(4096)
	receive_data(addr, data)
