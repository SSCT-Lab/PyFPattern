def exec_command(self, cmd, become_user=None, sudoable=False, executable='/bin/sh', in_data=None):
    ' run a command on the remote minion '
    if in_data:
        raise errors.AnsibleError('Internal Error: this module does not support optimized module pipelining')
    vvv(('EXEC %s' % cmd), host=self.host)
    p = self.client.command.run(cmd)[self.host]
    return (p[0], p[1], p[2])