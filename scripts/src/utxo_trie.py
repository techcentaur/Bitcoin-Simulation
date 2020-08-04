class UTXOTrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_node = False
        self.end_list = []

    def __repr__(self):
        print(self.children) 
        print(self.end_list) 
        return ""

class UTXOTrie:
    def __init__(self):
        self.depth = 2
        self.root_node = UTXOTrieNode()

    def insert(self, txn):
        self.__insert__(self.root_node, txn, 0)

    def __insert__(self, node, txn, index):
        if index == self.depth:
            node.end_list.append(txn.txnid)
            return

        if txn.txnid[index] not in node.children:
            node.children[txn.txnid[index]] = UTXOTrieNode()

        self.__insert__(node.children[txn.txnid[index]], txn, index+1)
        return

    def search(self, txn):
        return self.__search__(self.root_node, txn, 0)

    def __search__(self, node, txn, index):
        if index == self.depth:
            return True if txn.txnid in node.end_list else False

        if txn.txnid[index] not in node.children:
            return False

        return self.__search__(node.children[txn.txnid[index]], txn, index+1)

    def remove(self, txn):
        self.__remove__(self.root_node, txn, 0)

    def __remove__(self, node, txn, index):
        if index == self.depth:
            if txn.txnid in node.end_list:
                node.end_list.remove(txn.txnid)
            return

        if txn.txnid[index] not in node.children:
            return

        self.__remove__(node.children[txn.txnid[index]], txn, index+1)

    def print(self):
        self.__print__(self.root_node, 0)

    def __print__(self, node, index):
        if index == self.depth:
            print(node.end_list)
            return

        for key in node.children:
            print(key, end=" -> ")
            self.__print__(node.children[key], index+1)

        return

class T:
    def __init__(self, t):
        self.txnid = t 

if __name__ == '__main__':

    u = UTXOTrie()
    u.insert(T("ab2356"))
    u.insert(T("ac2356"))
    u.insert(T("ac226D"))
    u.insert(T("acx26D"))
    u.insert(T("3c2356"))
    u.insert(T("5c2356"))
    u.insert(T("5a2346"))
    u.print()
    print(u.search(T("5a2346")))
    print(u.search(T("acx26D")))
    print(u.search(T("xzx26D")))

    u.remove(T("ac226D"))
    u.remove(T("acx26D"))
    u.remove(T("5c2356"))
    u.remove(T("3c2356"))
    u.remove(T("5a2346"))
    u.print()