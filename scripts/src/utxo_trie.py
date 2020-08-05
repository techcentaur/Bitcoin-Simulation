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

    def insert(self, txn, node=None, index=0):
        if index == 0:
            node = self.root_node

        if index == self.depth:
            node.end_list[txn.txnid] = {'vout': [x for x in range(len(txn.out_txns))],
            'txn': txn}
            return

        if txn.txnid[index] not in node.children:
            node.children[txn.txnid[index]] = UTXOTrieNode()

        self.insert(txn, node.children[txn.txnid[index]], index+1)

    def search(self, txnid, vout, node=None, index=0):
        if index == 0:
            node = self.root_node

        if index == self.depth:
            if txnid in node.end_list:
                if vout in node.end_list[txnid]['vout']:
                    return True
            return False

        if txnid[index] not in node.children:
            return False

        return self.search(txnid, vout, node.children[txnid[index]], index+1)

    def get(self, txnid, node=None, index=0):
        if index == 0:
            node = self.root_node

        if index == self.depth:
            if txnid in node.end_list:
                return node.end_list[txnid]['txn']
            return False

        if txnid[index] not in node.children:
            return False

        return self.get(txnid, node.children[txnid[index]], index+1)

    def remove(self, txnid, vout, node=None, index=0):
        if index == 0:
            node = self.root_node

        if index == self.depth:
            if txnid in node.end_list:
                if vout in node.end_list[txnid]['vout']:
                    node.end_list[txnid]['vout'].remove(vout)
                    if len(node.end_list[txnid]['vout']) == 0:
                        node.end_list[txnid]['txn'] = None
            return

        if txnid[index] not in node.children:
            return

        self.remove(txnid, vout, node.children[txnid[index]], index+1)

    def print(self, node=None, index=0):
        if index == 0:
            node = self.root_node

        if index == self.depth:
            print(node.end_list)
            return

        for key in node.children:
            print(key, end=" -> ")
            self.print(node.children[key], index+1)

class T:
    def __init__(self, txnid, out):
        self.txnid = txnid
        self.out_txns = [1,2,3]

class P:
    def __init__(self, txnid, out):
        self.txnid = txnid
        self.vout = out

if __name__ == '__main__':
    # testing that if the data structure works
    u = UTXOTrie(depth=2)
    u.insert(T("ab2356", 0))
    u.insert(T("ab2356", 1))
    u.insert(T("ab2356", 2))
    u.insert(T("ac2356", 2))
    u.insert(T("ac226D", 0))
    u.insert(T("acx26D", 2))
    u.insert(T("3c2356", 3))
    u.insert(T("5c2356", 2))
    u.insert(T("5a2346", 1))
    
    u.print()

    print(u.search("5a2346", 1))
    print(u.search("acx26D", 2))
    print(u.search("xzx26D", 0))

    u.remove("ac226D", 0)
    u.remove("ab2356", 2)
    u.remove("5c2356", 2)
    (u.remove("xzx26D", 0))

    print(u.get("5a2346"))

    u.print()