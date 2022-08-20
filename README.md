# MasterChef

Farming contract for minted Narfex Token.
Distributes a reward from the balance instead of minting it.

## Install Dependencies

Delete previous node_modules and type:

`npm i`

## Preparing local node

We need brownie and ganache installed, then:

`brownie compile`

`brownie console`

## Run tests

Open second terminal and type:

All tests - `brownie test -s`

Target test - `brownie test -s -k test_account_balance`, test_account_balance is your test name from test_contract.py
