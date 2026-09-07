# Simple Python Blockchain

This is a small blockchain project in Python.
I made it to understand the basic ideas of blockchain in a clear way.

It is not a real crypto coin.
It is just for learning.

Repo: https://github.com/selengr/python-blockchain

## Project structure

```
blockchain/
  transaction.py  - one payment from sender to receiver
  block.py        - one block with hash and mining
  chain.py        - the chain + pending transactions
  wallet.py       - read balances from the chain
  storage.py      - save and load the chain as JSON
  network.py      - talk to other nodes
  app.py          - simple Flask API
  cli.py          - simple commands in the terminal
  run.py          - start demo or node
  static/         - tiny web page
tests/
  test_basic.py   - light tests for the main ideas
```

## How to install

From the project folder:

```bash
pip3 install -r requirements.txt
```

## Short commands

```bash
make demo
make test
make node
```

`make node` starts the app, then open http://localhost:5000/

## How to run the demo

```bash
PYTHONPATH=. python3 blockchain/run.py
```

Or with the CLI:

```bash
PYTHONPATH=. python3 blockchain/cli.py demo
```

## Simple CLI

Mine a reward block:

```bash
PYTHONPATH=. python3 blockchain/cli.py mine --miner Reza
```

Send coins (goes to pending first):

```bash
PYTHONPATH=. python3 blockchain/cli.py send Reza Bobi 10
PYTHONPATH=. python3 blockchain/cli.py mine --miner Reza
```

Check things:

```bash
PYTHONPATH=. python3 blockchain/cli.py pending
PYTHONPATH=. python3 blockchain/cli.py chain
PYTHONPATH=. python3 blockchain/cli.py balance Reza
PYTHONPATH=. python3 blockchain/cli.py balances
PYTHONPATH=. python3 blockchain/cli.py valid
```

The chain is saved in `chain_data.json` in the project folder.

## How to run a node

```bash
PYTHONPATH=. python3 blockchain/cli.py node --port 5000
```

Or:

```bash
PYTHONPATH=. python3 blockchain/run.py node 5000
```

Then open this in your browser:

```text
http://localhost:5000/
```

On that tiny page you can:
- send coins
- mine pending transactions
- see balances, pending list, and the chain

The node also loads and saves `chain_data.json`.

## Run the light tests

```bash
PYTHONPATH=. python3 -m unittest tests.test_basic -v
```

## Simple API examples

Add a transaction to the pending list:

```bash
curl -X POST http://localhost:5000/transaction \
  -H "Content-Type: application/json" \
  -d '{"sender":"Reza","receiver":"Bobi","amount":10}'
```

Mine pending transactions:

```bash
curl -X POST http://localhost:5000/mine \
  -H "Content-Type: application/json" \
  -d '{"miner":"Reza"}'
```

Useful reads:

```bash
curl http://localhost:5000/chain
curl http://localhost:5000/pending
curl http://localhost:5000/balance/Reza
curl http://localhost:5000/balances
curl http://localhost:5000/valid
```

## How it works

1. A transaction waits in the pending list.
2. Mining puts pending transactions into a new block.
3. The miner also gets a small reward.
4. Each block has a hash and points to the previous block.
5. Wallet balances are calculated from all transactions in the chain.
6. The chain can be saved to a JSON file and loaded again later.

That is the main idea.
Keep it simple and keep learning.
