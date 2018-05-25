#!/usr/bin/python
# -*- coding: UTF-8 -*-
import socket 
import json
import os

global LocalIP
global HostIP
global Login_Token
Domains = None

def ddns(domain):
    import dnspod

    domain_id = dnspod.get_domain_id(Login_Token, domain['name'])
    if domain_id == 0:
        domain_id = dnspod.create_domain(Login_Token, domain['name'])
    
    for sub_domain in domain['sub_domains']:
        record_id = dnspod.get_record_id(Login_Token, domain_id, sub_domain)
        if record_id == 0:
            dnspod.create_record_id(Login_Token, domain_id, sub_domain, LocalIP)
        else:
            dnspod.record_ddns(Login_Token, domain_id, record_id, sub_domain, LocalIP)

    
def getip():
    global LocalIP
    sock = socket.create_connection(('ns1.dnspod.net', 6666), 20)
    LocalIP = sock.recv(16)
    sock.close()


def getHostIP(domain):
    global HostIP
    ip = socket.gethostbyname_ex(domain['name'])
    HostIP = ip[2][0]

    
if __name__ == '__main__':
    global Login_Token
    conf = json.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "conf.json"), "r"))

    Login_Token = "%s,%s" % (conf['id'], conf['token'])
    Domains = conf['domains']
    
    try:
        getip()
        for domain in Domains:
            getHostIP(domain)
            if HostIP != LocalIP:
                print "Begin update [%s]." % domain['name']
                ddns(domain)
    except Exception as e:
        print e
        pass