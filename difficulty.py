#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bitcoin import rpc
from tabulate import tabulate

from util import ts_to_datetime, DIFFICULTY_RESET_BLOCKS


def main():
    proxy = rpc.RawProxy()
    current_height = proxy.getblockchaininfo()['blocks']
    height = 0
    rows = []
    prev_difficulty = 0
    while height < current_height:
        block_hash = proxy.getblockhash(height)
        block = proxy.getblock(block_hash)
        block_time = ts_to_datetime(block['time'])
        difficulty = block['difficulty']
        change_percent = (difficulty - prev_difficulty) * 100 / prev_difficulty if prev_difficulty else 0
        rows.append([height, block_time, int(difficulty), round(change_percent, 2)])
        height += DIFFICULTY_RESET_BLOCKS
        prev_difficulty = difficulty
    headers = ['Height', 'Block Time', 'Difficulty', 'Change (%)']
    print(tabulate(rows, headers=headers))


if __name__ == "__main__":
    main()
