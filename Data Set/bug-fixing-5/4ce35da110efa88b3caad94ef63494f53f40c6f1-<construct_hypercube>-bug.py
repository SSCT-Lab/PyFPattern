def construct_hypercube(self, origin, supremum, gen, hgr, printout=False):
    '\n        Build a hypercube with triangulations symmetric to C0.\n\n        Parameters\n        ----------\n        origin : vec\n        supremum : vec (tuple)\n        gen : generation\n        hgr : parent homology group rank\n        '
    C_new = Cell(gen, hgr, origin, supremum)
    C_new.centroid = tuple(((np.array(origin) + np.array(supremum)) / 2.0))
    V_new = []
    for (i, v) in enumerate(self.C0()[:(- 1)]):
        t1 = self.generate_sub_cell_t1(origin, v.x)
        t2 = self.generate_sub_cell_t2(supremum, v.x)
        vec = (t1 + t2)
        vec = tuple(vec)
        C_new.add_vertex(self.V[vec])
        V_new.append(vec)
    C_new.add_vertex(self.V[C_new.centroid])
    V_new.append(C_new.centroid)
    for (i, connections) in enumerate(self.graph):
        for j in connections:
            self.V[V_new[i]].connect(self.V[V_new[j]])
    if printout:
        print('A sub hyper cube with:')
        print('origin: {}'.format(origin))
        print('supremum: {}'.format(supremum))
        for v in C_new():
            v.print_out()
    self.H[gen].append(C_new)
    return C_new