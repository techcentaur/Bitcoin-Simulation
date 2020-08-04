from utils import reverse_bytes

import proof

class Block:
    def __init__(self):
        self.prev_block_hash = None
        self.txn_pool = []

    def add_txn(self, txn):
        self.txn_pool.append(txn)

    def get_serialized_block_header(self, nonce):
        serial = reverse_bytes(self.prev_hash) + 
                 reverse_bytes(self.get_merkle_root_hash()) + 
                 reverse_bytes(proof.Proof.target_threshold)
                 reverse_bytes(nonce)
        return serial

    def get_merkle_root_hash(self):
        root_hash = ""
        return root_hash
