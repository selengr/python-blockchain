# Simple Python Blockchain

Small blockchain I built in Python to learn how the basic pieces work.

This is **not** a real coin. Just a learning project.

Repo: https://github.com/selengr/python-blockchain

## What you can do

- mine blocks and get a reward
- send coins (they wait in a pending list until someone mines)
- check balances and if the chain is valid
- save / load the chain from a JSON file
- run a tiny web page or use the API

## Install

```bash
pip3 install -r requirements.txt
```

## Quick start

```bash
make demo   # run a short demo in the terminal
make test   # run the light tests
make node   # start the node, then open http://localhost:5000/
```

## Demo

```bash
PYTHONPATH=. python3 blockchain/run.py
```

Same thing with the CLI:

```bash
PYTHONPATH=. python3 blockchain/cli.py demo
```

## CLI

Mine a block (miner gets the reward):

```bash
PYTHONPATH=. python3 blockchain/cli.py mine --miner Reza
```

Send coins, then mine so they go into the chain:

```bash
PYTHONPATH=. python3 blockchain/cli.py send Reza Bobi 10
PYTHONPATH=. python3 blockchain/cli.py mine --miner Reza
```

Other useful commands:

```bash
PYTHONPATH=. python3 blockchain/cli.py pending
PYTHONPATH=. python3 blockchain/cli.py chain
PYTHONPATH=. python3 blockchain/cli.py balance Reza
PYTHONPATH=. python3 blockchain/cli.py balances
PYTHONPATH=. python3 blockchain/cli.py valid
```

Everything is saved in `chain_data.json` in the project folder.

## Web page + node

```bash
PYTHONPATH=. python3 blockchain/cli.py node --port 5000
```

Open http://localhost:5000/

From the page you can send coins, mine, and look at balances / pending / chain.

## API examples

```bash
curl -X POST http://localhost:5000/transaction \
  -H "Content-Type: application/json" \
  -d '{"sender":"Reza","receiver":"Bobi","amount":10}'

curl -X POST http://localhost:5000/mine \
  -H "Content-Type: application/json" \
  -d '{"miner":"Reza"}'

curl http://localhost:5000/chain
curl http://localhost:5000/pending
curl http://localhost:5000/balance/Reza
curl http://localhost:5000/balances
curl http://localhost:5000/valid
```

## Tests

```bash
PYTHONPATH=. python3 -m unittest tests.test_basic -v
```

Or just `make test`.

## Project files

```
blockchain/
  transaction.py  - one payment
  block.py        - one block + mining
  chain.py        - the chain and pending list
  wallet.py       - balances
  storage.py      - save / load JSON
  network.py      - talk to other nodes
  app.py          - Flask API
  cli.py          - terminal commands
  run.py          - demo or node
  static/         - tiny web page
tests/
  test_basic.py
```

## How it works

1. A send goes into the pending list.
2. Mining puts those pending transactions into a new block.
3. The miner also gets a reward.
4. Each block has a hash and links to the previous block.
5. Balances are calculated by walking through all transactions.
6. The chain can be saved to JSON and loaded later.
