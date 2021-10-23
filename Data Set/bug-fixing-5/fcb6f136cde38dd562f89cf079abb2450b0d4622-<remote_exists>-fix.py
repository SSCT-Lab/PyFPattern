def remote_exists(module, binary, name, method):
    'Check if the remote exists.'
    command = '{0} remote-list -d --{1}'.format(binary, method)
    output = _flatpak_command(module, False, command)
    for line in output.splitlines():
        listed_remote = line.split()
        if (len(listed_remote) == 0):
            continue
        if (listed_remote[0] == to_native(name)):
            return True
    return False