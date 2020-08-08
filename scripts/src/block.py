from utils import reverse_bytes, calculate_merkle_root
import proof
import config

        
class Block:
    def __init__(self, txns=[], prev_block_hash=""):
        self.txns = txns
        self.nonce = 0
        self.hash = ""
        self.prev_block_hash = prev_block_hash
        self.bits = config.bits
        self.merkle_root = self.get_merkle_root_hash()
        
    def update(self, prev_block_hash, txns, nonce):
        self.hash = "" 
        self.prev_block_hash = prev_block_hash
        self.txns = txns
        self.nonce = nonce
        self.merkle_root = self.get_merkle_root_hash()

    def get_serialized_block_header(self, nonce):
        serial = reverse_bytes(self.prev_block_hash) + reverse_bytes(self.merkle_root)
        serial += reverse_bytes('0'*(len(hex(config.bits))%2) + hex(config.bits)[2:]) 
        serial += reverse_bytes('0'*(len(hex(nonce))%2)+ hex(nonce)[2:])
        return serial

    def get_merkle_root_hash(self):
        print(self.txns)
        txn_hash = [txn.txid for txn in self.txns]
        return calculate_merkle_root(txn_hash, config.arity)

    def create_copy(self):
        txn_copy = [txn.create_copy() for txn in self.txns]
        new_block = Block(txn_copy, self.prev_block_hash)
        new_block.nonce = self.nonce
        new_block.hash = self.hash
        new_block.bits = self.bits
        new_block.merkle_root = self.merkle_root

    @staticmethod
    def create_genesis_block(coinbase_txn):
        block = Block()
        block.update("0"*64, [coinbase_txn], 0)
        return block

