def command_windows_integration(args):
    '\n    :type args: WindowsIntegrationConfig\n    '
    filename = 'test/integration/inventory.winrm'
    if ((not args.explain) and (not args.windows) and (not os.path.isfile(filename))):
        raise ApplicationError(('Use the --windows option or provide an inventory file (see %s.template).' % filename))
    all_targets = tuple(walk_windows_integration_targets(include_hidden=True))
    internal_targets = command_integration_filter(args, all_targets, init_callback=windows_init)
    instances = []
    if args.windows:
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
    success = False
    try:
        command_integration_filtered(args, internal_targets, all_targets)
        success = True
    finally:
        if ((args.remote_terminate == 'always') or ((args.remote_terminate == 'success') and success)):
            for instance in instances:
                instance.result.stop()