import hashlib

import network
from script_interpreter import ScriptInterpreter
from chain_stabilize import Stabilize
from utils import double_sha256
import config

class Blockchain:
    def __init__(self, UTXOdb, node):
        self.UTXOdb = UTXOdb
        self.node = node

        self.prev_block_hash = "0"*64
        self.last_block_pointer = None

        self.stabilize = Stabilize(orphan_threshold=3)

    def __str__(self):
        return self.stabilize.print_it_all(self.stabilize.root)

    def print(self, pad=""):
        print(pad, self.stabilize.print_it_all(self.stabilize.root))

    def add_block(self, block, genesis=False):
        if genesis:
            self.insert_block_in_chain(block)
        else:
            if not self.verify_block(block): 
                return False
            self.insert_block_in_chain(block)
        return True

    def verify_txn(self, txn):
        input_amount = 0
        for inp_txn in txn.inp_txns:
            if not self.UTXOdb.search_by_txnid(inp_txn.txnid, inp_txn.vout):
                return False
    
            output_txn = self.UTXOdb.get_txn_by_txnid(inp_txn.txnid).out_txns[inp_txn.vout]
            if not ScriptInterpreter.verify_pay_to_pubkey_hash(
                inp_txn.signature_script,
                output_txn.script_pub_key,
                txn.get_txn_data()
                ):
                return False

            input_amount += output_txn.amount 

        output_amount = 0.0
        for out_txn in txn.out_txns:
            output_amount += out_txn.amount

        if output_amount > input_amount:
            return False

        return True

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
    
        # verifying hash of block
        hash_hex = double_sha256(serial)
        if not (hash_hex == block.hash and 
            block.merkle_root == block.get_merkle_root_hash()):
            return False

        # block.txns[0] is coinbase [ASSUMPTION]
        coinbase_future_reward = 0.0
        for txn in block.txns[1:]:
            input_amount = 0.0
            for inp_txn in txn.inp_txns:
                if not self.UTXOdb.search_by_txnid(inp_txn.txnid, inp_txn.vout):
                    return False
        
                output_txn = self.UTXOdb.get_txn_by_txnid(inp_txn.txnid).out_txns[inp_txn.vout]
                if not ScriptInterpreter.verify_pay_to_pubkey_hash(
                    inp_txn.signature_script,
                    output_txn.script_pub_key,
                    txn.get_txn_data()
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
        coinbase = block.txns[0]
        if not ((len(coinbase.inp_txns) == 1) and (int(coinbase.inp_txns[0].txnid, 16) == 0)
                        and (int(coinbase.inp_txns[0].vout, 16) == -1)
                        and (len(coinbase.out_txns) == 1)):
            return False
        if coinbase.out_txns[0].amount > coinbase_future_reward + config.reward:
            return False

        return True

    def update_txn_pool(self, txns):
        txn_hashmap = {}
        for txn in txns:
            txn_hashmap[txn.txnid] = True

        remove_pool = []
        for txn in self.node.waiting_txn_pool:
            if txn in txn_hashmap:
                remove_pool.append(txn)

        for txn in remove_pool:
            self.node.waiting_txn_pool.remove(txn)

    def insert_block_in_chain(self, block):
        """
        - For each transaction in the block, delete any matching transaction from the transaction pool
        - add block to chain and stabilize if necessary
        """

        if block.prev_block_hash == self.prev_block_hash:
            # new block is in main chain
            self.prev_block_hash = block.hash
            reorg_dict = self.stabilize.add(block)
            if reorg_dict:
                print("[?] Error: Chain can't be reorganized when new block adds in longest chain")
            
            for txn in block.txns[1:]:
                for inp_txn in txn.inp_txns:
                    self.UTXOdb.remove_by_txnid(inp_txn.txnid, inp_txn.vout)
            for txn in block.txns:
                self.UTXOdb.add_by_txn(txn)

            self.update_txn_pool(block.txns[1:])
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
            for txn in block.txns:
                self.UTXOdb.remove_by_txn(txn)

            for txn in block.txns[1:]:
                for inp_txn in txn.inp_txns:
                    self.UTXOdb.add_by_txnid(inp_txn.txnid, inp_txn.vout)

        # adding blocks in front-track of new main chain
        for block in reorg_dict['blocks_to_add']:
            for txn in block.txns[1:]:
                for inp_txn in txn.inp_txns:
                    self.UTXOdb.remove_by_txnid(inp_txn.txnid, inp_txn.vout)
            
            for txn in block.txns:
                self.UTXOdb.add_by_txn(txn)

    def orphan_txns_redistribute(self):
        o_blocks = self.stabilize.check_for_orphan_nodes()
        if o_blocks:
            for block in o_blocks:
                for txn in block.txns:
                    for inp_txn in txn.inp_txns:
                        if not self.UTXOdb.search_by_txnid(inp_txn.txnid, inp_txn.vout):
                            break
                    else:
                        # redistribute on network
                        self.network.distribute_txn(txn, self.node)

    def get_inputs(self, amount_needed):
        amount_found = 0
        input_txnids = []

        for (txnid, vout) in self.node.recieved_txn_ids:
            if self.UTXOdb.search_by_txnid(txnid, vout):
                if amount_found >= amount_needed:
                    break
                amount_found += self.UTXOdb.get_txn_by_txnid(txnid).out_txns[vout].amount
                input_txnids.append((txnid, vout))

        return input_txnids, amount_found

