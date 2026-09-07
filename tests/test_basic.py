import os
import tempfile
import unittest

from blockchain.block import Block
from blockchain.chain import Blockchain
from blockchain.storage import Storage
from blockchain.transaction import Transaction
from blockchain.wallet import Wallet


class BasicBlockchainTests(unittest.TestCase):
    def test_block_hash_changes_when_data_changes(self):
        block = Block(1, [Transaction("A", "B", 5)], "0")
        first_hash = block.hash

        block.transactions.append(Transaction("B", "C", 1))
        second_hash = block.calculate_hash()

        self.assertNotEqual(first_hash, second_hash)

    def test_balance_after_reward_and_transfer(self):
        chain = Blockchain(difficulty=1, mining_reward=50)
        chain.mine_pending("Reza")

        self.assertEqual(Wallet.get_balance(chain, "Reza"), 50)

        added = chain.add_transaction(Transaction("Reza", "Bobi", 10))
        self.assertTrue(added)

        chain.mine_pending("Reza")

        self.assertEqual(Wallet.get_balance(chain, "Reza"), 90)
        self.assertEqual(Wallet.get_balance(chain, "Bobi"), 10)

    def test_invalid_spend_is_rejected(self):
        chain = Blockchain(difficulty=1, mining_reward=5)
        chain.mine_pending("Reza")

        added = chain.add_transaction(Transaction("Reza", "Bobi", 100))
        self.assertFalse(added)
        self.assertEqual(len(chain.pending_transactions), 0)

    def test_save_and_load_keeps_chain(self):
        chain = Blockchain(difficulty=1, mining_reward=20)
        chain.mine_pending("Reza")
        chain.add_transaction(Transaction("Reza", "Bobi", 5))
        chain.mine_pending("Reza")

        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "test_chain.json")
            Storage.save(chain, path)
            loaded = Storage.load(path)

            self.assertIsNotNone(loaded)
            self.assertEqual(len(loaded.chain), len(chain.chain))
            self.assertEqual(loaded.chain[-1].hash, chain.chain[-1].hash)
            self.assertTrue(loaded.is_valid())
            self.assertEqual(Wallet.get_balance(loaded, "Bobi"), 5)


if __name__ == "__main__":
    unittest.main()
