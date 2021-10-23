

def delegate_remote(args, exclude, require):
    '\n    :type args: EnvironmentConfig\n    :type exclude: list[str]\n    :type require: list[str]\n    '
    parts = args.remote.split('/', 1)
    platform = parts[0]
    version = parts[1]
    core_ci = AnsibleCoreCI(args, platform, version, stage=args.remote_stage)
    success = False
    try:
        core_ci.start()
        core_ci.wait()
        options = {
            '--remote': 1,
        }
        cmd = generate_command(args, 'ansible/test/runner/test.py', options, exclude, require)
        if isinstance(args, TestConfig):
            if (args.coverage and (not args.coverage_label)):
                cmd += ['--coverage-label', ('remote-%s-%s' % (platform, version))]
        if isinstance(args, IntegrationConfig):
            if (not args.allow_destructive):
                cmd.append('--allow-destructive')
        if (isinstance(args, UnitsConfig) and (not args.python)):
            cmd += ['--python', 'default']
        manage = ManagePosixCI(core_ci)
        manage.setup()
        ssh_options = []
        if isinstance(args, TestConfig):
            cloud_platforms = get_cloud_providers(args)
            for cloud_platform in cloud_platforms:
                ssh_options += cloud_platform.get_remote_ssh_options()
        try:
            manage.ssh(cmd, ssh_options)
            success = True
        finally:
            manage.ssh('rm -rf /tmp/results && cp -a ansible/test/results /tmp/results && chmod -R a+r /tmp/results')
            manage.download('/tmp/results', 'test')
    finally:
        if ((args.remote_terminate == 'always') or ((args.remote_terminate == 'success') and success)):
            core_ci.stop()
