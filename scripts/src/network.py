import node
import threading

class Network:
    nodes  = [] # star topology
    address_map = {} # pub_key_hash -> index in nodes

    def __init__(self):
        pass

    @staticmethod
    def add_node(n):
        Network.nodes.append(n)

    @staticmethod
    def create_nodes(num_nodes):
        for i in range(num_nodes):
            Network.nodes.append(node.Node())

    @staticmethod
    def get_blockchain():
        pass

    @staticmethod
    def distribute_txn(txn, src_node):
        for n in Network.nodes:
            if n != src_node:
                n.send_message(("txn", temp_txn))

    @staticmethod
    def distribute_block(block, src_node):
        for n in Network.nodes:
            if n != src_node:
                n.send_message(("block", block))

    @staticmethod
    def send_txnid_to_node(reciever_address, txndata):
        pass

if __name__ == '__main__':
    pass