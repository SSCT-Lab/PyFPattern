def has_dead_workers(self):
    defunct = False
    for (idx, x) in enumerate(self._workers):
        if hasattr(x[0], 'exitcode'):
            if (x[0].exitcode in [(- 9), (- 15)]):
                defunct = True
    return defunct