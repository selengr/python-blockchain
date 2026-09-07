class Wallet:
    @staticmethod
    def get_balance(blockchain, name):
        balance = 0

        for block in blockchain.chain:
            for transaction in block.transactions:
                if transaction.sender == name:
                    balance -= transaction.amount
                if transaction.receiver == name:
                    balance += transaction.amount

        return balance

    @staticmethod
    def get_balances(blockchain):
        balances = {}

        for block in blockchain.chain:
            for transaction in block.transactions:
                sender = transaction.sender
                receiver = transaction.receiver

                if sender not in balances:
                    balances[sender] = 0
                if receiver not in balances:
                    balances[receiver] = 0

                balances[sender] -= transaction.amount
                balances[receiver] += transaction.amount

        return balances
