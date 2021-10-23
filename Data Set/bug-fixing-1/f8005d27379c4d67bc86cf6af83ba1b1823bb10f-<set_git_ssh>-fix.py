

def set_git_ssh(ssh_wrapper, key_file, ssh_opts):
    os.environ['GIT_SSH'] = ssh_wrapper
    os.environ['GIT_SSH_COMMAND'] = ('%s %s' % (os.environ.get('SHELL', '/bin/sh'), ssh_wrapper))
    if os.environ.get('GIT_KEY'):
        del os.environ['GIT_KEY']
    if key_file:
        os.environ['GIT_KEY'] = key_file
    if os.environ.get('GIT_SSH_OPTS'):
        del os.environ['GIT_SSH_OPTS']
    if ssh_opts:
        os.environ['GIT_SSH_OPTS'] = ssh_opts
