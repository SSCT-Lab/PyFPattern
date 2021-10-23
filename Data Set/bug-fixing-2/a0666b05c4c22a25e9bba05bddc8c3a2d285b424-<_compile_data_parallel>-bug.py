

def _compile_data_parallel(self):
    if self._share_vars_from:
        if self._scope:
            sys.stderr.write('share_vars_from is set, scope is ignored.\n')
        if (not self._share_vars_from._is_data_parallel):
            raise ValueError('share_vars_from is not data parallel. Cannot share vars from it.')
        if (self._share_vars_from._executor is None):
            raise ValueError('share_vars_from is not compiled and run, so there is no var to share.')
        self._local_scopes = self._share_vars_from._executor.local_scopes()
    else:
        self._local_scopes = []
    self._exec_strategy.use_cuda = isinstance(self._place, core.CUDAPlace)
    if self._exec_strategy.use_cuda:
        gpus_env = os.getenv('FLAGS_selected_gpus')
        if gpus_env:
            gpus = [int(s) for s in gpus_env.split(',')]
        else:
            gpus = [i for i in six.moves.range(core.get_cuda_device_count())]
        self._places = [core.CUDAPlace(i) for i in gpus]
    else:
        cpu_num = int(os.environ.get('CPU_NUM', multiprocessing.cpu_count()))
        self._places = [core.CPUPlace() for _ in six.moves.range(cpu_num)]
    assert self._places, 'no place for execution'
    if (self._exec_strategy.num_threads == 0):
        if self._exec_strategy.use_cuda:
            self._exec_strategy.num_threads = (len(self._places) * 4)
        else:
            cpu_num = int(os.environ.get('CPU_NUM', multiprocessing.cpu_count()))
            self._exec_strategy.num_threads = (cpu_num * 2)
    trainers_endpoints = self._program._trainers_endpoints
    if (self._build_strategy.memory_optimize is None):
        self._build_strategy.memory_optimize = (False if main._is_mem_optimized else True)
    if (self._build_strategy.enable_inplace is None):
        self._build_strategy.enable_inplace = (False if main._is_mem_optimized else True)
    if ((self._build_strategy.num_trainers > 1) and trainers_endpoints):
        assert (self._build_strategy.num_trainers == len(trainers_endpoints)), 'num_trainers == len(end_points)'
        self._build_strategy.trainers_endpoints = trainers_endpoints
    self._persistable_vars = set([cpt.to_text(v.name) for v in [var for var in self._program.list_vars() if (var.persistable and (var.type != core.VarDesc.VarType.RAW))]])
    places = list(map(_place_obj, self._places))
    return core.ParallelExecutor(places, self._persistable_vars, self._program.desc, (cpt.to_text(self._loss_name) if self._loss_name else six.u('')), self._scope, self._local_scopes, self._exec_strategy, self._build_strategy)
