import hashlib

from script_interpreter import ScriptInterpreter
from chain_stabilize import Stabilize

class Blockchain:
    def __init__(self, UTXOdb, network, node):
        self.UTXOdb = UTXOdb
        self.network = network
        self.node = node

        self.prev_block_hash = None
        self.last_block_pointer = None

        self.stabilize = Stabilize(orphan_threshold=3)

    def add_block(self, block):
        if not self.verify_block(block):
            return False
        self.insert_block_in_chain(block)

    def verify_block(self, block):
        """
        1. hash (block header + nonce) to see if the hash is correct
        - also verify merkel hash
        2. input txns should exist as UTXO 
            2.1 check scripting signatures and pubkeyscript
            2.2 diff of output and input amount == reward in coinbase txn of block
        this means: block is correct.
        """

        serial = block.get_serialized_block_header(block.nonce)
        
        hash_hex = hashlib.new('sha256',
            hashlib.new('sha256', serial.decode('hex')).digest()).digest().encode('hex')

        # verifying hash of block
        if not (hash_hex == block.hash):
            return False

        # TODO: verify merkle hash here
        if not (block.merkle_root_hash == block.get_merkle_root_hash()):
            return False

        # block.txn_pool[0] is coinbase [ASSUMPTION]
        coinbase_future_reward = 0.0
        for txn in block.txn_pool[1:]:
            input_amount = 0.0
            for inp_txn in txn.inp_txns:
                if not self.UTXOdb.search_by_txnid(inp_txn.txnid, inp_txn.vout):
                    return False
        
                output_txn = self.UTXOdb.get_txn_by_txnid(inp_txn.txnid).out_txns[inp_txn.vout]
                if not ScriptInterpreter.verify_pay_to_pubkey_hash(
                    inp_txn.signature_script,
                    output_txn.script_pub_key,
                    message # ? serialized txn
                    ):
                    return False

                input_amount += output_txn.amount 

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


    def insert_block_in_chain(self, block):
        """
        TODO: For each transaction in the block, delete any matching transaction from the transaction pool
        - add block to chain and stabilize if necessary
        """

        if block.prev_block_hash == self.prev_block_hash:
            # new block is in main chain
            self.prev_block_hash = block.hash
            reorg_dict = self.stabilize.add(block)
            if reorg_dict:
                print("[?] Error: Chain can't be reorganized when new block adds in longest chain")
            
            for txn in block.txn_pool[1:]:
                for inp_txn in txn.inp_txns:
                    self.UTXOdb.remove_by_txnid(inp_txn.txnid, inp_txn.vout)
            for txn in block.txn_pool:
                self.UTXOdb.add_by_txn(txn)
        else:
            # new block is in side chain
            reorg_dict = self.stabilize.add(block)
            if reorg_dict:
                # need reorganization
                self.reorganize_blocks(reorg_dict)
            else:
                # just add block (already added) in side chain and don't change UTXOdb
                pass

    def reorganize_blocks(self, reorg_dict):
        # removing blocks in back-track of prev main chain
        for block in reorg_dict['blocks_to_remove']:
            for txn in block.txn_pool:
                self.UTXOdb.remove_by_txn(txn)

            for txn in block.txn_pool[1:]:
                for inp_txn in txn.inp_txns:
                    self.UTXOdb.add_by_txnid(inp_txn.txnid, inp_txn.vout)

        # adding blocks in front-track of new main chain
        for block in reorg_dict['blocks_to_add']:
            for txn in block.txn_pool[1:]:
                for inp_txn in txn.inp_txns:
                    self.UTXOdb.remove_by_txnid(inp_txn.txnid, inp_txn.vout)
            
            for txn in block.txn_pool:
                self.UTXOdb.add_by_txn(txn)

    def orphan_txns_redistribute(self):
        o_blocks = self.stabilize.check_for_orphan_nodes()
        if o_blocks:
            for block in o_blocks:
                for txn in block.txn_pool:
                    for inp_txn in txn.inp_txns:
                        if not self.UTXOdb.search_by_txnid(inp_txn.txnid, inp_txn.vout):
                            break
                    else:
                        # redistribute on network
                        self.network.distribute_txn(txn, self.node)