

def get_integration_remote_filter(args, targets):
    '\n    :type args: IntegrationConfig\n    :type targets: tuple[IntegrationTarget]\n    :rtype: list[str]\n    '
    parts = args.remote.split('/', 1)
    platform = parts[0]
    exclude = []
    common_integration_filter(args, targets, exclude)
    skip = ('skip/%s/' % platform)
    skipped = [target.name for target in targets if (skip in target.aliases)]
    if skipped:
        exclude.append(skip)
        display.warning(('Excluding tests marked "%s" which are not supported on %s: %s' % (skip.rstrip('/'), platform, ', '.join(skipped))))
    skip = ('skip/%s/' % args.remote.replace('/', ''))
    skipped = [target.name for target in targets if (skip in target.aliases)]
    if skipped:
        exclude.append(skip)
        display.warning(('Excluding tests marked "%s" which are not supported on %s: %s' % (skip.rstrip('/'), platform, ', '.join(skipped))))
    python_version = 2
    skip = ('skip/python%d/' % python_version)
    skipped = [target.name for target in targets if (skip in target.aliases)]
    if skipped:
        exclude.append(skip)
        display.warning(('Excluding tests marked "%s" which are not supported on python %d: %s' % (skip.rstrip('/'), python_version, ', '.join(skipped))))
    return exclude
