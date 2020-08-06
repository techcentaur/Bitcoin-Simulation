import utils
from blockchain import Blockchain 

class Node:
    def __init__(self, network, blockchain=None):
        self.keys = utils.generate_ec_key_pairs()
        hash160 = utils.hash160(self.keys['public'])
        self.address = utils.Base58.base58encode(hash160)
        self.txn_pool = []
        self.get_blockchain()
        while True:
            self.calculate_proof()

    def get_blockchain(self):
        self.blockchain = network.get_blockchain()
        self.database_UTXO = self.create_database_UTXO()
        self.blockchain.node = self
        self.blockchain.UTXOdb = self.database_UTXO

    def create_database_UTXO(self):
        """ # database is of type TRIE DS
            - one time scanning of blockchain:
            to find all unspent txns.
        """

    def add_block_txns_to_UTXOdb(self, block):
        # assuming block has been verified
        for txn in block.txns:
            for inptxn in txn.inp_txns:
                if database_UTXO.remove(inptxn):
        for txn in block.txns:
            for vout, outtxn in enumerate(txn.out_txns):
                outtxn.vout = vout
                database_UTXO.insert(outtxn)

    def send_txn_over_network(self, txn):
        network.distribute_txn(txn)

    def receive_txn(txn):
        self.blockchain.verify_txn(txn)
        self.txn_pool.append(txn)

    def calculate_proof(self):
        self.current_block = Block([txn for txn in self.txn_pool], self.blockchain.prev_block_hash)
        self.proof = Proof(self.current_block)
        proof.run()
        self.current_block.nonce = work.nonce
        self.current_block.hash = work.hash
        network.send_block(self.current_block)


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


