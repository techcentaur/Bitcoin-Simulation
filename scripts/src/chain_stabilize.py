class Bnode:
    def __init__(self, children=[], parent=None, height=0, block=None):
        self.children = children
        self.parent = parent
        self.height = height
        if block is None:
            self.block = B(None, None)
        else:
            self.block = block

    def __str__(self):
        s = ""
        s += " p: {}".format(None if self.parent is None else self.parent.block.hash)
        s += " h: {}".format(self.height)
        s += " id: {}".format(self.block.hash)
        s += " child: -> \n{a}[{b}]".format(a="\t"*(self.height+1), b="\n\t".join([x.__str__() for x in self.children]))
        return s

class Stabilize:
    def __init__(self, orphan_threshold):
        self.root = Bnode()
        self.orphan_threshold = orphan_threshold

        self.longest_height = 0
        self.second_longest_head_height = 0
        self.longest_active_head = None

    def add(self, b):
        if b.prev_block_hash == None:
            self.root.block = b
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
                            'nodes_to_remove': r_nodes,
                            'nodes_to_add': a_nodes
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

    def check_for_orphan_nodes(self, end_block):
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

        return orphan_chains

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
            
class B:
    def __init__(self, _hash, prev_block_hash):
        self.hash = _hash
        self.prev_block_hash = prev_block_hash

def prrrint(x):
    if x:
        print("REMOVE")
        for i in x['nodes_to_remove']:
            print(i)
        print("ADD")
        x['nodes_to_add'].reverse()
        for i in x['nodes_to_add']:
            print(i)

if __name__ == '__main__':
    bstab = Stabilize(2)
    x = bstab.add(B(1, None))
    prrrint(x)
    x = bstab.add(B(2, 1))
    prrrint(x)
    x = bstab.add(B(3, 2))
    prrrint(x)
    x = bstab.add(B("a", 2))    
    prrrint(x)
    x = bstab.add(B("+", 2))    
    prrrint(x)
    x = bstab.add(B("b", "a"))    
    prrrint(x)
    x = bstab.add(B("-", "b"))    
    prrrint(x)
    x = bstab.add(B("c", "b"))    
    prrrint(x)
    x = bstab.add(B("d", "c"))    
    prrrint(x)
    x = bstab.add(B(4, 3))
    prrrint(x)
    x = bstab.add(B(5, 4))
    prrrint(x)
    x = bstab.add(B(6, 5))
    prrrint(x)
    x = bstab.add(B(7, 6))
    prrrint(x)
    x = bstab.add(B(8, 7))
    prrrint(x)
    x = bstab.add(B(9, 8))
    prrrint(x)

    # print(bstab.root.children[0].children)
    # print(bstab.root)
    print("ORPHAN")
    on = bstab.check_for_orphan_nodes(bstab.longest_active_head)
    for o in on:
        print(o)