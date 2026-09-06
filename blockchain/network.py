import requests

from blockchain.block import Block
from blockchain.chain import Blockchain


class Network:
    def __init__(self):
        self.peers = set()

    def add_peer(self, peer):
        if peer:
            self.peers.add(peer)
        return list(self.peers)

    def broadcast_block(self, block):
        for peer in self.peers:
            try:
                requests.post(
                    f"http://{peer}/receive_block",
                    json=block.to_dict(),
                    timeout=3,
                )
            except requests.RequestException:
                continue

    def sync_chain(self, blockchain):
        best_chain = blockchain.chain

        for peer in self.peers:
            try:
                response = requests.get(f"http://{peer}/chain", timeout=3)
                if response.status_code != 200:
                    continue

                peer_chain = Blockchain.from_dict(
                    response.json(),
                    difficulty=blockchain.difficulty,
                )

                if len(peer_chain.chain) > len(best_chain) and peer_chain.is_valid():
                    best_chain = peer_chain.chain
            except requests.RequestException:
                continue

        if best_chain is not blockchain.chain:
            blockchain.chain = best_chain
            return True

        return False
