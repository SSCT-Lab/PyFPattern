def _find_avg_pooling_ids(self, graph):
    ids = []
    for op in graph.all_op_nodes():
        if (op.name() in self._pool_ops):
            if (op.op().attr('pooling_type') == 'avg'):
                ids.append(op.id())
    return (set(ids) if len(ids) else set([(- 1)]))