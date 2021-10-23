

def run(self, tmp=None, task_vars=None):
    socket_path = None
    play_context = copy.deepcopy(self._play_context)
    play_context.network_os = self._get_network_os(task_vars)
    if (play_context.connection == 'local'):
        module_name = 'ansible.module_utils.network.{0}.{0}'.format(play_context.network_os)
        (f, p, d) = find_module('ansible')
        for package in module_name.split('.')[1:]:
            (f, p, d) = find_module(package, [p])
        module = load_module(module_name, f, p, d)
        self.provider = load_provider(module.get_provider_argspec(), self._task.args)
        if (play_context.network_os == 'junos'):
            play_context.connection = 'netconf'
            play_context.port = int((self.provider['port'] or self._play_context.port or 830))
        elif ((self.provider.get('transport') in ('nxapi', 'eapi')) and (play_context.network_os in ('nxos', 'eos'))):
            play_context.connection = play_context.connection
            play_context.port = int((self.provider['port'] or self._play_context.port or 22))
        else:
            play_context.connection = 'network_cli'
            play_context.port = int((self.provider['port'] or self._play_context.port or 22))
        play_context.remote_addr = (self.provider['host'] or self._play_context.remote_addr)
        play_context.remote_user = (self.provider['username'] or self._play_context.connection_user)
        play_context.password = (self.provider['password'] or self._play_context.password)
        play_context.private_key_file = (self.provider['ssh_keyfile'] or self._play_context.private_key_file)
        play_context.timeout = int((self.provider['timeout'] or C.PERSISTENT_COMMAND_TIMEOUT))
        if ('authorize' in self.provider.keys()):
            play_context.become = (self.provider['authorize'] or False)
            play_context.become_pass = self.provider['auth_pass']
            play_context.become_method = 'enable'
        if (self._play_context.connection == 'local'):
            if ((self.provider.get('transport') == 'nxapi') and (play_context.network_os == 'nxos')):
                self._task.args['provider'] = _NxosActionModule.nxapi_implementation(self.provider, self._play_context)
            elif ((self.provider.get('transport') == 'eapi') and (play_context.network_os == 'eos')):
                self._task.args['provider'] = _EosActionModule.eapi_implementation(self.provider, self._play_context)
            else:
                socket_path = self._start_connection(play_context)
                task_vars['ansible_socket'] = socket_path
    else:
        provider = self._task.args.get('provider', {
            
        })
        if any(provider.values()):
            display.warning(('provider is unnecessary when using connection=%s and will be ignored' % play_context.connection))
    if (play_context.connection == 'network_cli'):
        if (socket_path is None):
            socket_path = self._connection.socket_path
        conn = Connection(socket_path)
        out = conn.get_prompt()
        if to_text(out, errors='surrogate_then_replace').strip().endswith(')#'):
            display.vvvv('wrong context, sending exit to device', self._play_context.remote_addr)
            conn.send_command('exit')
    if ('fail_on_missing_module' not in self._task.args):
        self._task.args['fail_on_missing_module'] = False
    result = super(ActionModule, self).run(tmp, task_vars)
    module = self._get_implementation_module(play_context.network_os, self._task.action)
    if (not module):
        if self._task.args['fail_on_missing_module']:
            result['failed'] = True
        else:
            result['failed'] = False
        result['msg'] = ('Could not find implementation module %s for %s' % (self._task.action, play_context.network_os))
    else:
        new_module_args = self._task.args.copy()
        if ('network_os' in new_module_args):
            del new_module_args['network_os']
        del new_module_args['fail_on_missing_module']
        display.vvvv(('Running implementation module %s' % module))
        result.update(self._execute_module(module_name=module, module_args=new_module_args, task_vars=task_vars, wrap_async=self._task.async_val))
        display.vvvv(('Caching network OS %s in facts' % play_context.network_os))
        result['ansible_facts'] = {
            'network_os': play_context.network_os,
        }
    return result
