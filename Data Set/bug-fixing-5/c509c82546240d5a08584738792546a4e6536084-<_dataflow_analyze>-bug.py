def _dataflow_analyze(self):
    self._build_graph()
    live_in = defaultdict(set)
    live_out = defaultdict(set)
    while True:
        for i in range(self.op_size, 0, (- 1)):
            live_in[i] = set(self._live_in[i])
            live_out[i] = set(self._live_out[i])
            for s in self._successors[i]:
                self._live_out[i] |= self._live_in[s]
            self._live_in[i] = (self._uses[i] | (self._live_out[i] - self._defs[i]))
        if self._reach_fixed_point(live_in, live_out):
            break