# -*- coding: utf-8 -*-
import sys
import argparse
import os
from gevent import socket
import gevent
from gevent import monkey
monkey.patch_socket()
import redis
from dnslib import *
import ConfigParser
cf = ConfigParser.ConfigParser()
# 读取配置文件
# /etc/tinydns.conf
cf.read("../tinydns.conf")
A_RECORD_PREFIX = cf.get('dns','A_RECORD_PREFIX')
TXT_RECORD_PREFIX = cf.get('dns','TXT_RECORD_PREFIX')
CNAME_RECORD_PREFIX = cf.get('dns','CNAME_RECORD_PREFIX')
AF_INET = cf.get('gevent','AF_INET')
SOCK_DGRAM = cf.get('gevent','AF_INET')
s = socket.socket(int(AF_INET), int(SOCK_DGRAM))
port = cf.get('dns','port')
s.bind(('', int(port)))


def dns_handler(s, peer, data,r):
    request = DNSRecord.parse(data)
    id = request.header.id
    qname = request.q.qname
    qtype = request.q.qtype
    IP =  r.get(A_RECORD_PREFIX % qname)
    TXT = r.get(TXT_RECORD_PREFIX % qname)
    CNAME = r.get(CNAME_RECORD_PREFIX % qname)
    if not IP:
        try:
            IP = socket.gethostbyname(str(qname))
        except Exception as e:
            print e
            print ('Host not found')
            IP = '0.0.0.0'
    reply = DNSRecord(DNSHeader(id=id, qr=1, aa=1, ra=1), q=request.q)
    if qtype == QTYPE.A:
        reply.add_answer(RR(qname, qtype, rdata=A(IP)))
    elif qtype == QTYPE['*']:
        reply.add_answer(RR(qname, QTYPE.A, rdata=A(IP)))
        reply.add_answer(RR(qname, QTYPE.MX, rdata=MX(IP)))
        reply.add_answer(RR(qname, QTYPE.TXT, rdata=TXT(TXT)))
    else:
        reply.add_answer(RR(qname, QTYPE.CNAME, rdata=CNAME(TXT)))
    s.sendto(reply.pack(), peer)


try:
    import resource
except ImportError:
    resource = None
MAXFD = 1024
if hasattr(os, "devnull"):
    REDIRECT_TO = os.devnull  # PRAGMA: NOCOVER
else:
    REDIRECT_TO = "/dev/null"  # PRAGMA: NOCOVER

def get_maxfd():
    if not resource:
        maxfd = MAXFD
    else:
        maxfd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
        if maxfd == resource.RLIM_INFINITY:
            maxfd = MAXFD
    return maxfd

try:
    from os import closerange
except ImportError:
    def closerange(fd_low, fd_high):    # NOQA
        # Iterate through and close all file descriptors.
        for fd in range(fd_low, fd_high):
            try:
                os.close(fd)
            except OSError:    # ERROR, fd wasn't open to begin with (ignored)
                pass

def daemonize():
    """Standard daemonization of a process.
    """
    # guard to prevent daemonization with gevent loaded
    for module in sys.modules.keys():
        if module.startswith('gevent'):
            raise ValueError('Cannot daemonize if gevent is loaded')

    if hasattr(os, 'fork'):
        child_pid = os.fork()
    else:
        raise ValueError("Daemonizing is not available on this platform.")

    if child_pid != 0:
        # we're in the parent
        os._exit(0)

    # child process
    os.setsid()

    subchild = os.fork()
    if subchild:
        os._exit(0)

    # subchild
    maxfd = get_maxfd()
    closerange(0, maxfd)
    os.open(REDIRECT_TO, os.O_RDWR)
    os.dup2(0, 1)
    os.dup2(0, 2)

def main():
    parser = argparse.ArgumentParser(description='Run some watchers.')
    parser.add_argument('-c', dest='daemonize', action='store_true',
                        help="Start tinydns in the background. Not supported "
                             "on Windows")
    args = parser.parse_args()
    host = cf.get('db','db_host')
    port = cf.get('db','db_port')
    db = cf.get('db','db')
    r = redis.Redis(host=host, port=int(port), db=int(db))
    while True:
        data, peer = s.recvfrom(8192)
        gevent.spawn(dns_handler, s, peer, data,r)


if __name__ == '__main__':
    main()

