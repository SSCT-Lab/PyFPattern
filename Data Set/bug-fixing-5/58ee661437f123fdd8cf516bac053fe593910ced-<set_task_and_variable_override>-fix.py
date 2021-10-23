def set_task_and_variable_override(self, task, variables, templar):
    '\n        Sets attributes from the task if they are set, which will override\n        those from the play.\n        '
    new_info = self.copy()
    for attr in TASK_ATTRIBUTE_OVERRIDES:
        if hasattr(task, attr):
            attr_val = getattr(task, attr)
            if (attr_val is not None):
                setattr(new_info, attr, attr_val)
    if (task.delegate_to is not None):
        delegated_host_name = templar.template(task.delegate_to)
        delegated_vars = variables.get('ansible_delegated_vars', dict()).get(delegated_host_name, dict())
        delegated_transport = C.DEFAULT_TRANSPORT
        for transport_var in MAGIC_VARIABLE_MAPPING.get('connection'):
            if (transport_var in delegated_vars):
                delegated_transport = delegated_vars[transport_var]
                break
        for address_var in MAGIC_VARIABLE_MAPPING.get('remote_addr'):
            if (address_var in delegated_vars):
                break
        else:
            display.debug(('no remote address found for delegated host %s\nusing its name, so success depends on DNS resolution' % delegated_host_name))
            delegated_vars['ansible_host'] = delegated_host_name
        for port_var in MAGIC_VARIABLE_MAPPING.get('port'):
            if (port_var in delegated_vars):
                break
        else:
            if (delegated_transport == 'winrm'):
                delegated_vars['ansible_port'] = 5986
            else:
                delegated_vars['ansible_port'] = C.DEFAULT_REMOTE_PORT
        for user_var in MAGIC_VARIABLE_MAPPING.get('remote_user'):
            if ((user_var in delegated_vars) and delegated_vars[user_var]):
                break
        else:
            delegated_vars['ansible_user'] = (task.remote_user or self.remote_user)
    else:
        delegated_vars = dict()
        for exe_var in MAGIC_VARIABLE_MAPPING.get('executable'):
            if (exe_var in variables):
                setattr(new_info, 'executable', variables.get(exe_var))
    attrs_considered = []
    for (attr, variable_names) in iteritems(MAGIC_VARIABLE_MAPPING):
        for variable_name in variable_names:
            if (attr in attrs_considered):
                continue
            if (task.delegate_to is not None):
                if (isinstance(delegated_vars, dict) and (variable_name in delegated_vars)):
                    setattr(new_info, attr, delegated_vars[variable_name])
                    attrs_considered.append(attr)
            elif (variable_name in variables):
                setattr(new_info, attr, variables[variable_name])
                attrs_considered.append(attr)
    if (not new_info.become_pass):
        if ((new_info.become_method == 'sudo') and new_info.sudo_pass):
            setattr(new_info, 'become_pass', new_info.sudo_pass)
        elif ((new_info.become_method == 'su') and new_info.su_pass):
            setattr(new_info, 'become_pass', new_info.su_pass)
    for become_pass_name in MAGIC_VARIABLE_MAPPING.get('become_pass'):
        if (become_pass_name in variables):
            break
    else:
        if (new_info.become_method == 'sudo'):
            for sudo_pass_name in MAGIC_VARIABLE_MAPPING.get('sudo_pass'):
                if (sudo_pass_name in variables):
                    setattr(new_info, 'become_pass', variables[sudo_pass_name])
                    break
        if (new_info.become_method == 'sudo'):
            for su_pass_name in MAGIC_VARIABLE_MAPPING.get('su_pass'):
                if (su_pass_name in variables):
                    setattr(new_info, 'become_pass', variables[su_pass_name])
                    break
    if ((new_info.port is None) and (C.DEFAULT_REMOTE_PORT is not None)):
        new_info.port = int(C.DEFAULT_REMOTE_PORT)
    if (len(delegated_vars) > 0):
        for connection_type in MAGIC_VARIABLE_MAPPING.get('connection'):
            if (connection_type in delegated_vars):
                break
        else:
            remote_addr_local = (new_info.remote_addr in C.LOCALHOST)
            inv_hostname_local = (delegated_vars.get('inventory_hostname') in C.LOCALHOST)
            if (remote_addr_local and inv_hostname_local):
                setattr(new_info, 'connection', 'local')
            elif ((getattr(new_info, 'connection', None) == 'local') and ((not remote_addr_local) or (not inv_hostname_local))):
                setattr(new_info, 'connection', C.DEFAULT_TRANSPORT)
    if (new_info.connection == 'local'):
        new_info.connection_user = new_info.remote_user
        new_info.remote_user = pwd.getpwuid(os.getuid()).pw_name
    if (new_info.no_log is None):
        new_info.no_log = C.DEFAULT_NO_LOG
    task.set_become_defaults(new_info.become, new_info.become_method, new_info.become_user)
    if task.always_run:
        display.deprecated('always_run is deprecated. Use check_mode = no instead.', version='2.4', removed=False)
        new_info.check_mode = False
    if (task.check_mode is not None):
        new_info.check_mode = task.check_mode
    return new_info