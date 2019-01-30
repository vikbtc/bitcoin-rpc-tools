#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from bitcoin import rpc
from tabulate import tabulate


def main():
    proxy = rpc.RawProxy()
    utxos = proxy.listunspent()
    balances = {}
    total = 0
    for utxo in utxos:
        address = utxo['address']
        amount = utxo['amount']
        label = utxo['label']
        data = balances.setdefault(address, {})
        # get location, if specified
        data['label'], data['loc'] = label.split('@') if '@' in label else (label, None)
        data['first_in'] = min(get_tx_time(proxy, utxo['txid']), data.get('first_in', datetime.max))
        data['count'] = data.get('count', 0) + 1
        data['balance'] = data.get('balance', 0) + amount
        total += amount
    rows = []
    for address, data in balances.items():
        rows.append([
            address,
            data.get('label'),
            data.get('loc'),
            data.get('balance'),
            data.get('first_in'),
            data.get('count'),
        ])
    # sort by label
    rows.sort(key=lambda x: x[1])
    rows.append(['Total', '', '', total, '', ''])
    print(tabulate(rows, headers=['Address', 'Label', 'Location', 'Balance', 'First In', 'Count']))


def get_tx_time(proxy, tx_hash):
    tx = proxy.gettransaction(tx_hash)
    return datetime.fromtimestamp(tx['blocktime'])


if __name__ == "__main__":
    main()
