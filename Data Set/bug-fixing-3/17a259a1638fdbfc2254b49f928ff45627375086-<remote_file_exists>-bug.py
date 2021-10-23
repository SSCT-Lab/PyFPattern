def remote_file_exists(module, dst, file_system='bootflash:'):
    command = 'dir {0}/{1}'.format(file_system, dst)
    body = run_commands(module, [command])[0]
    if ('No such file' in body):
        return False
    return True