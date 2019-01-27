#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

import bitcoin.rpc as rpc
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
        data = balances.get(address, {})
        # get location, if specified
        data['label'], data['loc'] = label.split('@') if '@' in label else (label, None)
        data['balance'] = data.get('balance', 0) + amount
        tx_time = get_tx_time(proxy, utxo['txid'])
        data['first_in'] = tx_time if not data.get('first_in') else min(tx_time, data.get('first_in'))
        data['count'] = data.get('count', 0) + 1
        balances[address] = data
        total += amount
    rows = []
    for address, data in balances.items():
        rows.append([
            address,
            data.get('label'),
            data.get('loc'),
            data.get('balance'),
            datetime.fromtimestamp(data.get('first_in')),
            data.get('count'),
        ])
    # sort by label
    rows.sort(key=lambda x: x[1])
    rows.append(['Total', '', '', total, '', ''])
    print(tabulate(rows, headers=['Address', 'Label', 'Location', 'Balance', 'First In', 'Count']))


def get_tx_time(proxy, tx_hash):
    tx = proxy.gettransaction(tx_hash)
    return tx['blocktime']


if __name__ == "__main__":
    main()
