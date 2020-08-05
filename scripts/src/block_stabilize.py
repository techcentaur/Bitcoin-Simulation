class Bnode:
    def __init__(self):
        self.children = []
        self.parent = None
        self.height = 0
        self.block = B(None, None)

    def update(self, c, p, h, b):
        self.children = c
        self.parent = p
        self.height = h
        self.block = b

    def __str__(self):
        s = ""
        s += " p: {}".format(None if self.parent is None else self.parent.block.id)
        s += " h: {}".format(self.height)
        s += " id: {}".format(self.block.id)
        s += " child: -> \n{a}[{b}]".format(a="\t"*(self.height+1), b="\n\t".join([x.__str__() for x in self.children]))
        return s

class Stabilize:
    def __init__(self, t):
        self.root = Bnode()
        self.orphan_threshold = t
        self.longest_height = 0
        self.second_longest_head_height = 0
        self.longest_active_head = None

    def print(self, node=None):
        if node is None:
            node = self.root
            print(self.root)
            return

    def add(self, b):
        if b.p == None:
            self.root.block = b
        else:
            self.__add(self.root, b)

    def __add(self, r, b):
        if r.block.id == b.p:
            bnode = Bnode()
            bnode.update([], r, r.height+1, b)
            r.children.append(bnode)

            if r.height+1 > self.longest_height:
                self.longest_height = r.height+1

                if (self.longest_active_head is not None):
                    if self.longest_active_head.block.id != r.block.id:
                        common = self.side_branch_nodes(bnode, self.longest_active_head)
                        p_nodes = self.path_nodes(common, self.longest_active_head)
                        """these p_nodes needed to removed from UTXOs and that thing"""

                        self.second_longest_head_height = self.longest_active_head.height

                self.longest_active_head = bnode
            
            return 1

        for c in r.children:
            ret = self.__add(c, b) 
            if ret == 1:
                return 1
        return 0

    def path_nodes(self, start, end):
        p_nodes = []
        while end.block.id != start.block.id:
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
                        if c.block.id != end.block.id:
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
            if sp.block.id in main_ids:
                return sp
            elif mp.block.id in side_ids:
                return mp
            side_ids.append(sp.block.id)
            main_ids.append(mp.block.id)

            sp = sp.parent
            mp = mp.parent

        if sp.height == 0:
            while mp.height > 0:
                if mp.block.id in side_ids:
                    return mp
                mp = mp.parent

        print("never coming here")
        return self.root
            
class B:
    def __init__(self, i, p):
        self.id = i
        self.p = p


if __name__ == '__main__':
    bstab = Stabilize(t=2)
    bstab.add(B(1, None))
    bstab.add(B(2, 1))
    bstab.add(B(3, 2))
    bstab.add(B("a", 2))    
    bstab.add(B("+", 2))    
    bstab.add(B("b", "a"))    
    bstab.add(B("-", "b"))    
    bstab.add(B("c", "b"))    
    bstab.add(B("d", "c"))    
    bstab.add(B(4, 3))
    bstab.add(B(5, 4))
    bstab.add(B(6, 5))
    bstab.add(B(7, 6))
    bstab.add(B(8, 7))
    bstab.add(B(9, 8))

    # print(bstab.root.children[0].children)
    bstab.print()
    on = bstab.check_for_orphan_nodes(bstab.longest_active_head)
    for o in on:
        print(o)