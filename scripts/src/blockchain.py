import hashlib

from script_interpreter import ScriptInterpreter

class Blockchain:
    def __init__(self, UTXOdb):
        self.UTXOdb = UTXOdb
        self.prev_block_hash = None
        self.last_block_pointer = None

    def verify_block(self, block):
        """
        1. hash (block header + nonce) to see if the hash is correct
        2. input txns exist as UTXO 
            2.1 check scripting signatures and pubkeyscript
            2.2 diff of output and input amount == reward in coinbase txn of block
        this means: block is correct.
        """

        serial = block.get_serialized_block_header(block.nonce)
        serial_hex = serial.decode('hex')
        
        hash_str = hashlib.new('sha256', hashlib.new('sha256', serial_hex).digest()).digest()
        hash_hex = hash_str.encode('hex')

        # verifying hash of block
        if not (hash_hex == block.hash):
            return False

        # block.txn_pool[0] is coinbase [ASSUMPTION]
        coinbase_future_reward = 0.0
        for txn in block.txn_pool[1:]:
            input_amount = 0.0
            for inp_txn in txn.inp_txns:
                if not self.UTXOdb.search(inp_txn.txnid, inp_txn.vout):
                    return False
        
                output_txn = self.UTXOdb.get(inp_txn.txnid).out_txns[inp_txn.vout]
                if not ScriptInterpreter.verify_pay_to_pubkey_hash(
                    inp_txn.signature_script,
                    output_txn.script_pub_key,
                    message
                    ):
                    return False

                input_amount += output_txn.amount 
                self.UTXOdb.remove(inp_txn.txnid, inp_txn.vout)

            output_amount = 0.0
            for out_txn in txn.out_txns:
                output_amount += out_txn.amount

            if output_amount > input_amount:
                return False
            coinbase_future_reward += (input_amount - output_amount)

        # verify coinbase
        coinbase = block.txn_pool[0]
        if not ((len(coinbase.inputs()) == 1) and (int(coinbase.inputs[0].txnid, 16) == 0)
                        and (int(coinbase.inputs[0].vout, 16) == -1)
                        and (len(coinbase.out_txns) == 1)):
            return False
        if coinbase.out_txns[0].amount > coinbase_future_reward:
            return False
        return True

    def add_block(self, block):
        """add block to chain and add outputs to UTXOs
        """

        # set (blockchain) prev block hash and (block) prev pointer
        self.prev_block_hash = block.hash
        block.prev_block = self.last_block_pointer
        self.last_block_pointer = block

        # add outputs to UTXOdb
        for txn in block.txn_pool:
            self.UTXOdb.insert(out_txn)


    def self_stabilise(self):
        # all 3 cases from
        # https://en.bitcoin.it/wiki/Protocol_rules#.22tx.22_messages
        pass

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



