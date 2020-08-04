class Blockchain:
    def verify_txn(self, txn):
        pass

    def self_stabilise(self):
        # all 3 cases from
        # https://en.bitcoin.it/wiki/Protocol_rules#.22tx.22_messages
        pass

    @staticmethod
    def is_coinbase(txn):
        return (len(txn.inputs()) == 1) and (int(txn.inputs[0].txnid, 16) == 0)
                and (int(txn.inputs[0].vout, 16) == -1)

    def verify_txn(self, txn):
        if Blockchain.is_coinbase(txn):
            return True
        # verify all inputs and amount
        
    def get_all_UTXOs(self):
        pass

    def find_txn(self, txnid):
        pass
