from utils import reverse_bytes, calculate_merkle_root
import proof

        
class Block:
    def __init__(self):
        self.txn_pool = []
        self.nonce = 0
        self.hash = ""
        self.prev_block_hash = ""
        self.merkle_root = get_merkle_root_hash()
        # self.prev_block = None
        self.waiting_txn_pool = []

    def update(self, _hash, prev_block_hash, txns, nonce):
        self.hash = _hash 
        self.prev_block_hash = prev_block_hash
        self.txn_pool = txns
        self.nonce = nonce
        self.merkle_root = get_merkle_root_hash()

    def add_txn(self, txn):
        self.txn_pool.append(txn)

    def get_serialized_block_header(self, nonce):
        serial = reverse_bytes(self.prev_block_hash) + 
                 reverse_bytes(self.merkle_root) + 
                 reverse_bytes(proof.Proof.target_threshold)
                 reverse_bytes(nonce)
        return serial

    def get_merkle_root_hash(self):
        txn_hash = [txn.txid for txn in self.txn_pool]
        root_hash = calculate_merkle_root(txn_hash, arity)

    @staticmethod
    def create_genesis_block(coinbase_txn):
        block = Block()
        block.update("", "0"*64, [coinbase_txn], 0)

        # mine proof of work of block
        return block

