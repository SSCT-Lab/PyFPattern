def remote_file_exists(module, dst, file_system='bootflash:'):
    command = 'dir {0}/{1}'.format(file_system, dst)
    body = execute_show_command(command, module, command_type='cli_show_ascii')
    if ('No such file' in body[0]):
        return False
    return True