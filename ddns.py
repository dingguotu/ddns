#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib2
import json, os, logging
import dnspod
import logger

global LocalIP
global HostIP
global Login_Token
global Domain_Id

def init_domain(domain):
    global Domain_Id
    try:
        domain_exists = check_domain_exists(domain)
        if domain_exists == False:
            Domain_Id = dnspod.create_domain(Login_Token, domain['name'])
        pass
    except Exception as e:
        logging.error(u"初始化域名失败")
        pass

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
    try:
        response = urllib2.urlopen(r'http://ip.taobao.com/outGetIpInfo?ip=myip&accessKey=alibaba-inc').read().decode('utf-8')
        data = json.loads(response)
        LocalIP = data['data']['ip']
        pass
    except Exception as e:
        logging.error(u"获取本机IP失败")
        pass

def get_host_ip(domain):
    global HostIP
    global Domain_Id
    try:
        HostIP = dnspod.get_record_value(Login_Token, Domain_Id, domain['sub_domains'][0])
        pass
    except Exception as e:
        logging.error(u"获取远程IP失败")
        pass

    
if __name__ == '__main__':
    global Login_Token
    
    logger.setup_logging()
    conf = json.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "conf.json"), "r"))
    Login_Token = "%s,%s" % (conf['id'], conf['token'])
    Domains = conf['domains']
    
    try:
        get_ip()
        for domain in Domains:
            init_domain(domain)
            get_host_ip(domain)
            if HostIP != LocalIP:
                logging.info("Begin update [%s]." % domain['name'])
                ddns(domain)
        pass
    except Exception as e:
        logging.error(e)
        pass
