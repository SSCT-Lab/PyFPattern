def command_network_integration(args):
    '\n    :type args: NetworkIntegrationConfig\n    '
    internal_targets = command_integration_filter(args, walk_network_integration_targets())
    platform_targets = set((a for t in internal_targets for a in t.aliases if a.startswith('network/')))
    if args.platform:
        instances = []
        SshKey(args)
        for platform_version in args.platform:
            (platform, version) = platform_version.split('/', 1)
            platform_target = ('network/%s/' % platform)
            if ((platform_target not in platform_targets) and ('network/basics/' not in platform_targets)):
                display.warning(('Skipping "%s" because selected tests do not target the "%s" platform.' % (platform_version, platform)))
                continue
            instance = lib.thread.WrappedThread(functools.partial(network_run, args, platform, version))
            instance.daemon = True
            instance.start()
            instances.append(instance)
        install_command_requirements(args)
        while any((instance.is_alive() for instance in instances)):
            time.sleep(1)
        remotes = [instance.wait_for_result() for instance in instances]
        inventory = network_inventory(remotes)
        filename = 'test/integration/inventory.networking'
        display.info(('>>> Inventory: %s\n%s' % (filename, inventory.strip())), verbosity=3)
        if (not args.explain):
            with open(filename, 'w') as inventory_fd:
                inventory_fd.write(inventory)
    else:
        install_command_requirements(args)
    command_integration_filtered(args, internal_targets)