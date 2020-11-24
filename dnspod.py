#!/usr/bin/python
# -*- coding: UTF-8 -*-
import httplib 
import urllib
import json, os, logging
import logger

Headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json"}

def get_domain_id(login_token, domain_name):
    conn = httplib.HTTPSConnection("dnsapi.cn")
    params = dict(
        login_token=login_token,
        format="json"
    )
    conn.request("POST", "/Domain.List", urllib.urlencode(params), Headers)
    response = conn.getresponse()
    data = json.loads(response.read())

    if int(data['status']['code']) == 1:
        domails = data['domains']
        for domain in domails:
            if domain['name'] == domain_name:
                return domain['id']
        return 0
    else:
        return 0

    conn.close()


def create_domain(login_token, domain_name):
    conn = httplib.HTTPSConnection("dnsapi.cn")
    params = dict(
        login_token=login_token,
        format="json",
        domain = domain_name
    )
    conn.request("POST", "/Domain.Create", urllib.urlencode(params), Headers)
    response = conn.getresponse()
    data = json.loads(response.read())

    if int(data['status']['code']) == 1:
        return data['domain']['id']

    conn.close()


def get_record_value(login_token, domain_id, sub_domain):
    conn = httplib.HTTPSConnection("dnsapi.cn")
    params = dict(
        login_token=login_token,
        format="json",
        domain_id = domain_id,
        sub_domain = sub_domain
    )
    conn.request("POST", "/Record.List", urllib.urlencode(params), Headers)
    response = conn.getresponse()
    data = json.loads(response.read())

    if int(data['status']['code']) == 1:
        records = data['records']
        for record in records:
            if record['type'] == 'A' and record['name'] == sub_domain:
                return record['value']
        return "127.0.0.1"
    else:
        return "127.0.0.1"

    conn.close()


def get_record_id(login_token, domain_id, sub_domain):
    conn = httplib.HTTPSConnection("dnsapi.cn")
    params = dict(
        login_token=login_token,
        format="json",
        domain_id = domain_id,
        sub_domain = sub_domain
    )
    conn.request("POST", "/Record.List", urllib.urlencode(params), Headers)
    response = conn.getresponse()
    data = json.loads(response.read())

    if int(data['status']['code']) == 1:
        records = data['records']
        for record in records:
            if record['type'] == 'A' and record['name'] == sub_domain:
                return record['id']
        return 0
    else:
        return 0

    conn.close()


def create_record_id(login_token, domain_id, sub_domain, localIP):
    conn = httplib.HTTPSConnection("dnsapi.cn")
    params = dict(
        login_token=login_token,
        format="json",
        domain_id = domain_id,
        sub_domain = sub_domain,
        record_type = 'A',
        record_line_id = "0",
        value = localIP
    )
    conn.request("POST", "/Record.Create", urllib.urlencode(params), Headers)
    response = conn.getresponse()
    data = json.loads(response.read())

    if int(data['status']['code']) == 1:
        logging.info("Sub_domain [%s] create success" % sub_domain)
    else:
        logging.error("Sub_domain [%s] create failed" % sub_domain)
    conn.close()


def record_ddns(login_token, domain_id, record_id, sub_domain, localIP):
    conn = httplib.HTTPSConnection("dnsapi.cn")
    params = dict(
        login_token=login_token,
        format="json",
        domain_id = domain_id,
        record_id = record_id,
        sub_domain = sub_domain,
        record_line_id = "0",
        value = localIP
    )

    conn.request("POST", "/Record.Ddns", urllib.urlencode(params), Headers)
    response = conn.getresponse()
    data = json.loads(response.read())

    if int(data['status']['code']) == 1:
        logging.info("DDns Success for subdomain [%s], IP change to %s" % (sub_domain, localIP))
    else:
        logging.error("DDns Error for subdomain [%s]: %s" % (sub_domain, data['status']['message']))

    conn.close()
