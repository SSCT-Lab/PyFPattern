def substitute_controller(path):
    global client_addr
    if (not client_addr):
        ssh_env_string = os.environ.get('SSH_CLIENT', None)
        try:
            (client_addr, _) = ssh_env_string.split(None, 1)
        except AttributeError:
            ssh_env_string = os.environ.get('SSH_CONNECTION', None)
            try:
                (client_addr, _) = ssh_env_string.split(None, 1)
            except AttributeError:
                pass
        if (not client_addr):
            raise ValueError
    if path.startswith('localhost:'):
        path = path.replace('localhost', client_addr, 1)
    return path