Bitcoin RPC Tools
======

Command line tools for your [Bitcoin Core](https://bitcoincore.org/) node.

## Installation

1. Install [python3](https://www.python.org/) and [virtualenv](https://virtualenv.pypa.io/en/latest/)

2. Set up a virtualenv with `virtualenv -p python3 --no-site-packages venv` and `. venv/bin/activate`

3. Install the dependencies using `pip install -r requirements.txt`.

## balance.py

Get balances by wallet address. An optional @ in the label can be added to specify the location. 
For example, to add watch-only addresses to your node:

```text
bitcoin-cli importaddress "15ZeP1vxvGCNyPZsuE8yLp8FE5HrG1XCTW" "Cold Wallet@Paper" false
bitcoin-cli importaddress "1BvrhdTvGxxjFG45qJPX7ktAMfGrzhwNWZ" "Hot Wallet@Trezor" false
bitcoin-cli rescanblockchain
```

Output:

```text
> python balance.py

Address                             Label        Location      Balance  First In             Count
----------------------------------  -----------  ----------  ---------  -------------------  -------
15ZeP1vxvGCNyPZsuE8yLp8FE5HrG1XCTW  Cold Wallet  Paper            0.01  2019-01-27 13:09:44  1
1BvrhdTvGxxjFG45qJPX7ktAMfGrzhwNWZ  Hot Wallet   Trezor           0.02  2019-01-27 12:39:38  1
Total                                                             0.03
```