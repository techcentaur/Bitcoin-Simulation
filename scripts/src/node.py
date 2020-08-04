import utils

class Node:
    def __init__(self):
        self.keys = utils.generate_ec_key_pairs()
        self.address = base58encode(self.keys['public'])


    def get_blockchain(self):
        self.blockchain = network.get_blockchain()

    def get_UTXO_array(self):
        # use self.blockchain
        # TRIE DS
        pass

    def send_txn_over_network(self, txn):
        network.distribute_txn(txn)

    def receive_txn(txn):
        self.blockchain.verify_txn(txn)

        self.current_block.add_txn(txn)

    def calculate_proof(self):
        self.current_block = Block()

        work = Proof(self.current_block)
        network.send_block(self.current_block)

    def recieve_block(self, block):
        """
        1. block <- verify all txns / proof of work check
        check coinbase all props
        2. current_block <- txns in block, next current block mem pool
        3. start proof of works
        """
        self.blockchain.add_block(block)
