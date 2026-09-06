from flask import Flask, jsonify, request

from blockchain.block import Block
from blockchain.chain import Blockchain
from blockchain.network import Network
from blockchain.transaction import Transaction


blockchain = Blockchain(difficulty=3)
network = Network()
app = Flask(__name__)


@app.route("/chain", methods=["GET"])
def get_chain():
    return jsonify(blockchain.to_dict())


@app.route("/mine", methods=["POST"])
def mine_block():
    data = request.get_json(silent=True) or {}
    sender = data.get("sender", "network")
    receiver = data.get("receiver", "miner")
    amount = data.get("amount", 1)

    transaction = Transaction(sender, receiver, amount)
    block = blockchain.add_block([transaction])
    network.broadcast_block(block)

    return jsonify({
        "message": "block mined",
        "block": block.to_dict(),
    })


@app.route("/receive_block", methods=["POST"])
def receive_block():
    data = request.get_json()
    if not data:
        return jsonify({"message": "invalid data"}), 400

    block = Block.from_dict(data)
    latest = blockchain.get_latest_block()

    if block.previous_hash != latest.hash:
        return jsonify({"message": "previous hash does not match"}), 400

    if block.hash != block.calculate_hash():
        return jsonify({"message": "invalid block hash"}), 400

    if not block.hash.startswith("0" * blockchain.difficulty):
        return jsonify({"message": "proof of work is invalid"}), 400

    blockchain.chain.append(block)
    return jsonify({"message": "block received"})


@app.route("/add_peer", methods=["POST"])
def add_peer():
    data = request.get_json() or {}
    peer = data.get("peer")

    if not peer:
        return jsonify({"message": "peer is required"}), 400

    peers = network.add_peer(peer)
    return jsonify({
        "message": "peer added",
        "peers": peers,
    })


@app.route("/peers", methods=["GET"])
def get_peers():
    return jsonify({"peers": list(network.peers)})


@app.route("/sync", methods=["GET"])
def sync_chain():
    updated = network.sync_chain(blockchain)
    return jsonify({
        "message": "chain updated" if updated else "already up to date",
        "length": len(blockchain.chain),
    })


@app.route("/valid", methods=["GET"])
def is_valid():
    return jsonify({"valid": blockchain.is_valid()})
