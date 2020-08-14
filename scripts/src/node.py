from collections import deque
from threading import Lock, current_thread
import utils
import block 
import transaction
import output_txn
import input_txn
import network
from utxo_trie import UTXOTrie 
from blockchain import Blockchain 
from proof import Proof
import time

class Node:
    def __init__(self):
        self.keys = utils.generate_ec_key_pairs()
        self.pub_key_hash = utils.hash160(self.keys['public'])
        # self.address = utils.Base58.base58encode(hash160)
        
        self.waiting_txn_pool = []
        self.lock = Lock()
        self.messages = deque()
        
        self.database_UTXO = UTXOTrie()
        self.blockchain = Blockchain(self.database_UTXO, self)

        self.recieved_txn_ids = []
        self.proof = None
        self.run_now = True

    def __str__(self):
        return self.blockchain.__str__()

    def print(self, pad=""):
        print(pad, "##########---------- Node ----------##########")
        print(pad, "[@] Private Key : {}".format(self.keys['private']))
        print(pad, "[@] Public Key : {}".format(self.keys['public']))
        print(pad, "[@] Pub Key Hash : {}".format(self.pub_key_hash))

        print(pad, "[@] Blockchain")
        self.blockchain.print(pad + "    ")

    def start_mining(self):
        while self.run_now:
            if not self.waiting_txn_pool:
                # print("T: {} [slept]".format(current_thread().name))
                time.sleep(5)
                # print("T: {} [woke]".format(current_thread().name))
                self.check_messages()
                continue

            new_txn_pool = self.waiting_txn_pool.copy()
            self.waiting_txn_pool = []

            coinbase_txn = transaction.TXN.create_coinbase_txn(self.keys)
            self.current_block = block.Block([coinbase_txn] + [txn for txn in new_txn_pool], self.blockchain.prev_block_hash)
            self.calculate_proof()

    def coin_recieved_txnid(self, txndata):
        self.recieved_txn_ids.append(txndata)

    def create_txn(self, reciever_address, amount):
        out_txns = []
        out_txns.append(output_txn.OutputTXN(amount, reciever_address))
        
        inp_txnids, total_amount = self.blockchain.get_inputs(amount)
        if (not inp_txnids) or (total_amount < amount):
            # not enough coin
            return False
        
        is_last_vout_self = False
        if total_amount > amount:
            is_last_vout_self = True
            out_txns.append(output_txn.OutputTXN(total_amount - amount, self.pub_key_hash))

        inp_txns = []
        for i in inp_txnids:
            script_sig = utils.create_script_sig(self.keys, i[0])
            inp_txns.append(input_txn.InputTXN(i[0], i[1], script_sig))

        new_txn = transaction.TXN(inp_txns, out_txns)
        
        with self.lock:
            self.messages.append(("txn", new_txn))

        if is_last_vout_self:
            self.recieved_txn_ids.append((new_txn.txnid, len(new_txn.out_txns)-1))

        with self.lock:
            network.Network.nodes[network.Network.address_map[reciever_address]].coin_recieved_txnid((new_txn.txnid, 0))

        with self.lock:
            for n in network.Network.nodes:
                if n != self:
                    n.messages.append(("txn", new_txn))
        return True

    @staticmethod
    def create_genesis_block(keys):
        coinbase_txn = transaction.TXN.create_coinbase_txn(keys)
        genesis_block = block.Block.create_genesis_block(coinbase_txn)

        genesis_block.prev_block_hash = "0"*64
        genesis_block.hash = "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"

        return genesis_block

    def save_genesis_block(self, genesis_block):
        # we will always get it once at the start
        return self.blockchain.add_block(genesis_block, genesis=True)

    def send_txn_over_network(self, txn):
        network.distribute_txn(txn, self)

    def receive_txn(self, txn):
        ret = self.blockchain.verify_txn(txn)
        if not ret:
            print("T: {} TXN false".format(current_thread().name))
        self.waiting_txn_pool.append(txn)

    def calculate_proof(self):
        self.proof = Proof(self.current_block)
        work = 0
        while True:
            work = self.proof.run(work)
            if type(work) == int:
                self.check_messages()
            else:
                break

        if(work == None):
            return

        self.current_block.nonce = work.nonce
        self.current_block.hash = work.hash
        self.current_block.print()
        print("T: ", current_thread().name, "[MINED] [BLOCK]")
        self.blockchain.add_block(self.current_block)
        network.Network.distribute_block(self.current_block, self)

    def check_messages(self):
        while len(self.messages):
            with self.lock:
                msg_type, msg = self.messages.popleft()
            
            if msg_type == "txn":
                print("T: ", current_thread().name, "[RECEIVED] [TXN]")
                _txn = msg.create_copy()
                self.receive_txn(_txn)
            elif msg_type == "block":
                print("T: ", current_thread().name, "[RECEIVED] [BLOCK]")
                block = msg.create_copy()
                self.recieve_block(block)
            elif msg_type == "new_txn":
                print("T: ", current_thread().name, "[CREATED] [TXN]")
                reciever_address, amount = msg[0], msg[1]
                ret = self.create_txn(reciever_address, amount)

    def send_message(self, message):
        with self.lock:
            self.messages.append(message)

    def recieve_block(self, block):
        """
        1. block <- verify all txns / proof of work check
        check coinbase all props
        2. current_block <- txns in block, next current block mem pool
        3. start proof of works
        """
        # block.print()
        output = self.blockchain.add_block(block)
        if not output:
            print("[?] Block not added")
        else:
            if self.proof != None:
                self.proof.quit = True