def container_run(platform: str, docker_binary: str, docker_registry: str, shared_memory_size: str, local_ccache_dir: str, command: List[str], dry_run: bool=False, into_container: bool=False) -> str:
    tag = get_docker_tag(platform=platform, registry=docker_registry)
    mx_root = get_mxnet_root()
    local_build_folder = buildir()
    os.makedirs(local_build_folder, exist_ok=True)
    os.makedirs(local_ccache_dir, exist_ok=True)
    logging.info('Using ccache directory: %s', local_ccache_dir)
    runlist = [docker_binary, 'run', '--rm', '-t', '--shm-size={}'.format(shared_memory_size), '-v', '{}:/work/mxnet'.format(mx_root), '-v', '{}:/work/build'.format(local_build_folder), '-v', '{}:/work/ccache'.format(local_ccache_dir), '-u', '{}:{}'.format(os.getuid(), os.getgid()), '-e', 'CCACHE_MAXSIZE={}'.format(CCACHE_MAXSIZE), '-e', 'CCACHE_DIR=/work/ccache', tag]
    runlist.extend(command)
    cmd = ' '.join(runlist)
    if ((not dry_run) and (not into_container)):
        logging.info('Running %s in container %s', command, tag)
        logging.info('Executing: %s', cmd)
        ret = call(runlist)
    into_cmd = deepcopy(runlist)
    idx = (into_cmd.index('-u') + 2)
    into_cmd[idx:idx] = ['-ti', '--entrypoint', '/bin/bash']
    docker_run_cmd = ' '.join(into_cmd)
    if ((not dry_run) and into_container):
        check_call(into_cmd)
    if ((not dry_run) and (ret != 0)):
        logging.error('Running of command in container failed (%s): %s', ret, cmd)
        logging.error('You can try to get into the container by using the following command: %s', docker_run_cmd)
        raise subprocess.CalledProcessError(ret, cmd)
    return docker_run_cmd