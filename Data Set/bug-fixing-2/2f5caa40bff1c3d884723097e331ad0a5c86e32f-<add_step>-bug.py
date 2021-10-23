

def add_step(self, step, run_meta):
    'Add statistics of a step.\n\n    Args:\n      step: A step uint64 used to identify the RunMetadata. Must be different\n         across different AddStep() calls.\n      run_meta: RunMetadata proto that contains statistics of a session run.\n    '
    op_log = tfprof_logger._merge_default_with_oplog(self._graph, run_meta=run_meta, add_trace=False, add_trainable_var=False)
    print_mdl.AddStep(step, run_meta.SerializeToString(), op_log.SerializeToString())
