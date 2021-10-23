

def set_omp_mkl_env_vars(trainer_count):
    'Auto set CPU environment if have not set before.\n       export KMP_AFFINITY, OMP_DYNAMIC according to the Hyper Threading status.\n       export OMP_NUM_THREADS, MKL_NUM_THREADS according to trainer_count.\n    '
    import platform
    if (not (platform.system() in ['Linux', 'Darwin'])):
        return

    def set_env(key, value):
        'If the key has not been set in the environment, set it with value.'
        assert isinstance(key, str)
        assert isinstance(value, str)
        envset = os.environ.get(key)
        if (envset is None):
            os.environ[key] = value

    def num_physical_cores():
        'Get the number of physical cores'
        if (platform.system() == 'Linux'):
            num_sockets = int(os.popen('lscpu |grep "Socket" |awk -F\':\' \'{print $2}\'|xargs').read())
            num_cores_per_socket = int(os.popen('lscpu |grep "per socket" |awk -F\':\' \'{print $2}\'|xargs').read())
            return (num_sockets * num_cores_per_socket)
        else:
            cmds = {
                'Darwin': 'sysctl hw.physicalcpu',
            }
            return int(os.popen(cmds.get(platform.system(), 'expr 1')).read())

    def num_logical_processors():
        'Get the number of logical processors'
        cmds = {
            'Linux': 'grep "processor" /proc/cpuinfo|sort -u|wc -l',
            'Darwin': 'sysctl hw.logicalcpu',
        }
        return int(os.popen(cmds.get(platform.system(), 'expr 1')).read())
    num_cores = num_physical_cores()
    num_processors = num_logical_processors()
    if (num_processors > num_cores):
        set_env('OMP_DYNAMIC', 'true')
        set_env('KMP_AFFINITY', 'granularity=fine,compact,1,0')
    else:
        set_env('OMP_DYNAMIC', 'false')
        set_env('KMP_AFFINITY', 'granularity=fine,compact,0,0')
    threads = (num_processors / trainer_count)
    threads = ('1' if (threads < 1) else str(threads))
    set_env('OMP_NUM_THREADS', threads)
    set_env('MKL_NUM_THREADS', threads)
