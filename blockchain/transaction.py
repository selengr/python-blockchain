class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def to_dict(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
        }

    @staticmethod
    def from_dict(data):
        return Transaction(
            data["sender"],
            data["receiver"],
            data["amount"],
        )
