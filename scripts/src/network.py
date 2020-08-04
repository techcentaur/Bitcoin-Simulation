class Network:
    def __init__(self):
        self.nodes  = []

    def create_nodes(self, num_nodes):
        for i in num_nodes:
            self.nodes.append(Node())

if __name__ == '__main__':
    net = Network()
    net.create_nodes(2)