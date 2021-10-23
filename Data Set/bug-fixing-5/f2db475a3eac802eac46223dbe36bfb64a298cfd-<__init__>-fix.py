def __init__(self, use_cuda, loss_name=None, main_program=None, share_vars_from=None, exec_strategy=None, build_strategy=None, num_trainers=1, trainer_id=0, scope=None):
    sys.stderr.write('ParallelExecutor is deprecated. Please use CompiledProgram and Executor. CompiledProgram is a central place for optimization and Executor is the unified executor. Example can be found in compiler.py.\n')
    if (build_strategy is None):
        build_strategy = BuildStrategy()
    if ((num_trainers != 1) and (build_strategy.num_trainers != num_trainers)):
        sys.stderr.write(('The value of build_strategy.num_trainers[%d] is overwritten by the passed num_trainers[%d].\n' % (build_strategy.num_trainers, num_trainers)))
        build_strategy.num_trainers = num_trainers
    if ((trainer_id != 0) and (build_strategy.trainer_id != trainer_id)):
        sys.stderr.write(('The value of build_strategy.trainer_id[%d] is overwritten by the passed trainer_id[%d].\n' % (build_strategy.trainer_id, trainer_id)))
        build_strategy.trainer_id = trainer_id
    self._places = (framework.cuda_places() if use_cuda else framework.cpu_places())
    self._scope = (scope if (scope is not None) else executor.global_scope())
    if ((main_program is not None) and main_program._enable_dgc):
        assert (build_strategy.num_trainers > 1), 'dgc is not useful when num_trainers <= 1'
        assert (build_strategy.reduce_strategy == BuildStrategy.ReduceStrategy.AllReduce), 'dgc                 only used for allreduce'
        assert ((build_strategy.num_trainers * len(self._places)) > 1), 'dgc is not useful for single card training'
        assert use_cuda, 'dgc only used under cuda'
    main_program = (main_program if (main_program is not None) else framework.default_main_program())
    self._compiled_program = compiler.CompiledProgram(main_program)
    if share_vars_from:
        assert isinstance(share_vars_from, ParallelExecutor), 'The share_vars_from should be ParallelExecutor.'
    self._compiled_program.with_data_parallel(loss_name=loss_name, build_strategy=build_strategy, exec_strategy=exec_strategy, share_vars_from=(share_vars_from._compiled_program if share_vars_from else None))
    self._place = (core.CUDAPlace(0) if use_cuda else core.CPUPlace())
    self._exe = executor.Executor(self._place)
    self._compiled_program._compile(place=self._place, scope=self._scope)