from udpgen import settings
import logging
log = logging.getLogger(__name__)

import atexit
import os
import random
import re
import socket
import sys
import threading
from time import sleep

UDP_THREADS = []
command_pattern = re.compile(r'(?P<mode>[+-])(?P<host>[\d\w\:\-\.]+) (?P<port>\d+)')

def send_udp(host, port, stopping, bw=100, rate=3):
    """Send udp packets to <host>:<port> at a rate of <rate> bytes per second"""
    host = socket.getaddrinfo(host, port)[0]
    s = socket.socket(host[0], socket.SOCK_DGRAM)
    bw_r = int(bw/rate)
    wait = 1.0/rate
    source = open("/dev/urandom", "r")
    while not stopping.is_set():
        data = source.read(bw_r)
        log.debug("%d bytes to %s: %s" % (
            len(data),
            host[4],
            ''.join([hex(ord(c))[2:] for c in data])
        ))
        s.sendto(data, host[4])
        sleep(wait)
    log.info("Stream to %s:%s dead" % (host[4][0], host[4][1]))

def create_ctl_sock(ctrl_sock=settings.UDPGEN_CONTROL_SOCKET):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    def cleanup_ctl_sock(ctrl_sock):
        try:
            os.remove(ctrl_sock)
        except:
            pass
    cleanup_ctl_sock(ctrl_sock)
    s.bind(ctrl_sock)
    s.listen(1)
    atexit.register(cleanup_ctl_sock, ctrl_sock)
    return s

def run_command(mode=None, host=None, port=None, **others):
    log.info("running command: mode=%s, host=%s, port=%s" % (mode, host, port))
    if mode == None or host == None or port == None:
        log.error("Invalid command: %r %r %r %r" % (mode, host, port, others))
        return
    if mode == '+':
        t_stop = threading.Event()
        t = threading.Thread(target=send_udp, args=(host, int(port), t_stop))
        t.daemon =  True # Die on exit
        t.start()
        log.info("Started sending to %s:%d" % (host, int(port)))
        UDP_THREADS.append(("%s:%s"%(host,port), t, t_stop))
        return
    if mode == '-':
      for u_t in UDP_THREADS:
        log.debug("Searching for %s:%s: %s" % (host, port, u_t[0]))
        if u_t[0] == "%s:%s"%(host,port):
            log.info("Stopping thread: %s" % u_t[1])
            u_t[2].set()
            log.info("Stopped sending to %s:%d" % (host, int(port)))
            return
        log.error("Could not find (%s:%s) in %s" % (host, port, UDP_THREADS))
        

if __name__ == '__main__':
    # Create a control socket
    try:
        sock_name = sys.argv[1]
    except Exception as e:
        sock_name = settings.UDPGEN_CONTROL_SOCKET
        log.debug("Using UDPGEN_CONTROL_SOCKET")
    while True:
        try:
            s = create_ctl_sock(sock_name)
            log.debug("Listening on %s" % sock_name)
        except socket.error:
            log.error("Unable to open control socket %s")
            s = None
            continue
        while True:
            try:
                conn, addr = s.accept()
                log.info("Accepted connection from %s" % addr)
                while True:
                    ctl_buf = conn.recv(4096)
                    if ctl_buf == "":
                        # Symptomatic of a closed connection
                        conn.close()
                        break
                    log.debug("Command received: %s" % ctl_buf)
                    match = re.match(command_pattern, ctl_buf)
                    if match == None:
                        log.error("Could not parse command: %s" % ctl_buf)
                    command = match.groupdict()
                    run_command(**command)
            except socket.error:
                info("Bad Stream")
                continue
            except Exception as e:
                log.error("%s"%e)
                conn.close()


