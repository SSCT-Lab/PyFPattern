def container_run(platform: str, nvidia_runtime: bool, docker_registry: str, shared_memory_size: str, local_ccache_dir: str, command: List[str], cleanup: Cleanup, dry_run: bool=False) -> int:
    'Run command in a container'
    container_wait_s = 600
    environment = {
        'CCACHE_MAXSIZE': '500G',
        'CCACHE_TEMPDIR': '/tmp/ccache',
        'CCACHE_DIR': '/work/ccache',
        'CCACHE_LOGFILE': '/tmp/ccache.log',
    }
    jenkins_env_vars = ['BUILD_NUMBER', 'BUILD_ID', 'BUILD_TAG']
    environment.update({k: os.environ[k] for k in jenkins_env_vars if (k in os.environ)})
    environment.update({k: os.environ[k] for k in ['CCACHE_MAXSIZE'] if (k in os.environ)})
    tag = get_docker_tag(platform=platform, registry=docker_registry)
    mx_root = get_mxnet_root()
    local_build_folder = buildir()
    os.makedirs(local_build_folder, exist_ok=True)
    os.makedirs(local_ccache_dir, exist_ok=True)
    logging.info('Using ccache directory: %s', local_ccache_dir)
    docker_client = docker.from_env()
    docker_cmd_list = [get_docker_binary(nvidia_runtime), 'run', '--cap-add', 'SYS_PTRACE', '--rm', '--shm-size={}'.format(shared_memory_size), '-v', '{}:/work/mxnet'.format(mx_root), '-v', '{}:/work/build'.format(local_build_folder), '-v', '{}:/work/ccache'.format(local_ccache_dir), '-u', '{}:{}'.format(os.getuid(), os.getgid()), '-e', 'CCACHE_MAXSIZE={}'.format(environment['CCACHE_MAXSIZE']), '-e', 'CCACHE_TEMPDIR={}'.format(environment['CCACHE_TEMPDIR']), '-e', 'CCACHE_DIR={}'.format(environment['CCACHE_DIR']), '-e', 'CCACHE_LOGFILE={}'.format(environment['CCACHE_LOGFILE']), '-ti', tag]
    docker_cmd_list.extend(command)
    docker_cmd = ' \\\n\t'.join(docker_cmd_list)
    logging.info('Running %s in container %s', command, tag)
    logging.info('Executing the equivalent of:\n%s\n', docker_cmd)
    ret = 0
    if (not dry_run):
        signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGINT, signal.SIGTERM})
        runtime = None
        if nvidia_runtime:
            runtime = 'nvidia'
        container = docker_client.containers.run(tag, runtime=runtime, detach=True, command=command, shm_size=shared_memory_size, user='{}:{}'.format(os.getuid(), os.getgid()), cap_add='SYS_PTRACE', volumes={
            mx_root: {
                'bind': '/work/mxnet',
                'mode': 'rw',
            },
            local_build_folder: {
                'bind': '/work/build',
                'mode': 'rw',
            },
            local_ccache_dir: {
                'bind': '/work/ccache',
                'mode': 'rw',
            },
        }, environment=environment)
        try:
            logging.info('Started container: %s', trim_container_id(container.id))
            cleanup.add_container(container)
            signal.pthread_sigmask(signal.SIG_UNBLOCK, {signal.SIGINT, signal.SIGTERM})
            stream = container.logs(stream=True, stdout=True, stderr=True)
            sys.stdout.flush()
            for chunk in stream:
                sys.stdout.buffer.write(chunk)
                sys.stdout.buffer.flush()
            sys.stdout.flush()
            stream.close()
            try:
                logging.info('Waiting for status of container %s for %d s.', trim_container_id(container.id), container_wait_s)
                wait_result = container.wait(timeout=container_wait_s)
                logging.info('Container exit status: %s', wait_result)
                ret = wait_result.get('StatusCode', 200)
            except Exception as e:
                logging.exception(e)
                ret = 150
            try:
                logging.info('Stopping container: %s', trim_container_id(container.id))
                container.stop()
            except Exception as e:
                logging.exception(e)
                ret = 151
            try:
                logging.info('Removing container: %s', trim_container_id(container.id))
                container.remove()
            except Exception as e:
                logging.exception(e)
                ret = 152
            cleanup.remove_container(container)
            containers = docker_client.containers.list()
            if containers:
                logging.info('Other running containers: %s', [trim_container_id(x.id) for x in containers])
        except docker.errors.NotFound as e:
            logging.info('Container was stopped before cleanup started: %s', e)
    return ret