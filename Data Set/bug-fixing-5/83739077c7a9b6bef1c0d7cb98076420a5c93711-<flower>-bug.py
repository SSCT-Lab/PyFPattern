@cli_utils.action_logging
def flower(args):
    'Starts Flower, Celery monitoring tool'
    broka = conf.get('celery', 'BROKER_URL')
    address = '--address={}'.format(args.hostname)
    port = '--port={}'.format(args.port)
    api = ''
    if args.broker_api:
        api = ('--broker_api=' + args.broker_api)
    url_prefix = ''
    if args.url_prefix:
        url_prefix = ('--url-prefix=' + args.url_prefix)
    basic_auth = ''
    if args.basic_auth:
        basic_auth = ('--basic_auth=' + args.basic_auth)
    flower_conf = ''
    if args.flower_conf:
        flower_conf = ('--conf=' + args.flower_conf)
    if args.daemon:
        (pid, stdout, stderr, _) = setup_locations('flower', args.pid, args.stdout, args.stderr, args.log_file)
        stdout = open(stdout, 'w+')
        stderr = open(stderr, 'w+')
        ctx = daemon.DaemonContext(pidfile=TimeoutPIDLockFile(pid, (- 1)), stdout=stdout, stderr=stderr)
        with ctx:
            os.execvp('flower', ['flower', '-b', broka, address, port, api, flower_conf, url_prefix, basic_auth])
        stdout.close()
        stderr.close()
    else:
        signal.signal(signal.SIGINT, sigint_handler)
        signal.signal(signal.SIGTERM, sigint_handler)
        os.execvp('flower', ['flower', '-b', broka, address, port, api, flower_conf, url_prefix, basic_auth])