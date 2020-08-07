import sys
from utils import double_sha256
class Work:
    def __init__(self, nonce, _hash):
        self.nonce = nonce
        self.hash = _hash

class Proof:
    def __init__(self, block):
        self.quit = False
        self.block = block
        self.target_hash = hex(int("0"*block.bits + "1" + "0"*(255 - block.bits), 2))[2:]
        self.target_hash = (64 - len(self.target_hash))*'0' + self.target_hash

    def run(self, start):
        for nonce in range(start+1, sys.maxsize): # 2^63-1
            if(quit):
                return None 
            _hash = self.get_hash(nonce)
            if _hash < self.target_hash:
                return Work(nonce, _hash)

            if(nonce % 1000 == 0):
                return nonce

    def get_hash(self, nonce):
        # hash function TBI
        double_hash = double_sha256(block.get_serialized_block_header(nonce))
        return double_hash

if __name__ == '__main__':
    p = Proof()
    print(p.target_hash)