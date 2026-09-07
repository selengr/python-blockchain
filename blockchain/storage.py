import json
import os

from blockchain.chain import Blockchain
from blockchain.transaction import Transaction


DEFAULT_FILE = "chain_data.json"


class Storage:
    @staticmethod
    def save(blockchain, path=DEFAULT_FILE):
        data = {
            "difficulty": blockchain.difficulty,
            "mining_reward": blockchain.mining_reward,
            "pending_transactions": [
                tx.to_dict() for tx in blockchain.pending_transactions
            ],
            "chain": blockchain.to_dict(),
        }

        with open(path, "w") as file:
            json.dump(data, file, indent=2)

        return path

    @staticmethod
    def load(path=DEFAULT_FILE):
        if not os.path.exists(path):
            return None

        with open(path, "r") as file:
            data = json.load(file)

        blockchain = Blockchain.from_dict(
            data.get("chain", []),
            difficulty=data.get("difficulty", 3),
            mining_reward=data.get("mining_reward", 1),
        )
        blockchain.pending_transactions = [
            Transaction.from_dict(tx)
            for tx in data.get("pending_transactions", [])
        ]
        return blockchain
