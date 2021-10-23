def start_procs(gpus, entrypoint, entrypoint_args, log_dir):
    procs = []
    log_fns = []
    os.system(('mkdir -p %s' % log_dir))
    for (k, v) in os.environ.items():
        if (k.startswith('FLAGS_') or k.startswith('NCCL_') or k.startswith('GLOG_')):
            default_envs[k] = v
    node_trainer_id = int(os.getenv('PADDLE_TRAINER_ID', '0'))
    current_ip = os.getenv('POD_IP', '127.0.0.1')
    trainer_ips = os.getenv('PADDLE_TRAINERS', current_ip).split(',')
    num_nodes = len(trainer_ips)
    all_nodes_devices_endpoints = ''
    for n in trainer_ips:
        for i in range(gpus):
            if all_nodes_devices_endpoints:
                all_nodes_devices_endpoints += ','
            all_nodes_devices_endpoints += ('%s:617%d' % (n, i))
    nranks = (num_nodes * gpus)
    gpu_ids = get_gpu_ids(gpus)
    for i in gpu_ids:
        curr_env = {
            
        }
        curr_env.update(default_envs)
        curr_env.update({
            'FLAGS_selected_gpus': ('%d' % i),
            'PADDLE_TRAINER_ID': ('%d' % ((node_trainer_id * gpus) + i)),
            'PADDLE_CURRENT_ENDPOINT': ('%s:617%d' % (current_ip, i)),
            'PADDLE_TRAINERS_NUM': ('%d' % nranks),
            'PADDLE_TRAINER_ENDPOINTS': all_nodes_devices_endpoints,
        })
        print('starting process ', i, entrypoint, entrypoint_args, curr_env)
        fn = open(('%s/workerlog.%d' % (log_dir, i)), 'w')
        log_fns.append(fn)
        cmd = ([sys.executable, '-u', entrypoint] + entrypoint_args)
        procs.append(subprocess.Popen(cmd, stdout=fn, stderr=fn, env=curr_env))
    for i in range(gpus):
        try:
            procs[i].communicate()
            procs[i].terminate()
            log_fns[i].close()
        except:
            pass