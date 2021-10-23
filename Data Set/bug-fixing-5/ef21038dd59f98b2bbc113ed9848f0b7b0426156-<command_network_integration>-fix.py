def command_network_integration(args):
    '\n    :type args: NetworkIntegrationConfig\n    '
    default_filename = 'test/integration/inventory.networking'
    if args.inventory:
        filename = os.path.join('test/integration', args.inventory)
    else:
        filename = default_filename
    if ((not args.explain) and (not args.platform) and (not os.path.exists(filename))):
        if args.inventory:
            filename = os.path.abspath(filename)
        raise ApplicationError(('Inventory not found: %s\nUse --inventory to specify the inventory path.\nUse --platform to provision resources and generate an inventory file.\nSee also inventory template: %s.template' % (filename, default_filename)))
    all_targets = tuple(walk_network_integration_targets(include_hidden=True))
    internal_targets = command_integration_filter(args, all_targets, init_callback=network_init)
    instances = []
    if args.platform:
        get_coverage_path(args)
        configs = dict(((config['platform_version'], config) for config in args.metadata.instance_config))
        for platform_version in args.platform:
            (platform, version) = platform_version.split('/', 1)
            config = configs.get(platform_version)
            if (not config):
                continue
            instance = lib.thread.WrappedThread(functools.partial(network_run, args, platform, version, config))
            instance.daemon = True
            instance.start()
            instances.append(instance)
        while any((instance.is_alive() for instance in instances)):
            time.sleep(1)
        remotes = [instance.wait_for_result() for instance in instances]
        inventory = network_inventory(remotes)
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