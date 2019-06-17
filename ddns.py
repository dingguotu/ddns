#!/usr/bin/python
# -*- coding: UTF-8 -*-
import socket 
import json
import os
import dnspod

global LocalIP
global HostIP
global Login_Token
global Domain_Id

def init_domain(domain):
    global Domain_Id

    domain_exists = check_domain_exists(domain)
    if domain_exists == False:
        Domain_Id = dnspod.create_domain(Login_Token, domain['name'])


def check_domain_exists(domain):
    global Domain_Id

    Domain_Id = dnspod.get_domain_id(Login_Token, domain['name'])
    if Domain_Id == 0:
        return False
    else:
        return True


def ddns(domain):
    global Domain_Id

    for sub_domain in domain['sub_domains']:
        record_id = dnspod.get_record_id(Login_Token, Domain_Id, sub_domain)
        if record_id == 0:
            dnspod.create_record_id(Login_Token, Domain_Id, sub_domain, LocalIP)
        else:
            dnspod.record_ddns(Login_Token, Domain_Id, record_id, sub_domain, LocalIP)

    
def get_ip():
    global LocalIP
    sock = socket.create_connection(('ns1.dnspod.net', 6666), 20)
    LocalIP = sock.recv(16)
    sock.close()


def get_host_ip(domain):
    global HostIP
    global Domain_Id

    HostIP = dnspod.get_record_value(Login_Token, Domain_Id, domain['sub_domains'][0])

    
if __name__ == '__main__':
    global Login_Token
    conf = json.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "conf.json"), "r"))

    Login_Token = "%s,%s" % (conf['id'], conf['token'])
    Domains = conf['domains']
    
    try:
        get_ip()
        for domain in Domains:
            init_domain(domain)
            get_host_ip(domain)
            if HostIP != LocalIP:
                print "Begin update [%s]." % domain['name']
                ddns(domain)
    except Exception as e:
        print e
        pass
