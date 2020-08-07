import utils
from blockchain import Blockchain 
from colletion import deque
import output_txn
import txn

class Node:
    def __init__(self, network, blockchain=None):
        self.keys = utils.generate_ec_key_pairs()
        self.pub_key_hash = utils.hash160(self.keys['public'])
        # self.address = utils.Base58.base58encode(hash160)
        self.txn_pool = []
        self.messages = deque()
        self.get_blockchain()
        while True:
            self.calculate_proof()

    def start_process(self, lock):
        self.lock = lock

    def create_txn(self, reciever_address, amount):
        out_txns = []
        out_txns.append(output_txn.OutputTXN(amount, reciever_address))
        
        inp_txns, total_amount = self.blockchain.get_inputs(amount)
        if (not inp_txns) or (total_amount < amount):
            # not enough coin
            return False
        
        if not (total_amount == amount):
            out_txns.append(output_txn.OutputTXN(total_amount - amount, self.pub_key_hash))

        new_txn = txn.TXN(inp_txns, out_txn1)
        with self.lock:
            self.messages.append(("txn", new_txn))
        self.network.distribute_txn(txn, self.node)

        return True

    def get_blockchain(self):
        self.blockchain = network.get_blockchain()
        self.database_UTXO = self.create_database_UTXO()
        self.blockchain.node = self
        self.blockchain.UTXOdb = self.database_UTXO

    def send_txn_over_network(self, txn):
        network.distribute_txn(txn, self)

    def receive_txn(txn):
        self.blockchain.verify_txn(txn)
        self.txn_pool.append(txn)

    def calculate_proof(self):
        self.current_block = Block([txn for txn in self.txn_pool], self.blockchain.prev_block_hash)
        self.proof = Proof(self.current_block)
        work = 0
        while True:
            work = proof.run(work)
            if type(work) == int:
                check_messages()
            else:
                break

        if(work == None):
            return
        self.current_block.nonce = work.nonce
        self.current_block.hash = work.hash
        network.distribute_block(self.current_block, self)

    def check_messages(self):
        while len(self.messages):
            msg_type, msg = self.messages.popleft()
            if msg_type == "txn":
                _txn = msg.create_copy()
                self.receive_txn(_txn)
            elif msg_type == "block":
                block = msg.create_copy()
                self.recieve_block(block)
            elif msg_type == "new_txn":
                reciever_address, amount = msg[0], msg[1]
                self.create_txn(reciever_address, amount)

    def send_message(self, message):
        self.messages.append(message)

    def recieve_block(self, block):
        """
        1. block <- verify all txns / proof of work check
        check coinbase all props
        2. current_block <- txns in block, next current block mem pool
        3. start proof of works
        """
        output = self.blockchain.add_block(block)
        if(output):
            self.proof.quit = True


