

def _dataflow_analyze(self):
    self._build_graph()
    live_in = defaultdict(set)
    worklist = list(range((len(self._ops) - 1), (- 1), (- 1)))
    while worklist:
        i = worklist.pop(0)
        live_in[i] = set(self._live_in[i])
        for s in self._successors[i]:
            self._live_out[i] |= self._live_in[s]
        self._live_in[i] = (self._uses[i] | (self._live_out[i] - self._defs[i]))
        if (live_in[i] != set(self._live_in[i])):
            for d in self._presuccessors[i]:
                worklist.append(d)
