from udpgen import settings
import logging
log = logging.getLogger(__name__)

import atexit
import os
import random
import socket
from time import sleep

def send_udp(host, port, bw=100, rate=3):
    """Send udp packets to <host>:<port> at a rate of <rate> bytes per second"""
    host = socket.getaddrinfo(host, port)[0]
    s = socket.socket(host[0], socket.SOCK_DGRAM)
    bw_r = int(bw/rate)
    wait = 1.0/rate
    source = open("/dev/urandom", "r")
    while True:
        data = source.read(bw_r)
	log.debug("%d bytes to %s: %s" % (
	    len(data),
	    host,
	    ''.join([hex(ord(c))[2:] for c in data])
	))
	s.sendto(data, host[4])
	sleep(wait)

def create_ctl_sock():
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    def cleanup_ctl_sock():
        try:
            os.remove(settings.UDPGEN_CONTROL_SOCKET)
	except:
	    pass
    cleanup_ctl_sock()
    s.bind(settings.UDPGEN_CONTROL_SOCKET)
    atexit.register(cleanup_ctl_sock)
    return s

if __name__ == '__main__':
    # Create a control socket
    s = create_ctl_sock()
    s.listen(1)
    ctl_buf = ""
    while True:
        conn, addr = s.accept()
        ctl_buf += conn.recv(4096)
	# Currently, do nothing. TODO open and close udp flows on command.
	# for now, dont memory leak.
	ctl_buf = ""


