#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

import requests
from bitcoin import rpc
from tabulate import tabulate


def main():
    proxy = rpc.RawProxy()
    peers = proxy.getpeerinfo()

    rows = []
    for peer in peers:
        user_agent = clean_user_agent(peer['subver'])
        ip = peer['addr']
        in_out = 'In' if peer['inbound'] else 'Out'
        ip_info = _get_ip_info(ip)
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


def _get_ip_info(ip):
    clean_ip = None
    pattern = re.compile('^(\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}):\\d+$')
    match = pattern.match(ip)
    if match:
        clean_ip = match.group(1)
    # TODO - IPv6 support

    if clean_ip:
        url = 'https://ipinfo.io/{}/json'.format(clean_ip)
        return requests.get(url).json() or {}
    else:
        return {}


def clean_user_agent(user_agent):
    pattern = re.compile('^/(.+)/$')
    match = pattern.match(user_agent)
    return match.group(1) if match else user_agent


if __name__ == "__main__":
    main()
