#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import re
import tempfile

import requests
from bitcoin import rpc
from tabulate import tabulate


def main():
    token = os.environ.get('IP_INFO_IO_TOKEN')
    proxy = rpc.RawProxy()
    peers = proxy.getpeerinfo()

    rows = []
    for peer in peers:
        user_agent = clean_user_agent(peer['subver'])
        ip = peer['addr']
        in_out = 'In' if peer['inbound'] else 'Out'
        ip_info = _get_ip_info(ip, token)
        country = ip_info.get('country')
        region = ip_info.get('region')
        city = ip_info.get('city')
        org = ip_info.get('org')
        rows.append([
            ip,
            user_agent,
            in_out,
            country,
            region,
            city,
            org,
        ])
    headers = ['IP', 'User Agent', 'I/O', 'Cn', 'Region', 'City', 'Org']
    print(tabulate(rows, headers=headers))


def _get_ip_info(ip, token):
    clean_ip = None
    # IPv4
    pattern = re.compile('^(\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}):\\d+$')
    match = pattern.match(ip)
    if match:
        clean_ip = match.group(1)
        if clean_ip.startswith('127.'):  # ignore localhost
            clean_ip = None
    # IPv6
    pattern = re.compile('^\\[(.+)\\]:\\d+$')
    match = pattern.match(ip)
    if match:
        clean_ip = match.group(1)

    if clean_ip:
        cache = os.path.join(tempfile.gettempdir(), clean_ip)
        if os.path.exists(cache):
            with open(cache, 'r') as file:
                data = json.load(file)
        else:
            url = 'https://ipinfo.io/{}/json'.format(clean_ip)
            if token:
                url += '?token={}'.format(token)
            data = requests.get(url).json() or {}
            with open(cache, 'w') as outfile:
                json.dump(data, outfile, indent=2, sort_keys=True)
        return data
    else:
        return {}


def clean_user_agent(user_agent):
    pattern = re.compile('^/(.+)/$')
    match = pattern.match(user_agent)
    return match.group(1) if match else user_agent


if __name__ == "__main__":
    main()
