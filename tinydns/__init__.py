# -*- coding: utf-8 -*-
import argparse
from gevent import socket
import gevent
from gevent import monkey
monkey.patch_socket()
from dnslib import *
import ConfigParser
cf = ConfigParser.ConfigParser()
# 读取配置文件
# /etc/tinydns.conf
cf.read("../tinydns.conf")
# AF_INET = cf.get('gevent_dns','AF_INET')
# SOCK_DGRAM = cf.get('gevent_dns','AF_INET')
# port = cf.get('gevent_dns','port')

AF_INET = 2
SOCK_DGRAM = 2
port = 53
s = socket.socket(int(AF_INET), int(SOCK_DGRAM))
s.bind(('', int(port)))

def dns_handler(s, peer, data):
    request = DNSRecord.parse(data)
    id = request.header.id
    qname = request.q.qname
    qtype = request.q.qtype
    try:
        IP = socket.gethostbyname(str(qname))
    except Exception as e:
        print e
        print ('Host not found')
        IP = '0.0.0.0'
    print ("Request (%s): %r (%s) - Response: %s" % (str(peer), qname.label,QTYPE[qtype], IP))
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


def main():
    parser = argparse.ArgumentParser(description='Run some watchers.')
    parser.add_argument('-c', type=str,default='../tinydns.conf',
                        help="Run service command tinydns -c /etc/tinydns.conf")
    args = parser.parse_args()
    while True:
        data, peer = s.recvfrom(8192)
        gevent.spawn(dns_handler, s, peer, data)


if __name__ == '__main__':
    main()