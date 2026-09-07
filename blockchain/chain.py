from blockchain.block import Block
from blockchain.transaction import Transaction


class Blockchain:
    def __init__(self, difficulty=3, mining_reward=1):
        self.difficulty = difficulty
        self.mining_reward = mining_reward
        self.pending_transactions = []
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, [], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        if not transaction.sender or not transaction.receiver:
            return "sender and receiver are required"

        if transaction.amount <= 0:
            return "amount must be greater than 0"

        if transaction.sender != "network":
            from blockchain.wallet import Wallet

            balance = Wallet.get_balance(self, transaction.sender)
            pending_spent = sum(
                tx.amount
                for tx in self.pending_transactions
                if tx.sender == transaction.sender
            )
            available = balance - pending_spent

            if available < transaction.amount:
                return (
                    f"not enough balance: {transaction.sender} has {available}, "
                    f"tried to send {transaction.amount}"
                )

        self.pending_transactions.append(transaction)
        return None

    def mine_pending(self, miner):
        reward = Transaction("network", miner, self.mining_reward)
        transactions = self.pending_transactions + [reward]

        previous_block = self.get_latest_block()
        new_block = Block(
            previous_block.index + 1,
            transactions,
            previous_block.hash,
        )
        new_block.mine(self.difficulty)
        self.chain.append(new_block)
        self.pending_transactions = []
        return new_block

    def add_block(self, block):
        latest = self.get_latest_block()

        if block.previous_hash != latest.hash:
            return False

        if block.hash != block.calculate_hash():
            return False

        if not block.hash.startswith("0" * self.difficulty):
            return False

        self.chain.append(block)
        return True

    def is_valid(self):
        for index in range(1, len(self.chain)):
            current = self.chain[index]
            previous = self.chain[index - 1]

            if current.hash != current.calculate_hash():
                return False

            if current.previous_hash != previous.hash:
                return False

            if not current.hash.startswith("0" * self.difficulty):
                return False

        return True

    def replace_chain(self, new_blocks):
        if len(new_blocks) <= len(self.chain):
            return False

        old_chain = self.chain
        self.chain = new_blocks

        if not self.is_valid():
            self.chain = old_chain
            return False

        return True

    def to_dict(self):
        return [block.to_dict() for block in self.chain]

    @staticmethod
    def from_dict(data, difficulty=3, mining_reward=1):
        blockchain = Blockchain(difficulty=difficulty, mining_reward=mining_reward)
        blockchain.chain = [Block.from_dict(block) for block in data]
        return blockchain
