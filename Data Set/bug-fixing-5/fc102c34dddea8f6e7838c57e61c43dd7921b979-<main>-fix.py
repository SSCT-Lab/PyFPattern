def main() -> int:
    base = os.path.split(os.path.realpath(__file__))[0]
    os.chdir(base)
    logging.getLogger().setLevel(logging.INFO)

    def script_name() -> str:
        return os.path.split(sys.argv[0])[1]
    logging.basicConfig(format='{}: %(asctime)-15s %(message)s'.format(script_name()))
    parser = argparse.ArgumentParser(description='Utility for building and testing MXNet on docker\n    containers', epilog='')
    parser.add_argument('-p', '--platform', help='platform', type=str)
    parser.add_argument('--build-only', help="Only build the container, don't build the project", action='store_true')
    parser.add_argument('-a', '--all', help='build for all platforms', action='store_true')
    parser.add_argument('-n', '--nvidiadocker', help='Use nvidia docker', action='store_true')
    parser.add_argument('--shm-size', help="Size of the shared memory /dev/shm allocated in the container (e.g '1g')", default='500m', dest='shared_memory_size')
    parser.add_argument('-l', '--list', help='List platforms', action='store_true')
    parser.add_argument('--print-docker-run', help='print docker run command for manual inspection', action='store_true')
    parser.add_argument('-i', '--into-container', help='go in a shell inside the container', action='store_true')
    parser.add_argument('-d', '--docker-registry', help="Dockerhub registry name to retrieve cache from. Default is 'mxnetci'", default='mxnetci', type=str)
    parser.add_argument('-c', '--cache', action='store_true', help='Enable docker registry cache')
    parser.add_argument('command', help='command to run in the container', nargs='*', action='append', type=str)
    parser.add_argument('--ccache-dir', default=default_ccache_dir(), help='Ccache directory', type=str)
    args = parser.parse_args()

    def use_cache():
        return (args.cache or ('JOB_NAME' in os.environ))
    command = list(chain(*args.command))
    docker_binary = get_docker_binary(args.nvidiadocker)
    shared_memory_size = args.shared_memory_size
    if args.list:
        list_platforms()
    elif args.platform:
        platform = args.platform
        tag = get_docker_tag(platform=platform, registry=args.docker_registry)
        if use_cache():
            load_docker_cache(tag=tag, docker_registry=args.docker_registry)
        build_docker(platform, docker_binary, registry=args.docker_registry)
        if args.build_only:
            logging.warning('Container was just built. Exiting due to build-only.')
            return 0
        if command:
            container_run(platform=platform, docker_binary=docker_binary, shared_memory_size=shared_memory_size, command=command, docker_registry=args.docker_registry, local_ccache_dir=args.ccache_dir)
        elif args.print_docker_run:
            print(container_run(platform=platform, docker_binary=docker_binary, shared_memory_size=shared_memory_size, command=[], dry_run=True, docker_registry=args.docker_registry, local_ccache_dir=args.ccache_dir))
        elif args.into_container:
            container_run(platform=platform, docker_binary=docker_binary, shared_memory_size=shared_memory_size, command=[], dry_run=False, into_container=True, docker_registry=args.docker_registry, local_ccache_dir=args.ccache_dir)
        else:
            cmd = ['/work/mxnet/ci/docker/runtime_functions.sh', 'build_{}'.format(platform)]
            logging.info('No command specified, trying default build: %s', ' '.join(cmd))
            container_run(platform=platform, docker_binary=docker_binary, shared_memory_size=shared_memory_size, command=cmd, docker_registry=args.docker_registry, local_ccache_dir=args.ccache_dir)
    elif args.all:
        platforms = get_platforms()
        logging.info('Building for all architectures: {}'.format(platforms))
        logging.info('Artifacts will be produced in the build/ directory.')
        for platform in platforms:
            tag = get_docker_tag(platform=platform, registry=args.docker_registry)
            if use_cache():
                load_docker_cache(tag=tag, docker_registry=args.docker_registry)
            build_docker(platform, docker_binary, args.docker_registry)
            if args.build_only:
                continue
            build_platform = 'build_{}'.format(platform)
            cmd = ['/work/mxnet/ci/docker/runtime_functions.sh', build_platform]
            shutil.rmtree(buildir(), ignore_errors=True)
            container_run(platform=platform, docker_binary=docker_binary, shared_memory_size=shared_memory_size, command=cmd, docker_registry=args.docker_registry, local_ccache_dir=args.ccache_dir)
            plat_buildir = os.path.join(get_mxnet_root(), build_platform)
            shutil.move(buildir(), plat_buildir)
            logging.info('Built files left in: %s', plat_buildir)
    else:
        parser.print_help()
        list_platforms()
        print('\nExamples:\n\n./build.py -p armv7\n\n    Will build a docker container with cross compilation tools and build MXNet for armv7 by\n    running: ci/docker/runtime_functions.sh build_armv7 inside the container.\n\n./build.py -p armv7 ls\n\n    Will execute the given command inside the armv7 container\n\n./build.py -p armv7 --print-docker-run\n\n    Will print a docker run command to get inside the container in an interactive shell\n\n./build.py -p armv7 --into-container\n\n    Will execute a shell into the container\n\n./build.py -a\n\n    Builds for all platforms and leaves artifacts in build_<platform>\n\n    ')
    return 0