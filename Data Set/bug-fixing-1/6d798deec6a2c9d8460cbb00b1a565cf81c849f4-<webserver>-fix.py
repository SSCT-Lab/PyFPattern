

@cli_utils.action_logging
def webserver(args):
    'Starts Airflow Webserver'
    print(settings.HEADER)
    access_logfile = (args.access_logfile or conf.get('webserver', 'access_logfile'))
    error_logfile = (args.error_logfile or conf.get('webserver', 'error_logfile'))
    num_workers = (args.workers or conf.get('webserver', 'workers'))
    worker_timeout = (args.worker_timeout or conf.get('webserver', 'web_server_worker_timeout'))
    ssl_cert = (args.ssl_cert or conf.get('webserver', 'web_server_ssl_cert'))
    ssl_key = (args.ssl_key or conf.get('webserver', 'web_server_ssl_key'))
    if ((not ssl_cert) and ssl_key):
        raise AirflowException(('An SSL certificate must also be provided for use with ' + ssl_key))
    if (ssl_cert and (not ssl_key)):
        raise AirflowException(('An SSL key must also be provided for use with ' + ssl_cert))
    if args.debug:
        print('Starting the web server on port {0} and host {1}.'.format(args.port, args.hostname))
        (app, _) = create_app(None, testing=conf.getboolean('core', 'unit_test_mode'))
        app.run(debug=True, use_reloader=(not app.config['TESTING']), port=args.port, host=args.hostname, ssl_context=((ssl_cert, ssl_key) if (ssl_cert and ssl_key) else None))
    else:
        os.environ['SKIP_DAGS_PARSING'] = 'True'
        app = cached_app(None)
        (pid, stdout, stderr, log_file) = setup_locations('webserver', args.pid, args.stdout, args.stderr, args.log_file)
        os.environ.pop('SKIP_DAGS_PARSING')
        if args.daemon:
            handle = setup_logging(log_file)
            stdout = open(stdout, 'w+')
            stderr = open(stderr, 'w+')
        print(textwrap.dedent('                Running the Gunicorn Server with:\n                Workers: {num_workers} {workerclass}\n                Host: {hostname}:{port}\n                Timeout: {worker_timeout}\n                Logfiles: {access_logfile} {error_logfile}\n                =================================================================            '.format(num_workers=num_workers, workerclass=args.workerclass, hostname=args.hostname, port=args.port, worker_timeout=worker_timeout, access_logfile=access_logfile, error_logfile=error_logfile)))
        run_args = ['gunicorn', '-w', str(num_workers), '-k', str(args.workerclass), '-t', str(worker_timeout), '-b', ((args.hostname + ':') + str(args.port)), '-n', 'airflow-webserver', '-p', str(pid), '-c', 'python:airflow.www.gunicorn_config']
        if args.access_logfile:
            run_args += ['--access-logfile', str(args.access_logfile)]
        if args.error_logfile:
            run_args += ['--error-logfile', str(args.error_logfile)]
        if args.daemon:
            run_args += ['-D']
        if ssl_cert:
            run_args += ['--certfile', ssl_cert, '--keyfile', ssl_key]
        webserver_module = 'www'
        run_args += [(('airflow.' + webserver_module) + '.app:cached_app()')]
        gunicorn_master_proc = None

        def kill_proc(dummy_signum, dummy_frame):
            gunicorn_master_proc.terminate()
            gunicorn_master_proc.wait()
            sys.exit(0)

        def monitor_gunicorn(gunicorn_master_proc):
            if (conf.getint('webserver', 'worker_refresh_interval') > 0):
                master_timeout = conf.getint('webserver', 'web_server_master_timeout')
                restart_workers(gunicorn_master_proc, num_workers, master_timeout)
            else:
                while (gunicorn_master_proc.poll() is None):
                    time.sleep(1)
                sys.exit(gunicorn_master_proc.returncode)
        if args.daemon:
            (base, ext) = os.path.splitext(pid)
            ctx = daemon.DaemonContext(pidfile=TimeoutPIDLockFile(((base + '-monitor') + ext), (- 1)), files_preserve=[handle], stdout=stdout, stderr=stderr, signal_map={
                signal.SIGINT: kill_proc,
                signal.SIGTERM: kill_proc,
            })
            with ctx:
                subprocess.Popen(run_args, close_fds=True)
                while True:
                    try:
                        with open(pid) as file:
                            gunicorn_master_proc_pid = int(file.read())
                            break
                    except OSError:
                        LOG.debug("Waiting for gunicorn's pid file to be created.")
                        time.sleep(0.1)
                gunicorn_master_proc = psutil.Process(gunicorn_master_proc_pid)
                monitor_gunicorn(gunicorn_master_proc)
            stdout.close()
            stderr.close()
        else:
            gunicorn_master_proc = subprocess.Popen(run_args, close_fds=True)
            signal.signal(signal.SIGINT, kill_proc)
            signal.signal(signal.SIGTERM, kill_proc)
            monitor_gunicorn(gunicorn_master_proc)
