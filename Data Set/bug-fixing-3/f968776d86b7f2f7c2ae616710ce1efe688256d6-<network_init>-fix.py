def network_init(args, internal_targets):
    '\n    :type args: NetworkIntegrationConfig\n    :type internal_targets: tuple[IntegrationTarget]\n    '
    if (not args.platform):
        return
    if (args.metadata.instance_config is not None):
        return
    platform_targets = set((a for t in internal_targets for a in t.aliases if a.startswith('network/')))
    instances = []
    SshKey(args)
    for platform_version in args.platform:
        (platform, version) = platform_version.split('/', 1)
        platform_target = ('network/%s/' % platform)
        if (platform_target not in platform_targets):
            display.warning(('Skipping "%s" because selected tests do not target the "%s" platform.' % (platform_version, platform)))
            continue
        instance = lib.thread.WrappedThread(functools.partial(network_start, args, platform, version))
        instance.daemon = True
        instance.start()
        instances.append(instance)
    while any((instance.is_alive() for instance in instances)):
        time.sleep(1)
    args.metadata.instance_config = [instance.wait_for_result() for instance in instances]