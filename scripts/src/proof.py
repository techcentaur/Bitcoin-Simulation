import sys

class Work:
    def __init__(self, nonce, _hash):
        self.nonce = nonce
        self.hash = _hash

class Proof:
    target_threshold = 5
    def __init__(self):
        self.target_hash = "0000001000000000000000000000000000" <- hex string

    def get_work(self, block):
        pass

    def run(self):
        for nonce in range(0, sys.maxsize): # 2^63-1
            _hash = self.get_hash(nonce)
            if _hash < self.target_hash:
                return Work(nonce, _hash)

    def get_hash(self, nonce):
        # hash function TBI
        double_hash = hash(hash(block.get_serialized_block_header(nonce)))
        return double_hash

if __name__ == '__main__':
    p = Proof()
    print(p.target_hash)