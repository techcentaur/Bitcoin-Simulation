class Network:
    def __init__(self):
        self.nodes  = [] # star topology

    def create_nodes(self, num_nodes):
        for i in num_nodes:
            self.nodes.append(Node())

    def get_blockchain(self):
        pass

    def distribute_txn(self, txn, src_node):
        for node in self.nodes:
            if node != src_node:
                node.receive_txn(txn)

if __name__ == '__main__':
    net = Network()
    net.create_nodes(2)