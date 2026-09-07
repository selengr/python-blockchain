import sys

from blockchain.transaction import Transaction
from blockchain.chain import Blockchain
from blockchain.wallet import Wallet


def run_demo():
    chain = Blockchain(difficulty=3)

    chain.mine_pending("Reza")

    chain.add_transaction(Transaction("Reza", "Bobi", 10))
    chain.add_transaction(Transaction("Bobi", "Charlie", 4))
    chain.mine_pending("Reza")

    chain.add_transaction(Transaction("Charlie", "Mahsa", 2))
    chain.mine_pending("Mahsa")

    for block in chain.chain:
        print("Block:", block.index)
        print("Hash:", block.hash)
        print("Previous hash:", block.previous_hash)
        print("Nonce:", block.nonce)
        print("Transactions:", [tx.to_dict() for tx in block.transactions])
        print()

    print("Chain valid:", chain.is_valid())
    print("Balances:", Wallet.get_balances(chain))


def run_node(port=5000):
    from blockchain.app import app
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "node":
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
        run_node(port)
    else:
        run_demo()
