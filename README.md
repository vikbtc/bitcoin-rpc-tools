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

## difficulty.py

Displays a history of difficulty changes.

```text
> python difficulty.py

  Height  Block Time              Difficulty    Change (%)
--------  -------------------  -------------  ------------
       0  2009-01-03 13:15:05              1          0
    2016  2009-01-27 08:38:51              1          0
...
  556416  2018-12-31 12:20:09  5618595848853         10.03
  558432  2019-01-13 21:19:54  5883988430955          4.72
  560448  2019-01-28 01:35:13  5814661935891         -1.18
```


## peers.py

Get info on connected peer nodes.

```text
> python peers.py

IP                   User Agent        I/O    Cn    Region              City        Org
-------------------  ----------------  -----  ----  ------------------  ----------  --------------------------
95.173.211.242:8333  Satoshi:0.17.0    Out    CZ    Hlavni mesto Praha  Prague      AS49025 PRO-ZETA a.s.
52.14.64.82:8333     Satoshi:0.16.3    Out    US    Ohio                Ashley      AS16509 Amazon.com, Inc.
```