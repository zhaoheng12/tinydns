# -*- coding: utf-8 -*-
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
port = int(cf.get('dns','port'))
s.bind(('', port))


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


def tinydns():
    host = cf.get('db','db_host')
    port = cf.get('db','db_port')
    db = cf.get('db','db')
    r = redis.Redis(host=host, port=int(port), db=int(db))
    while True:
        data, peer = s.recvfrom(8192)
        gevent.spawn(dns_handler, s, peer, data,r)


if __name__ == '__main__':
    tinydns()
