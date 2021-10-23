

def start_procs(args):
    '\n    '
    procs = []
    log_fns = []
    default_env = os.environ.copy()
    current_node_ip = args.node_ip
    node_ips = [x.strip() for x in args.cluster_node_ips.split(',')]
    node_id = node_ips.index(current_node_ip)
    if args.use_paddlecloud:
        trainer_nums = int(os.getenv('PADDLE_TRAINERS_NUM', '1'))
        if (trainer_nums != 1):
            current_node_ip = os.getenv('POD_IP')
            assert (current_node_ip is not None), 'POD_IP should not be None'
            node_ips = os.getenv('PADDLE_TRAINERS')
            assert (node_ips is not None), 'PADDLE_TRAINERS should not be None'
            node_ips = node_ips.split(',')
            node_id = os.getenv('PADDLE_TRAINER_ID')
            assert (node_id is not None), 'PADDLE_TRAINER_ID should not be None'
            node_id = int(node_id)
            if ((args.node_ip != '127.0.0.1') and (current_node_ip != args.node_ip)):
                logger.warning("Please NOTE: When using paddlecloud, current_node_ip is automatically got from POD_IP. Your input node_ip: {} doesn't equals to current_node_ip: {} from paddlecloud environment.".format(args.node_ip, current_node_ip))
            if ((args.cluster_node_ips != '127.0.0.1') and (args.cluster_node_ips != ','.join(node_ips))):
                logger.warning("Please NOTE: When using paddlecloud, cluster_node_ips is automatically got from PADDLE_TRAINERS(multi nodes) or POD_IP(single node).Your input cluster_node_ips: {} doesn't equals to IPs: {} from paddlecloud environment.".format(args.cluster_node_ips, node_ips))
    num_nodes = len(node_ips)
    if (args.selected_gpus is None):
        gpus_num = fluid.core.get_cuda_device_count()
        selected_gpus = [str(x) for x in range(0, gpus_num)]
    else:
        selected_gpus = [x.strip() for x in args.selected_gpus.split(',')]
    selected_gpus_num = len(selected_gpus)
    trainers_endpoints = ''
    for ip in node_ips:
        for i in range(selected_gpus_num):
            if (trainers_endpoints != ''):
                trainers_endpoints += ','
            trainers_endpoints += ('%s:%d' % (ip, (args.started_port + i)))
    nranks = (num_nodes * selected_gpus_num)
    if args.print_config:
        print('trainers_endpoints:', trainers_endpoints, ', node_id:', node_id, ', current_node_ip:', current_node_ip, ', num_nodes:', num_nodes, ', node_ips:', node_ips, ', nranks:', nranks)
    current_env = copy.copy(default_env)
    current_env.pop('http_proxy', None)
    current_env.pop('https_proxy', None)
    procs = []
    cmds = []
    ranks = []
    for i in range(0, selected_gpus_num):
        rank = ((node_id * selected_gpus_num) + i)
        current_env.update({
            'FLAGS_selected_gpus': ('%s' % selected_gpus[i]),
            'PADDLE_TRAINER_ID': ('%d' % rank),
            'PADDLE_CURRENT_ENDPOINT': ('%s:%d' % (current_node_ip, (args.started_port + i))),
            'PADDLE_TRAINERS_NUM': ('%d' % nranks),
            'PADDLE_TRAINER_ENDPOINTS': trainers_endpoints,
        })
        if (num_nodes > 1):
            current_env.update({
                'FLAGS_sync_nccl_allreduce': '0',
            })
        cmd = ([sys.executable, '-u', args.training_script] + args.training_script_args)
        cmds.append(cmd)
        if (args.log_dir is not None):
            os.system('mkdir -p {}'.format(args.log_dir))
            fn = open(('%s/workerlog.%d' % (args.log_dir, i)), 'w')
            log_fns.append(fn)
            proc = subprocess.Popen(cmd, env=current_env, stdout=fn, stderr=fn)
        else:
            proc = subprocess.Popen(cmd, env=current_env)
        procs.append(proc)
        ranks.append(rank)
    try:
        alive = True
        error = False
        error_rank = []
        while (alive and (not error)):
            alive = False
            for (rank, p) in zip(ranks, procs):
                ret = p.poll()
                if (ret is None):
                    alive = True
                elif (ret != 0):
                    error = True
                    error_rank.append(rank)
            time.sleep(1)
        if error:
            terminate_procs(procs)
            exit(1)
    except KeyboardInterrupt:
        logger.warning('KeyboardInterrupt, exit')
        terminate_procs(procs)
        raise
    except SystemExit:
        logger.error('ABORT!!! Out of all {} trainers, the trainer process with rank={} was aborted. Please check its log.'.format(nranks, error_rank))
        terminate_procs(procs)
        raise
    except:
        logger.error('ABORT!!! Out of all {} trainers, the trainer process with rank={} was aborted. Please check its log.'.format(nranks, error_rank))
        terminate_procs(procs)
        raise
    finally:
        for fn in log_fns:
            fn.close()
