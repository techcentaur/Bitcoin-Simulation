class UTXOTrieNode:
    def __init__(self):
        self.children = {}
        self.end_list = []

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
            node.end_list.append((txn.txnid, txn.vout))
            return

        if txn.txnid[index] not in node.children:
            node.children[txn.txnid[index]] = UTXOTrieNode()

        self.insert(txn, node.children[txn.txnid[index]], index+1)

    def search(self, txn, node=None, index=0):
        if index == 0:
            node = self.root_node

        if index == self.depth:
            return True if (txn.txnid, txn.vout) in node.end_list else False

        if txn.txnid[index] not in node.children:
            return False

        return self.search(txn, node.children[txn.txnid[index]], index+1)

    def remove(self, txn, node=None, index=0):
        if index == 0:
            node = self.root_node

        if index == self.depth:
            if (txn.txnid, txn.vout) in node.end_list:
                node.end_list.remove((txn.txnid, txn.vout))
            return

        if txn.txnid[index] not in node.children:
            return

        self.remove(txn, node.children[txn.txnid[index]], index+1)

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
    def __init__(self, txnid, vout):
        self.txnid = txnid
        self.vout = vout 

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

    print(u.search(T("5a2346", 1)))
    print(u.search(T("acx26D", 2)))
    print(u.search(T("xzx26D", 0)))

    u.remove(T("ac226D", 0))
    u.remove(T("ab2356", 2))
    u.remove(T("5c2356", 2))
    (u.remove(T("xzx26D", 0)))

    u.print()