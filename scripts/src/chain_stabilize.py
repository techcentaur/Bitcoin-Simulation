from block import Block

class Bnode:
    def __init__(self, children=[], parent=None, height=0, block=None):
        self.children = children
        self.parent = parent
        self.height = height
        if block is None:
            # self.block = B(None, None)
            self.block = Block()
        else:
            self.block = block

    def __str__(self):
        s = ""
        s += " p: {}".format("0"*64 if self.parent is None else self.parent.block.hash)
        s += " h: {}".format(self.height)
        s += " id: {}".format(self.block.hash)
        s += " child: -> \n{a}[{b}]".format(a="\t"*(self.height+1), b="\n\t".join([x.__str__() for x in self.children]))
        return s

class Stabilize:
    def __init__(self, orphan_threshold):
        self.root = None
        self.orphan_threshold = orphan_threshold

        self.longest_height = 0
        self.second_longest_head_height = 0
        self.longest_active_head = None

    def add(self, b):
        if b.prev_block_hash == "0"*64:
            self.root = Bnode([], None, 0, b)
        else:
            return self.__add(self.root, b)
        return []

    def __add(self, r, b):
        p_nodes = []
        if r.block.hash == b.prev_block_hash:
            bnode = Bnode([], r, r.height+1, b)
            r.children.append(bnode)

            if r.height+1 > self.longest_height:
                self.longest_height = r.height+1

                if (self.longest_active_head is not None):
                    if self.longest_active_head.block.hash != r.block.hash:
                        common = self.side_branch_nodes(bnode, self.longest_active_head)
                        r_nodes = self.path_nodes(common, self.longest_active_head)
                        a_nodes = self.path_nodes(common, bnode)
                        p_nodes = {
                            'blocks_to_remove': r_nodes,
                            'blocks_to_add': a_nodes
                        }
                        """these p_nodes needed to removed from UTXOs and that thing"""
                        print("REORGANIZE")
                        self.second_longest_head_height = self.longest_active_head.height

                self.longest_active_head = bnode
            
            return p_nodes

        for c in r.children:
            ret = self.__add(c, b) 
            if len(ret) != 0:
                return ret
        return p_nodes

    def path_nodes(self, start, end):
        p_nodes = []
        while end.block.hash != start.block.hash:
            p_nodes.append(end)
            end = end.parent
        return p_nodes

    def check_for_orphan_nodes(self):
        end_block = self.longest_active_head
        
        orphan_chains = []
        if (self.longest_height - self.second_longest_head_height) > self.orphan_threshold:
            end = end_block
            while end.height > 0:
                if len(end.parent.children) > 1:
                    for c in end.parent.children:
                        if c.block.hash != end.block.hash:
                            orphan_chains.append(c)
                    end.parent.children = [end_block]
                end = end.parent

        return self.chains_to_blocks(orphan_chains)

    def chains_to_blocks(self, chains):
        nodes = []
        for chain in chains:
            nodes.extend(self.__chains_to_nodes__(chain))
        return [n.block for n in nodes]

    def __chains_to_nodes__(self, start):
        l = []
        l.append(start)
        for c in start.children:
            l.extend(self.__chains_to_nodes__(c))
        return l

    def side_branch_nodes(self, main_branch, side_branch):
        side_ids = []
        main_ids = []

        sp = side_branch
        mp = main_branch
        
        while sp.height > 0:
            if sp.block.hash in main_ids:
                return sp
            elif mp.block.hash in side_ids:
                return mp
            side_ids.append(sp.block.hash)
            main_ids.append(mp.block.hash)

            sp = sp.parent
            mp = mp.parent

        if sp.height == 0:
            while mp.height > 0:
                if mp.block.hash in side_ids:
                    return mp
                mp = mp.parent

        print("[?] pointers can't go beyond the root")
        return self.root

    def print_main_branch(self):
        last = self.longest_active_head
        
        if not last:
            return ""
            
        while last.height > -1:
            print("[*] Block: ", last.block.hash)
            for txn in last.block.txn_pool:
                print("\t[.] txn: ", txn.txnid)
                for i in txn.inp_txns:
                    print("[txnid: {}. vout: {}. subsig: {}]".format(i.txnid, i.vout, i.signature_script))
                for o in txn.out_txns:
                    print("[amount: {}]".format(i.txnid, i.vout))
            last = last.parent

    def print_it_all(self, start):
        print(start)
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        return ""

class B:
    def __init__(self, _hash, prev_block_hash):
        self.hash = _hash
        self.prev_block_hash = prev_block_hash

def prrrint(x):
    if x:
        print("REMOVE")
        for i in x['blocks_to_remove']:
            print(i)
        print("ADD")
        x['blocks_to_add'].reverse()
        for i in x['blocks_to_add']:
            print(i)

if __name__ == '__main__':
    # bstab = Stabilize(2)
    # x = bstab.add(B(1, None))
    # x = bstab.add(B(2, 1))
    # x = bstab.add(B(3, 2))
    # x = bstab.add(B("a", 2))    
    # x = bstab.add(B("+", 2))    
    # x = bstab.add(B("b", "a"))    
    # x = bstab.add(B("-", "b"))    
    # x = bstab.add(B("c", "b"))    
    # x = bstab.add(B("d", "c"))    
    # x = bstab.add(B(4, 3))
    # x = bstab.add(B(5, 4))
    # x = bstab.add(B(6, 5))
    # x = bstab.add(B(7, 6))
    # x = bstab.add(B(8, 7))
    # x = bstab.add(B(9, 8))
    # bstab.print_it_all(bstab.root)

    # # print(bstab.root.children[0].children)
    # # print(bstab.root)
    # print("ORPHAN")
    # on = bstab.check_for_orphan_nodes()
    # print(on)
    pass