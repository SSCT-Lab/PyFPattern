def run(self, tmp=None, task_vars=None):
    ' generates params and passes them on to the rsync module '
    if (task_vars is None):
        task_vars = dict()
    _tmp_args = self._task.args.copy()
    result = super(ActionModule, self).run(tmp, task_vars)
    self._remote_transport = self._connection.transport
    if (self._remote_transport == 'docker'):
        self._docker_cmd = self._connection.docker_cmd
        if self._play_context.docker_extra_args:
            self._docker_cmd = ('%s %s' % (self._docker_cmd, self._play_context.docker_extra_args))
    remote_transport = False
    if (self._connection.transport != 'local'):
        remote_transport = True
    try:
        delegate_to = self._task.delegate_to
    except (AttributeError, KeyError):
        delegate_to = None
    if ((delegate_to is None) and (self._connection.transport not in ('ssh', 'paramiko', 'local', 'docker'))):
        result['failed'] = True
        result['msg'] = ('synchronize uses rsync to function. rsync needs to connect to the remote host via ssh, docker client or a direct filesystem copy. This remote host is being accessed via %s instead so it cannot work.' % self._connection.transport)
        return result
    use_ssh_args = _tmp_args.pop('use_ssh_args', None)
    _tmp_args['_local_rsync_path'] = (task_vars.get('ansible_rsync_path') or 'rsync')
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
    if (_tmp_args.get('dest_port', None) is None):
        if (inv_port is not None):
            _tmp_args['dest_port'] = inv_port
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
        localhost_executable = None
        for host in C.LOCALHOST:
            localhost_vars = task_vars['hostvars'].get(host, {
                
            })
            for executable_var in MAGIC_VARIABLE_MAPPING['executable']:
                localhost_executable = localhost_vars.get(executable_var, None)
                if localhost_executable:
                    break
            if localhost_executable:
                break
        else:
            localhost_executable = C.DEFAULT_EXECUTABLE
        self._play_context.executable = localhost_executable
        new_connection = connection_loader.get('local', self._play_context, new_stdin)
        self._connection = new_connection
        self._override_module_replaced_vars(task_vars)
    if (_tmp_args.get('mode', 'push') == 'pull'):
        (dest_host, src_host) = (src_host, dest_host)
    src = _tmp_args.get('src', None)
    dest = _tmp_args.get('dest', None)
    if ((src is None) or (dest is None)):
        return dict(failed=True, msg='synchronize requires both src and dest parameters are set')
    if (not dest_is_local):
        private_key = self._play_context.private_key_file
        if (private_key is not None):
            private_key = os.path.expanduser(private_key)
            _tmp_args['private_key'] = private_key
        user = None
        if boolean(_tmp_args.get('set_remote_user', 'yes')):
            if use_delegate:
                user = task_vars.get('ansible_delegated_vars', dict()).get('ansible_ssh_user', None)
                if (not user):
                    user = C.DEFAULT_REMOTE_USER
            else:
                user = (task_vars.get('ansible_ssh_user') or self._play_context.remote_user)
        if (_tmp_args.get('mode', 'push') == 'pull'):
            src = self._process_remote(_tmp_args, src_host, src, user, (inv_port in localhost_ports))
            dest = self._process_origin(dest_host, dest, user)
        else:
            src = self._process_origin(src_host, src, user)
            dest = self._process_remote(_tmp_args, dest_host, dest, user, (inv_port in localhost_ports))
    else:
        if (not src.startswith('/')):
            src = self._get_absolute_path(path=src)
        if (not dest.startswith('/')):
            dest = self._get_absolute_path(path=dest)
    _tmp_args['src'] = src
    _tmp_args['dest'] = dest
    rsync_path = _tmp_args.get('rsync_path', None)
    become = self._play_context.become
    if (not dest_is_local):
        if (self._play_context.become and (not rsync_path) and (self._remote_transport != 'docker')):
            if (self._play_context.become_method == 'sudo'):
                rsync_path = 'sudo rsync'
        self._play_context.become = False
    _tmp_args['rsync_path'] = rsync_path
    if use_ssh_args:
        ssh_args = [getattr(self._play_context, 'ssh_args', ''), getattr(self._play_context, 'ssh_common_args', ''), getattr(self._play_context, 'ssh_extra_args', '')]
        _tmp_args['ssh_args'] = ' '.join([a for a in ssh_args if a])
    if (self._remote_transport in ['docker']):
        if (not isinstance(_tmp_args.get('rsync_opts'), MutableSequence)):
            tmp_rsync_opts = _tmp_args.get('rsync_opts', [])
            if isinstance(tmp_rsync_opts, string_types):
                tmp_rsync_opts = tmp_rsync_opts.split(',')
            elif isinstance(tmp_rsync_opts, (int, float)):
                tmp_rsync_opts = [to_text(tmp_rsync_opts)]
            _tmp_args['rsync_opts'] = tmp_rsync_opts
        if ('--blocking-io' not in _tmp_args['rsync_opts']):
            _tmp_args['rsync_opts'].append('--blocking-io')
        if (become and self._play_context.become_user):
            _tmp_args['rsync_opts'].append(('--rsh=%s exec -u %s -i' % (self._docker_cmd, self._play_context.become_user)))
        elif (user is not None):
            _tmp_args['rsync_opts'].append(('--rsh=%s exec -u %s -i' % (self._docker_cmd, user)))
        else:
            _tmp_args['rsync_opts'].append(('--rsh=%s exec -i' % self._docker_cmd))
    result.update(self._execute_module('synchronize', module_args=_tmp_args, task_vars=task_vars))
    if ('SyntaxError' in result.get('exception', result.get('msg', ''))):
        result['exception'] = result['msg']
        result['msg'] = 'SyntaxError parsing module.  Perhaps invoking "python" on your local (or delegate_to) machine invokes python3. You can set ansible_python_interpreter for localhost (or the delegate_to machine) to the location of python2 to fix this'
    return result