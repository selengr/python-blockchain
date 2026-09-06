# Simple Python Blockchain

This is a small blockchain project in Python.
I made it to understand the basic ideas of blockchain in a clear way.

It is not a real crypto coin.
It is just for learning.

## What is inside

- `transaction.py` - send coins from one person to another
- `block.py` - one block with data, hash, and mining
- `chain.py` - the full chain of blocks
- `network.py` - talk to other nodes (peers)
- `app.py` - simple API with Flask
- `run.py` - start the demo or the node

## How to install

From the project folder:

```bash
pip3 install -r requirements.txt
```

## How to run the demo

This mines a few blocks and prints the chain:

```bash
PYTHONPATH=. python3 blockchain/run.py
```

You should see each block, its hash, and if the chain is valid.

## How to run a node

Start one node on port 5000:

```bash
PYTHONPATH=. python3 blockchain/run.py node 5000
```

You can start another node on another port if you want:

```bash
PYTHONPATH=. python3 blockchain/run.py node 5001
```

## Simple API examples

Get the chain:

```bash
curl http://localhost:5000/chain
```

Mine a new block:

```bash
curl -X POST http://localhost:5000/mine \
  -H "Content-Type: application/json" \
  -d '{"sender":"Reza","receiver":"Bobi","amount":10}'
```

Add a peer:

```bash
curl -X POST http://localhost:5000/add_peer \
  -H "Content-Type: application/json" \
  -d '{"peer":"localhost:5001"}'
```

Sync the chain from peers:

```bash
curl http://localhost:5000/sync
```

Check if the chain is valid:

```bash
curl http://localhost:5000/valid
```

## Simple idea

1. A transaction says who sends, who receives, and how much.
2. Transactions go into a block.
3. The block gets a hash.
4. Mining finds a hash that starts with zeros.
5. Each block points to the previous block hash.
6. That link is what makes the chain hard to change.

That is the main idea.
Keep it simple and keep learning.
