class Network:
    def __init__(self):
        self.nodes  = [] # star topology

    def create_nodes(self, num_nodes):
        for i in num_nodes:
            self.nodes.append(Node(self))

    def get_blockchain(self):
        pass

    def distribute_txn(self, txn, src_node):
        for node in self.nodes:
            if node != src_node:
                node.send_message(("txn", temp_txn))

    def distribute_block(self, block, src_node):
        for node in self.nodes:
            if node != src_node:
                node.send_message(("block", block))

    def send_txnid_to_node(self, reciever_address, txndata):
        self.address_node_map[reciever_address].coin_recieved_txnid(txndata)

if __name__ == '__main__':
    pass