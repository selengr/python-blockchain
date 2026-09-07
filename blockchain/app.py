import os

from flask import Flask, jsonify, request, send_from_directory

from blockchain.block import Block
from blockchain.chain import Blockchain
from blockchain.network import Network
from blockchain.storage import Storage
from blockchain.transaction import Transaction
from blockchain.wallet import Wallet


DATA_FILE = "chain_data.json"
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

network = Network()
app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="/static")

loaded = Storage.load(DATA_FILE)
blockchain = loaded if loaded is not None else Blockchain(difficulty=3)


def save_chain():
    return Storage.save(blockchain, DATA_FILE)


@app.route("/")
def home():
    return send_from_directory(STATIC_DIR, "index.html")


@app.route("/chain", methods=["GET"])
def get_chain():
    return jsonify(blockchain.to_dict())


@app.route("/pending", methods=["GET"])
def get_pending():
    return jsonify([tx.to_dict() for tx in blockchain.pending_transactions])


@app.route("/transaction", methods=["POST"])
def create_transaction():
    data = request.get_json(silent=True) or {}
    sender = data.get("sender")
    receiver = data.get("receiver")
    amount = data.get("amount")

    if sender is None or receiver is None or amount is None:
        return jsonify({"message": "sender, receiver and amount are required"}), 400

    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return jsonify({"message": "amount must be a number"}), 400

    transaction = Transaction(sender, receiver, amount)
    error = blockchain.add_transaction(transaction)

    if error:
        return jsonify({"message": error}), 400

    save_chain()
    return jsonify({
        "message": "transaction added to pending list",
        "transaction": transaction.to_dict(),
        "pending_count": len(blockchain.pending_transactions),
    })


@app.route("/mine", methods=["POST"])
def mine_block():
    data = request.get_json(silent=True) or {}
    miner = data.get("miner", "miner")

    block = blockchain.mine_pending(miner)
    network.broadcast_block(block)
    save_chain()

    return jsonify({
        "message": "block mined",
        "miner": miner,
        "reward": blockchain.mining_reward,
        "block": block.to_dict(),
    })


@app.route("/balance/<name>", methods=["GET"])
def get_balance(name):
    return jsonify({
        "name": name,
        "balance": Wallet.get_balance(blockchain, name),
    })


@app.route("/balances", methods=["GET"])
def get_balances():
    return jsonify(Wallet.get_balances(blockchain))


@app.route("/receive_block", methods=["POST"])
def receive_block():
    data = request.get_json()
    if not data:
        return jsonify({"message": "invalid data"}), 400

    block = Block.from_dict(data)
    accepted = blockchain.add_block(block)

    if not accepted:
        return jsonify({"message": "block rejected"}), 400

    save_chain()
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
    if updated:
        save_chain()
    return jsonify({
        "message": "chain updated" if updated else "already up to date",
        "length": len(blockchain.chain),
    })


@app.route("/valid", methods=["GET"])
def is_valid():
    return jsonify({"valid": blockchain.is_valid()})


@app.route("/save", methods=["POST"])
def save_now():
    path = save_chain()
    return jsonify({"message": "chain saved", "file": path})
