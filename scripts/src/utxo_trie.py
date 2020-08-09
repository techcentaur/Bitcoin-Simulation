class UTXOTrieNode:
    def __init__(self):
        self.children = {}
        self.end_list = {}

    def __repr__(self):
        s = ""
        s += str(self.children) 
        s += str(self.end_list) 
        return s

class UTXOTrie:
    def __init__(self, depth=2):
        self.depth = depth
        self.root_node = UTXOTrieNode()

    def add_by_txn(self, txn, node=None, index=0):
        if index == 0:
            node = self.root_node

        if index == self.depth:
            node.end_list[txn.txnid] = {'vout': [x for x in range(len(txn.out_txns))],
            'txn': txn}
            return

        if txn.txnid[index] not in node.children:
            node.children[txn.txnid[index]] = UTXOTrieNode()

        self.add_by_txn(txn, node.children[txn.txnid[index]], index+1)

    def add_by_txnid(self, txnid, vout, node=None, index=0):
        if index == 0:
            node = self.root_node

        if index == self.depth:
            if txnid in node.end_list:
                node.end_list[txnid]['vout'].append(vout)
            return

        if txnid[index] not in node.children:
            node.children[txnid[index]] = UTXOTrieNode()

        self.add_by_txnid(txnid, vout, node.children[txnid[index]], index+1)

    def search_by_txnid(self, txnid, vout, node=None, index=0):
        if index == 0:
            node = self.root_node

        if index == self.depth:
            if txnid in node.end_list:
                if vout in node.end_list[txnid]['vout']:
                    return True
            return False

        if txnid[index] not in node.children:
            return False

        return self.search_by_txnid(txnid, vout, node.children[txnid[index]], index+1)

    def get_txn_by_txnid(self, txnid, node=None, index=0):
        if index == 0:
            node = self.root_node

        if index == self.depth:
            if txnid in node.end_list:
                return node.end_list[txnid]['txn']
            return False

        if txnid[index] not in node.children:
            return False

        return self.get_txn_by_txnid(txnid, node.children[txnid[index]], index+1)

    def remove_by_txnid(self, txnid, vout, node=None, index=0):
        if index == 0:
            node = self.root_node

        if index == self.depth:
            if txnid in node.end_list:
                if vout in node.end_list[txnid]['vout']:
                    node.end_list[txnid]['vout'].remove(vout)
            return

        if txnid[index] not in node.children:
            return

        self.remove_by_txnid(txnid, vout, node.children[txnid[index]], index+1)

    def remove_by_txn(self, txn, node=None, index=0):
        if index == 0:
            node = self.root_node
        if index == self.depth:
            if txn.txnid in node.end_list:
                node.end_list.pop(txn.txnid, None)
            return
        if txn.txnid[index] not in node.children:
            return

        self.remove_by_txn(txn, node.children[txn.txnid[index]], index+1)

    def print(self, node=None, index=0):
        if index == 0:
            node = self.root_node

        if index == self.depth:
            print(node.end_list)
            return

        for key in node.children:
            print(key, end=" -> ")
            self.print(node.children[key], index+1)

class In:
    def __init__(self, t, o):
        self.txnid = t
        self.vout = o

class Out:
    def __init__(self):
        pass

class Txn:
    def __init__(self, i, o, h):
        self.inp_txns = i
        self.out_txns = o
        self.txnid = h

if __name__ == '__main__':
    # testing
    pass
    # u = UTXOTrie(depth=2)
    # txn = (Txn([In("12acf9", 1), In("12abb9", 2)],
    #     [Out(), Out(), Out()],
    #     "14fa21"))
    # u.add_by_txn(txn)

    # txn = (Txn([In("937acf", 1), In("124b7b", 0)],
    #     [Out(), Out(), Out()],
    #     "1212aa"))
    # u.add_by_txn(txn)

    # txn = (Txn([In("4212aa", 1), In("4212aa", 0)],
    #     [Out(), Out(), Out()],
    #     "233c42"))
    # u.add_by_txn(txn)

    # u.add_by_txnid("233c42", 3)
    # u.remove_by_txnid("233c42", 2)
    # u.print()   

    # u.remove_by_txn(txn)

    # for i in txn.inp_txns: