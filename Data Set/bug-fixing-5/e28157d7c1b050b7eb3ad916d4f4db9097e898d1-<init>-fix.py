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
    set_omp_mkl_env_vars(kwargs.get('trainer_count', 1))
    if ('use_gpu' in kwargs):
        cp.g_command_config_args['use_gpu'] = kwargs['use_gpu']
    if ('use_mkldnn' in kwargs):
        cp.g_command_config_args['use_mkldnn'] = kwargs['use_mkldnn']
    assert ('parallel_nn' not in kwargs), "currently 'parallel_nn' is not supported in v2 APIs."
    api.initPaddle(*args)