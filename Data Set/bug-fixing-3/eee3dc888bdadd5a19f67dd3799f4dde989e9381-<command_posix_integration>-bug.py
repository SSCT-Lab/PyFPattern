def command_posix_integration(args):
    '\n    :type args: PosixIntegrationConfig\n    '
    all_targets = tuple(walk_posix_integration_targets(include_hidden=True))
    internal_targets = command_integration_filter(args, all_targets)
    command_integration_filtered(args, internal_targets, all_targets)