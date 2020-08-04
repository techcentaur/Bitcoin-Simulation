class TXN:
    def __init__(self):
        self.inp_txns = []
        self.out_txns = []

    def create_txid(self):
        data = get_txn_data()
        self.txid = reverse_bytes(hash(hash(data)))

    def get_txn_data(self):
        pass
