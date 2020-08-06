from utils import reverse_bytes, calculate_merkle_root
import proof
import config

        
class Block:
    def __init__(self, txns, prev_block_hash):
        self.txns = txns
        self.nonce = 0
        self.hash = ""
        self.prev_block_hash = ""
        self.bits = config.bits
        self.merkle_root = self.get_merkle_root_hash()
        
    def update(self, prev_block_hash, txns, nonce):
        self.hash = "" 
        self.prev_block_hash = prev_block_hash
        self.txns = txns
        self.nonce = nonce
        self.merkle_root = get_merkle_root_hash()

    def get_serialized_block_header(self, nonce):
        serial = reverse_bytes(self.prev_block_hash) + 
                 reverse_bytes(self.merkle_root) + 
                 reverse_bytes(proof.Proof.target_threshold)
                 reverse_bytes(nonce)
        return serial

    def get_merkle_root_hash(self):
        txn_hash = [txn.txid for txn in self.txns]
        return calculate_merkle_root(txn_hash, arity)

    @staticmethod
    def create_genesis_block(coinbase_txn):
        block = Block()
        block.update("0"*64, [coinbase_txn], 0)

        # mine proof of work of block
        return block

