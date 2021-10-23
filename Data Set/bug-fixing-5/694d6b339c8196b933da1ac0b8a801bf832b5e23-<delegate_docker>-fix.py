def delegate_docker(args, exclude, require):
    '\n    :type args: EnvironmentConfig\n    :type exclude: list[str]\n    :type require: list[str]\n    '
    util_image = args.docker_util
    test_image = args.docker
    privileged = args.docker_privileged
    if util_image:
        docker_pull(args, util_image)
    docker_pull(args, test_image)
    util_id = None
    test_id = None
    options = {
        '--docker': 1,
        '--docker-privileged': 0,
        '--docker-util': 1,
    }
    cmd = generate_command(args, '/root/ansible/test/runner/test.py', options, exclude, require)
    if isinstance(args, TestConfig):
        if (args.coverage and (not args.coverage_label)):
            image_label = re.sub('^ansible/ansible:', '', args.docker)
            image_label = re.sub('[^a-zA-Z0-9]+', '-', image_label)
            cmd += ['--coverage-label', ('docker-%s' % image_label)]
    if isinstance(args, IntegrationConfig):
        if (not args.allow_destructive):
            cmd.append('--allow-destructive')
    cmd_options = []
    if (isinstance(args, ShellConfig) or (isinstance(args, IntegrationConfig) and args.debug_strategy)):
        cmd_options.append('-it')
    with tempfile.NamedTemporaryFile(prefix='ansible-source-', suffix='.tgz') as local_source_fd:
        try:
            if (not args.explain):
                if args.docker_keep_git:
                    tar_filter = lib.pytar.AllowGitTarFilter()
                else:
                    tar_filter = lib.pytar.DefaultTarFilter()
                lib.pytar.create_tarfile(local_source_fd.name, '.', tar_filter)
            if util_image:
                util_options = ['--detach']
                (util_id, _) = docker_run(args, util_image, options=util_options)
                if args.explain:
                    util_id = 'util_id'
                else:
                    util_id = util_id.strip()
            else:
                util_id = None
            test_options = ['--detach', '--volume', '/sys/fs/cgroup:/sys/fs/cgroup:ro', ('--privileged=%s' % str(privileged).lower())]
            if args.docker_memory:
                test_options.extend([('--memory=%d' % args.docker_memory), ('--memory-swap=%d' % args.docker_memory)])
            docker_socket = '/var/run/docker.sock'
            if os.path.exists(docker_socket):
                test_options += ['--volume', ('%s:%s' % (docker_socket, docker_socket))]
            if util_id:
                test_options += ['--link', ('%s:ansible.http.tests' % util_id), '--link', ('%s:sni1.ansible.http.tests' % util_id), '--link', ('%s:sni2.ansible.http.tests' % util_id), '--link', ('%s:fail.ansible.http.tests' % util_id), '--env', 'HTTPTESTER=1']
            if isinstance(args, IntegrationConfig):
                cloud_platforms = get_cloud_providers(args)
                for cloud_platform in cloud_platforms:
                    test_options += cloud_platform.get_docker_run_options()
            (test_id, _) = docker_run(args, test_image, options=test_options)
            if args.explain:
                test_id = 'test_id'
            else:
                test_id = test_id.strip()
            docker_put(args, test_id, 'test/runner/setup/docker.sh', '/root/docker.sh')
            docker_exec(args, test_id, ['/bin/bash', '/root/docker.sh'])
            docker_put(args, test_id, local_source_fd.name, '/root/ansible.tgz')
            docker_exec(args, test_id, ['mkdir', '/root/ansible'])
            docker_exec(args, test_id, ['tar', 'oxzf', '/root/ansible.tgz', '-C', '/root/ansible'])
            if (isinstance(args, UnitsConfig) and (not args.python)):
                cmd += ['--python', 'default']
            try:
                docker_exec(args, test_id, cmd, options=cmd_options)
            finally:
                with tempfile.NamedTemporaryFile(prefix='ansible-result-', suffix='.tgz') as local_result_fd:
                    docker_exec(args, test_id, ['tar', 'czf', '/root/results.tgz', '-C', '/root/ansible/test', 'results'])
                    docker_get(args, test_id, '/root/results.tgz', local_result_fd.name)
                    run_command(args, ['tar', 'oxzf', local_result_fd.name, '-C', 'test'])
        finally:
            if util_id:
                docker_rm(args, util_id)
            if test_id:
                docker_rm(args, test_id)