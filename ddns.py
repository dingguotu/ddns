#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket 
import json
import os

global LocalIP
global HostIP

ID = None
Token = None
Domain = None
SubDomains = None

params = dict(
    login_token=None,
    format="json",
    domain_id=None,
    record_id=None,
    sub_domain=None,
    record_line="默认",
    value=None
)

def ddns():
    import httplib 
    import urllib

    print ("LocalIP is: %s, HostIP is: %s" % (LocalIP, HostIP))
    
    params['login_token'] = ("%s,%s" % (ID, Token))
    params['value'] = LocalIP
    
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json"}
    conn = httplib.HTTPSConnection("dnsapi.cn")

    for item in SubDomains:
        params['domain_id'] = item['domain_id']
        params['record_id'] = item['record_id']
        params['sub_domain'] = item['name']
        
        conn.request("POST", "/Record.Ddns", urllib.urlencode(params), headers)
        response = conn.getresponse()
        # logger().info(response.status, response.reason)
        data = json.loads(response.read())
        if int(data['status']['code']) == 1:
            print ("DDns Success for subdomain [%s], IP change to %s" % (item['name'], LocalIP))
            continue
        else:
            print ("DDns Error for subdomain [%s]: %s" % (item['name'], data['status']['message']))
            continue
    conn.close()
    
    

def logger():
    import logging
    import datetime
    LOG_FORMAT = "[%(asctime)s]\t[%(levelname)s]\t[%(message)s]"
    LOG_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), ("%s%s%s.log" % (i.day, i.month, i.year) ))
    logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG, filename=LOG_FILE)
    return logging.getLogger(__name__)

    
def getip():
    global LocalIP
    sock = socket.create_connection(('ns1.dnspod.net', 6666), 20)
    LocalIP = sock.recv(16)
    sock.close()


def getHostIP():
    global HostIP
    ip = socket.gethostbyname_ex(Domain)
    HostIP = ip[2][0]

    
if __name__ == '__main__':
    conf = json.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "conf.json"), "r"))

    ID = conf['id']
    Token = conf['token']
    Domain = conf['domain']
    SubDomains = conf['sub_domains']
    
    try:
        getip()
        getHostIP()
        if HostIP != LocalIP:
            ddns()
    except Exception as e:
        print e
        pass