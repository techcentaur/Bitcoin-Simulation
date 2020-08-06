from utils import reverse_bytes, calculate_merkle_root
import proof

        
class Block:
    def __init__(self):
        self.prev_block_hash = None
        self.txns = []
        self.nonce = None
        self.hash = None
        self.prev_block = None

    def add_txn(self, txn):
        self.txn_pool.append(txn)

    def get_serialized_block_header(self, nonce):
        serial = reverse_bytes(self.prev_block_hash) + 
                 reverse_bytes(self.get_merkle_root_hash()) + 
                 reverse_bytes(proof.Proof.target_threshold)
                 reverse_bytes(nonce)
        return serial

    def get_merkle_root_hash(self):
        txn_hash = [txn.txid for txn in self.txns]
        root_hash = calculate_merkle_root(txn_hash, arity)

    def create_genesis_block(self):
        pass