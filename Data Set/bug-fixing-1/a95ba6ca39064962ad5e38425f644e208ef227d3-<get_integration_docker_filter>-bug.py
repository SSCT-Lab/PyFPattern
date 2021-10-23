

def get_integration_docker_filter(args, targets):
    '\n    :type args: IntegrationConfig\n    :type targets: tuple[IntegrationTarget]\n    :rtype: list[str]\n    '
    exclude = []
    common_integration_filter(args, targets, exclude)
    skip = 'skip/docker/'
    skipped = [target.name for target in targets if (skip in target.aliases)]
    if skipped:
        exclude.append(skip)
        display.warning(('Excluding tests marked "%s" which cannot run under docker: %s' % (skip.rstrip('/'), ', '.join(skipped))))
    if (not args.docker_privileged):
        skip = 'needs/privileged/'
        skipped = [target.name for target in targets if (skip in target.aliases)]
        if skipped:
            exclude.append(skip)
            display.warning(('Excluding tests marked "%s" which require --docker-privileged to run under docker: %s' % (skip.rstrip('/'), ', '.join(skipped))))
    python_version = 2
    python_version = int(get_docker_completion().get(args.docker_raw).get('python', str(python_version)))
    if args.python:
        if args.python.startswith('3'):
            python_version = 3
        elif args.python.startswith('2'):
            python_version = 2
    skip = ('skip/python%d/' % python_version)
    skipped = [target.name for target in targets if (skip in target.aliases)]
    if skipped:
        exclude.append(skip)
        display.warning(('Excluding tests marked "%s" which are not supported on python %d: %s' % (skip.rstrip('/'), python_version, ', '.join(skipped))))
    return exclude
