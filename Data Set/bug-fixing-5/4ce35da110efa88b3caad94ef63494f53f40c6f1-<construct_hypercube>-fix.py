def construct_hypercube(self, origin, supremum, gen, hgr, printout=False):
    '\n        Build a hypercube with triangulations symmetric to C0.\n\n        Parameters\n        ----------\n        origin : vec\n        supremum : vec (tuple)\n        gen : generation\n        hgr : parent homology group rank\n        '
    v_o = np.array(origin)
    v_s = np.array(supremum)
    C_new = Cell(gen, hgr, origin, supremum)
    C_new.centroid = tuple(((v_o + v_s) * 0.5))
    V_new = []
    for (i, v) in enumerate(self.C0()[:(- 1)]):
        v_x = np.array(v.x)
        sub_cell_t1 = (v_o - (v_o * v_x))
        sub_cell_t2 = (v_s * v_x)
        vec = (sub_cell_t1 + sub_cell_t2)
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