

def run(self, tmp=None, task_vars=None):
    ' generates params and passes them on to the rsync module '
    if (task_vars is None):
        task_vars = dict()
    result = super(ActionModule, self).run(tmp, task_vars)
    remote_transport = False
    if (self._connection.transport != 'local'):
        remote_transport = True
    try:
        delegate_to = self._task.delegate_to
    except (AttributeError, KeyError):
        delegate_to = None
    if ((delegate_to is None) and (self._connection.transport not in ('ssh', 'paramiko', 'local'))):
        result['failed'] = True
        result['msg'] = ('synchronize uses rsync to function. rsync needs to connect to the remote host via ssh or a direct filesystem copy. This remote host is being accessed via %s instead so it cannot work.' % self._connection.transport)
        return result
    use_ssh_args = self._task.args.pop('use_ssh_args', None)
    self._task.args['_local_rsync_path'] = (task_vars.get('ansible_rsync_path') or 'rsync')
    src_host = '127.0.0.1'
    inventory_hostname = task_vars.get('inventory_hostname')
    dest_host_inventory_vars = task_vars['hostvars'].get(inventory_hostname)
    try:
        dest_host = dest_host_inventory_vars['ansible_host']
    except KeyError:
        dest_host = dest_host_inventory_vars.get('ansible_ssh_host', inventory_hostname)
    localhost_ports = set()
    for host in C.LOCALHOST:
        localhost_vars = task_vars['hostvars'].get(host, {
            
        })
        for port_var in MAGIC_VARIABLE_MAPPING['port']:
            port = localhost_vars.get(port_var, None)
            if port:
                break
        else:
            port = C.DEFAULT_REMOTE_PORT
        localhost_ports.add(port)
    dest_is_local = False
    if ((not delegate_to) and (remote_transport is False)):
        dest_is_local = True
    elif (delegate_to and (delegate_to == dest_host)):
        dest_is_local = True
    inv_port = (task_vars.get('ansible_ssh_port', None) or C.DEFAULT_REMOTE_PORT)
    if (self._task.args.get('dest_port', None) is None):
        if (inv_port is not None):
            self._task.args['dest_port'] = inv_port
    use_delegate = False
    if (dest_host == delegate_to):
        dest_host = '127.0.0.1'
        use_delegate = True
    elif ((delegate_to is not None) and remote_transport):
        use_delegate = True
    if ((not use_delegate) and remote_transport):
        new_stdin = self._connection._new_stdin
        localhost_shell = None
        for host in C.LOCALHOST:
            localhost_vars = task_vars['hostvars'].get(host, {
                
            })
            for shell_var in MAGIC_VARIABLE_MAPPING['shell']:
                localhost_shell = localhost_vars.get(shell_var, None)
                if localhost_shell:
                    break
            if localhost_shell:
                break
        else:
            localhost_shell = os.path.basename(C.DEFAULT_EXECUTABLE)
        self._play_context.shell = localhost_shell
        new_connection = connection_loader.get('local', self._play_context, new_stdin)
        self._connection = new_connection
        self._override_module_replaced_vars(task_vars)
    if (self._task.args.get('mode', 'push') == 'pull'):
        (dest_host, src_host) = (src_host, dest_host)
    src = self._task.args.get('src', None)
    dest = self._task.args.get('dest', None)
    if ((src is None) or (dest is None)):
        return dict(failed=True, msg='synchronize requires both src and dest parameters are set')
    if (not dest_is_local):
        private_key = self._play_context.private_key_file
        if (private_key is not None):
            private_key = os.path.expanduser(private_key)
            self._task.args['private_key'] = private_key
        user = None
        if boolean(self._task.args.get('set_remote_user', 'yes')):
            if use_delegate:
                user = task_vars.get('ansible_delegated_vars', dict()).get('ansible_ssh_user', None)
                if (not user):
                    user = C.DEFAULT_REMOTE_USER
            else:
                user = (task_vars.get('ansible_ssh_user') or self._play_context.remote_user)
        if (self._task.args.get('mode', 'push') == 'pull'):
            src = self._process_remote(src_host, src, user, (inv_port in localhost_ports))
            dest = self._process_origin(dest_host, dest, user)
        else:
            src = self._process_origin(src_host, src, user)
            dest = self._process_remote(dest_host, dest, user, (inv_port in localhost_ports))
    else:
        if (not src.startswith('/')):
            src = self._get_absolute_path(path=src)
        if (not dest.startswith('/')):
            dest = self._get_absolute_path(path=dest)
    self._task.args['src'] = src
    self._task.args['dest'] = dest
    rsync_path = self._task.args.get('rsync_path', None)
    if (not dest_is_local):
        if (self._play_context.become and (not rsync_path)):
            if (self._play_context.become_method == 'sudo'):
                rsync_path = 'sudo rsync'
        self._play_context.become = False
    if rsync_path:
        self._task.args['rsync_path'] = ('"%s"' % rsync_path)
    if use_ssh_args:
        ssh_args = [getattr(self._play_context, 'ssh_args', ''), getattr(self._play_context, 'ssh_common_args', ''), getattr(self._play_context, 'ssh_extra_args', '')]
        self._task.args['ssh_args'] = ' '.join([a for a in ssh_args if a])
    result.update(self._execute_module('synchronize', task_vars=task_vars))
    if ('SyntaxError' in result.get('exception', result.get('msg', ''))):
        result['exception'] = result['msg']
        result['msg'] = 'SyntaxError parsing module.  Perhaps invoking "python" on your local (or delegate_to) machine invokes python3.  You can set ansible_python_interpreter for localhost (or the delegate_to machine) to the location of python2 to fix this'
    return result
