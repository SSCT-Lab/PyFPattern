def get_cloud_platforms(args, targets=None):
    '\n    :type args: IntegrationConfig\n    :type targets: tuple[IntegrationTarget] | None\n    :rtype: list[str]\n    '
    if args.list_targets:
        return []
    if (targets is None):
        cloud_platforms = set((args.metadata.cloud_config or []))
    else:
        cloud_platforms = set((get_cloud_platform(t) for t in targets))
    cloud_platforms.discard(None)
    return sorted(cloud_platforms)