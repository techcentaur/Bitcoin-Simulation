import hashlib

class Blockchain:
    def verify_incoming_block(self, block):
        """
        1. hash (block header + nonce) to see if the hash is correct
        2. input txns exist as UTXO 
            2.1 check scripting signatures and pubkeyscript
            2.2 diff of output and input amount == reward in coinbase txn of block
        this means: block is correct.
        3. add block to chain and add outputs to UTXOs
        4. do chain stabilization if necessary
        """
        serial = block.get_serialized_block_header(block.nonce)
        serial_hex = serial.decode('hex')
        
        hash_str = hashlib.new('sha256', hashlib.new('sha256', serial_hex).digest()).digest()
        hash_hex = hash_str.encode('hex')

        # verifying hash of block
        if not (hash_hex == block.hash):
            return False

        # block.txn_pool[0] is coinbase
        for txn in block.txn_pool[1:]:
            for input_txn in txn.inp_txns:




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

    def verify_txns_in_block(self, block):
        for txn in block.txn_pool:
            for inptxn in txn.inp_txns:
                if not database_UTXO.search(inptxn):
                    return False



