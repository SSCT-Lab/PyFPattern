def get_commands(module, pkg, file_system):
    commands = []
    splitted_pkg = pkg.split('.')
    fixed_pkg = '.'.join(splitted_pkg[0:(- 1)])
    command = 'show install inactive'
    inactive_body = execute_show_command(command, module)
    command = 'show install active'
    active_body = execute_show_command(command, module)
    if ((fixed_pkg not in inactive_body[0]) and (fixed_pkg not in active_body[0])):
        commands.append('install add {0}{1}'.format(file_system, pkg))
    if (fixed_pkg not in active_body[0]):
        commands.append('install activate {0}{1} force'.format(file_system, pkg))
    command = 'show install committed'
    install_body = execute_show_command(command, module, command_type='cli_show_ascii')
    if (fixed_pkg not in install_body[0]):
        commands.append('install commit {0}{1}'.format(file_system, pkg))
    return commands