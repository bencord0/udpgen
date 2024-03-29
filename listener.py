# Copyright 2012 Ben Cordero.
#
# This file is part of udpgen.
#
# udpgen is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# udpgen is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with udpgen.  If not, see <http://www.gnu.org/licenses/>.


from udpgen import settings
import logging
log = logging.getLogger(__name__)

import select
import socket
import sys

open_sockets = []
def listen(family=socket.AF_INET, port=0):
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
    try:
        port = int(sys.argv[1])
    except IndexError:
        port = settings.UDPGEN_LISTEN_PORT
    listen(socket.AF_INET, port)
    listen(socket.AF_INET6, port)

    while True:
        r, w, x = select.select(open_sockets, [], [])
    data, addr = r[0].recvfrom(4096)
    receive_data(addr, data)
