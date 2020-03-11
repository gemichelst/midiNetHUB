#!/usr/bin/python

import sys
import socket
import struct
import time

local_port = 5006

if len(sys.argv) == 1:
    family = socket.AF_INET
    connect_tuple = ( 'localhost', local_port )
else:
    details = socket.getaddrinfo( sys.argv[1], local_port, socket.AF_UNSPEC, socket.SOCK_DGRAM)
    family = details[0][0]
    if family == socket.AF_INET6:
        connect_tuple = ( sys.argv[1], local_port, 0, 0)
    else:
        connect_tuple = ( sys.argv[1], local_port)

s = socket.socket( family, socket.SOCK_DGRAM )
s.setblocking(0)
s.connect( connect_tuple )

# Control Change
bytes = struct.pack( "BBB", 0xB6, 0x3c, 0x7f )
s.send( bytes )
bytes = struct.pack( "BBB", 0xB6, 0x3e, 0x7f )
s.send( bytes )

s.close()

