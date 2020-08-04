class Block:
    def __init__(self):
        self.block_header = Blockheader()
        self.txn_pool = []

    def add_txn(self, txn):
        self.txn_pool.append(txn)

    def get_block_data(self, nonce):
        # use merkle tree to get hash
        pass