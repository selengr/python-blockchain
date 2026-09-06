from blockchain.block import Block


class Blockchain:
    def __init__(self, difficulty=3):
        self.difficulty = difficulty
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, [], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, transactions):
        previous_block = self.get_latest_block()
        new_block = Block(
            previous_block.index + 1,
            transactions,
            previous_block.hash,
        )
        new_block.mine(self.difficulty)
        self.chain.append(new_block)
        return new_block

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
    def from_dict(data, difficulty=3):
        blockchain = Blockchain(difficulty=difficulty)
        blockchain.chain = [Block.from_dict(block) for block in data]
        return blockchain
