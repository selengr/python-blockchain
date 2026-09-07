import argparse
import json
import sys

from blockchain.chain import Blockchain
from blockchain.storage import Storage, DEFAULT_FILE
from blockchain.transaction import Transaction
from blockchain.wallet import Wallet


def get_chain(path):
    loaded = Storage.load(path)
    if loaded is not None:
        return loaded
    return Blockchain(difficulty=3, mining_reward=50)


def print_json(data):
    print(json.dumps(data, indent=2))


def cmd_demo(_args):
    from blockchain.run import run_demo
    run_demo()


def cmd_node(args):
    from blockchain.run import run_node
    run_node(args.port)


def cmd_mine(args):
    chain = get_chain(args.file)
    block = chain.mine_pending(args.miner)
    Storage.save(chain, args.file)
    print("Miner:", args.miner)
    print("Reward:", chain.mining_reward)
    print("Hash:", block.hash)


def cmd_send(args):
    chain = get_chain(args.file)
    transaction = Transaction(args.sender, args.receiver, args.amount)
    error = chain.add_transaction(transaction)

    if error:
        print("Transaction rejected:", error)
        sys.exit(1)

    Storage.save(chain, args.file)
    print("Transaction added to pending list.")
    print_json(transaction.to_dict())


def cmd_pending(args):
    chain = get_chain(args.file)
    print_json([tx.to_dict() for tx in chain.pending_transactions])


def cmd_chain(args):
    chain = get_chain(args.file)
    print_json(chain.to_dict())


def cmd_balance(args):
    chain = get_chain(args.file)
    print(args.name, Wallet.get_balance(chain, args.name))


def cmd_balances(args):
    chain = get_chain(args.file)
    print_json(Wallet.get_balances(chain))


def cmd_valid(args):
    chain = get_chain(args.file)
    print("valid:", chain.is_valid())


def cmd_save(args):
    chain = get_chain(args.file)
    path = Storage.save(chain, args.file)
    print("saved:", path)


def build_parser():
    parser = argparse.ArgumentParser(
        description="Simple commands for this learning blockchain."
    )
    parser.add_argument(
        "--file",
        default=DEFAULT_FILE,
        help="JSON file used to save and load the chain",
    )

    sub = parser.add_subparsers(dest="command")
    sub.required = True

    demo = sub.add_parser("demo", help="run the local demo")
    demo.set_defaults(func=cmd_demo)

    node = sub.add_parser("node", help="start the Flask node")
    node.add_argument("--port", type=int, default=5000)
    node.set_defaults(func=cmd_node)

    mine = sub.add_parser("mine", help="mine pending transactions")
    mine.add_argument("--miner", default="miner")
    mine.set_defaults(func=cmd_mine)

    send = sub.add_parser("send", help="add a pending transaction")
    send.add_argument("sender")
    send.add_argument("receiver")
    send.add_argument("amount", type=float)
    send.set_defaults(func=cmd_send)

    pending = sub.add_parser("pending", help="show pending transactions")
    pending.set_defaults(func=cmd_pending)

    chain_cmd = sub.add_parser("chain", help="show the full chain")
    chain_cmd.set_defaults(func=cmd_chain)

    balance = sub.add_parser("balance", help="show one balance")
    balance.add_argument("name")
    balance.set_defaults(func=cmd_balance)

    balances = sub.add_parser("balances", help="show all balances")
    balances.set_defaults(func=cmd_balances)

    valid = sub.add_parser("valid", help="check if the chain is valid")
    valid.set_defaults(func=cmd_valid)

    save = sub.add_parser("save", help="save the chain to JSON")
    save.set_defaults(func=cmd_save)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
