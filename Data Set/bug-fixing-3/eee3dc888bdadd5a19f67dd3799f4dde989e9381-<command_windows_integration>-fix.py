def command_windows_integration(args):
    '\n    :type args: WindowsIntegrationConfig\n    '
    filename = 'test/integration/inventory.winrm'
    if ((not args.explain) and (not args.windows) and (not os.path.isfile(filename))):
        raise ApplicationError(('Use the --windows option or provide an inventory file (see %s.template).' % filename))
    all_targets = tuple(walk_windows_integration_targets(include_hidden=True))
    internal_targets = command_integration_filter(args, all_targets, init_callback=windows_init)
    instances = []
    pre_target = None
    post_target = None
    httptester_id = None
    if args.windows:
        get_coverage_path(args, args.python_executable)
        configs = dict(((config['platform_version'], config) for config in args.metadata.instance_config))
        for version in args.windows:
            config = configs[('windows/%s' % version)]
            instance = lib.thread.WrappedThread(functools.partial(windows_run, args, version, config))
            instance.daemon = True
            instance.start()
            instances.append(instance)
        while any((instance.is_alive() for instance in instances)):
            time.sleep(1)
        remotes = [instance.wait_for_result() for instance in instances]
        inventory = windows_inventory(remotes)
        display.info(('>>> Inventory: %s\n%s' % (filename, inventory.strip())), verbosity=3)
        if (not args.explain):
            with open(filename, 'w') as inventory_fd:
                inventory_fd.write(inventory)
        use_httptester = (args.httptester and any((('needs/httptester/' in t.aliases) for t in internal_targets)))
        docker_httptester = bool(os.environ.get('HTTPTESTER', False))
        if (use_httptester and (not docker_available()) and (not docker_httptester)):
            display.warning('Assuming --disable-httptester since `docker` is not available.')
        elif use_httptester:
            if docker_httptester:
                first_host = HTTPTESTER_HOSTS[0]
                ssh_options = ['-R', ('8080:%s:80' % first_host), '-R', ('8443:%s:443' % first_host)]
            else:
                args.inject_httptester = True
                (httptester_id, ssh_options) = start_httptester(args)
            ssh_options.insert(0, '-fT')

            def forward_ssh_ports(target):
                '\n                :type target: IntegrationTarget\n                '
                if ('needs/httptester/' not in target.aliases):
                    return
                for remote in [r for r in remotes if (r.version != '2008')]:
                    manage = ManageWindowsCI(remote)
                    manage.upload('test/runner/setup/windows-httptester.ps1', watcher_path)
                    script = ('powershell.exe -NoProfile -ExecutionPolicy Bypass -Command .\\%s -Hosts %s' % (watcher_path, ', '.join(HTTPTESTER_HOSTS)))
                    if (args.verbosity > 3):
                        script += ' -Verbose'
                    manage.ssh(script, options=ssh_options, force_pty=False)

            def cleanup_ssh_ports(target):
                '\n                :type target: IntegrationTarget\n                '
                if ('needs/httptester/' not in target.aliases):
                    return
                for remote in [r for r in remotes if (r.version != '2008')]:
                    manage = ManageWindowsCI(remote)
                    manage.ssh(('del %s /F /Q' % watcher_path))
            watcher_path = ('ansible-test-http-watcher-%s.ps1' % time.time())
            pre_target = forward_ssh_ports
            post_target = cleanup_ssh_ports
    success = False
    try:
        command_integration_filtered(args, internal_targets, all_targets, filename, pre_target=pre_target, post_target=post_target)
        success = True
    finally:
        if httptester_id:
            docker_rm(args, httptester_id)
        if ((args.remote_terminate == 'always') or ((args.remote_terminate == 'success') and success)):
            for instance in instances:
                instance.result.stop()