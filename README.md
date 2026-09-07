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
  network.py      - talk to other nodes
  app.py          - simple Flask API
  run.py          - start demo or node
```

## How to install

From the project folder:

```bash
pip3 install -r requirements.txt
```

## How to run the demo

```bash
PYTHONPATH=. python3 blockchain/run.py
```

This will:
1. give Reza a mining reward
2. send coins step by step
3. print every block
4. print balances

## How to run a node

```bash
PYTHONPATH=. python3 blockchain/run.py node 5000
```

Another node:

```bash
PYTHONPATH=. python3 blockchain/run.py node 5001
```

## Simple API examples

Add a transaction to the pending list:

```bash
curl -X POST http://localhost:5000/transaction \
  -H "Content-Type: application/json" \
  -d '{"sender":"Reza","receiver":"Bobi","amount":10}'
```

See pending transactions:

```bash
curl http://localhost:5000/pending
```

Mine pending transactions (miner gets a reward):

```bash
curl -X POST http://localhost:5000/mine \
  -H "Content-Type: application/json" \
  -d '{"miner":"Reza"}'
```

Get the chain:

```bash
curl http://localhost:5000/chain
```

Check one balance:

```bash
curl http://localhost:5000/balance/Reza
```

See all balances:

```bash
curl http://localhost:5000/balances
```

Add a peer and sync:

```bash
curl -X POST http://localhost:5000/add_peer \
  -H "Content-Type: application/json" \
  -d '{"peer":"localhost:5001"}'

curl http://localhost:5000/sync
```

Check if the chain is valid:

```bash
curl http://localhost:5000/valid
```

## How it works

1. A transaction waits in the pending list.
2. Mining puts pending transactions into a new block.
3. The miner also gets a small reward.
4. Each block has a hash and points to the previous block.
5. Wallet balances are calculated from all transactions in the chain.

That is the main idea.
Keep it simple and keep learning.
