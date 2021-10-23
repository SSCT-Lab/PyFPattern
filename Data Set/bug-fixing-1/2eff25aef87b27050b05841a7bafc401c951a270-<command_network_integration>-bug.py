

def command_network_integration(args):
    '\n    :type args: NetworkIntegrationConfig\n    '
    inventory_relative_path = get_inventory_relative_path(args)
    template_path = (os.path.join(ANSIBLE_TEST_CONFIG_ROOT, os.path.basename(inventory_relative_path)) + '.template')
    if args.inventory:
        inventory_path = os.path.join(data_context().content.root, INTEGRATION_DIR_RELATIVE, args.inventory)
    else:
        inventory_path = os.path.join(data_context().content.root, inventory_relative_path)
    if ((not args.explain) and (not args.platform) and (not os.path.isfile(inventory_path))):
        raise ApplicationError(('Inventory not found: %s\nUse --inventory to specify the inventory path.\nUse --platform to provision resources and generate an inventory file.\nSee also inventory template: %s' % (inventory_path, template_path)))
    check_inventory(args, inventory_path)
    delegate_inventory(args, inventory_path)
    all_targets = tuple(walk_network_integration_targets(include_hidden=True))
    internal_targets = command_integration_filter(args, all_targets, init_callback=network_init)
    instances = []
    if args.platform:
        get_python_path(args, args.python_executable)
        configs = dict(((config['platform_version'], config) for config in args.metadata.instance_config))
        for platform_version in args.platform:
            (platform, version) = platform_version.split('/', 1)
            config = configs.get(platform_version)
            if (not config):
                continue
            instance = WrappedThread(functools.partial(network_run, args, platform, version, config))
            instance.daemon = True
            instance.start()
            instances.append(instance)
        while any((instance.is_alive() for instance in instances)):
            time.sleep(1)
        remotes = [instance.wait_for_result() for instance in instances]
        inventory = network_inventory(remotes)
        display.info(('>>> Inventory: %s\n%s' % (inventory_path, inventory.strip())), verbosity=3)
        if (not args.explain):
            with open(inventory_path, 'w') as inventory_fd:
                inventory_fd.write(inventory)
    success = False
    try:
        command_integration_filtered(args, internal_targets, all_targets, inventory_path)
        success = True
    finally:
        if ((args.remote_terminate == 'always') or ((args.remote_terminate == 'success') and success)):
            for instance in instances:
                instance.result.stop()
