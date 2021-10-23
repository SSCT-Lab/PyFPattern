def init(**kwargs):
    import py_paddle.swig_paddle as api
    args = []
    args_dict = {
        
    }
    for (ek, ev) in os.environ.iteritems():
        if ek.startswith('PADDLE_INIT_'):
            args_dict[ek.replace('PADDLE_INIT_', '').lower()] = str(ev)
    args_dict.update(kwargs)
    for key in args_dict.keys():
        args.append(('--%s=%s' % (key, str(args_dict[key]))))

    def set_env(key, value):
        'If the key has not been set in the environment, set it with value.'
        assert isinstance(key, str)
        assert isinstance(value, str)
        envset = os.environ.get(key)
        if (envset is None):
            os.environ[key] = value
    ht = os.popen('lscpu |grep "per core"|awk -F\':\' \'{print $2}\'|xargs')
    ht = int(ht.read())
    if (ht == 1):
        set_env('OMP_DYNAMIC', 'false')
        set_env('KMP_AFFINITY', 'granularity=fine,compact,0,0')
    else:
        set_env('OMP_DYNAMIC', 'true')
        set_env('KMP_AFFINITY', 'granularity=fine,compact,1,0')
    processors = os.popen('grep "processor" /proc/cpuinfo|sort -u|wc -l')
    processors = int(processors.read())
    trainers = kwargs.get('trainer_count', 1)
    threads = (processors / trainers)
    threads = ('1' if (threads < 1) else str(threads))
    set_env('OMP_NUM_THREADS', threads)
    set_env('MKL_NUM_THREADS', threads)
    if ('use_gpu' in kwargs):
        cp.g_command_config_args['use_gpu'] = kwargs['use_gpu']
    if ('use_mkldnn' in kwargs):
        cp.g_command_config_args['use_mkldnn'] = kwargs['use_mkldnn']
    assert ('parallel_nn' not in kwargs), "currently 'parallel_nn' is not supported in v2 APIs."
    api.initPaddle(*args)