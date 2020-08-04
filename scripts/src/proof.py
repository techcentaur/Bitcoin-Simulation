import sys

class Work:
    def __init__(self, nonce, _hash):
        self.nonce = nonce
        self.hash = _hash

class Proof:
    target_threshold = 5
    def __init__(self):
        self.target_hash = hex(1, 10) >> (256 - target_threshold)

    def get_work(self, block):
        pass

    def run(self):
        for nonce in range(0, sys.maxsize):
            _hash = get_hash(nonce)
            if _hash < self.target_hash:
                return Work(nonce, _hash)

    def get_hash(self, nonce):
        double_hash = hash(hash(block.get_block_header(nonce)))
        return base58encode(double_hash)