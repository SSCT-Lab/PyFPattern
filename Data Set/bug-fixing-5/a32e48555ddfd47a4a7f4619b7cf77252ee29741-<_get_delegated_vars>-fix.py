def _get_delegated_vars(self, loader, play, task, existing_variables):
    vars_copy = existing_variables.copy()
    templar = Templar(loader=loader, variables=vars_copy)
    items = []
    if (task.loop is not None):
        if (task.loop in lookup_loader):
            try:
                loop_terms = listify_lookup_plugin_terms(terms=task.loop_args, templar=templar, loader=loader, fail_on_undefined=True, convert_bare=False)
                items = lookup_loader.get(task.loop, loader=loader, templar=templar).run(terms=loop_terms, variables=vars_copy)
            except AnsibleUndefinedVariable as e:
                items = [None]
        else:
            raise AnsibleError(("Unexpected failure in finding the lookup named '%s' in the available lookup plugins" % task.loop))
    else:
        items = [None]
    delegated_host_vars = dict()
    for item in items:
        if (item is not None):
            vars_copy['item'] = item
        templar.set_available_variables(vars_copy)
        delegated_host_name = templar.template(task.delegate_to, fail_on_undefined=False)
        if (delegated_host_name is None):
            raise AnsibleError(message='Undefined delegate_to host for task:', obj=task._ds)
        if (delegated_host_name in delegated_host_vars):
            continue
        new_port = C.DEFAULT_REMOTE_PORT
        if (C.DEFAULT_TRANSPORT == 'winrm'):
            new_port = 5986
        new_delegated_host_vars = dict(ansible_host=delegated_host_name, ansible_port=new_port, ansible_user=C.DEFAULT_REMOTE_USER, ansible_connection=C.DEFAULT_TRANSPORT)
        delegated_host = None
        if (self._inventory is not None):
            delegated_host = self._inventory.get_host(delegated_host_name)
            if (delegated_host is None):
                if (delegated_host_name in C.LOCALHOST):
                    delegated_host = self._inventory.localhost
                else:
                    for h in self._inventory.get_hosts(ignore_limits=True, ignore_restrictions=True):
                        if (h.address == delegated_host_name):
                            delegated_host = h
                            break
                    else:
                        delegated_host = Host(name=delegated_host_name)
                        delegated_host.vars.update(new_delegated_host_vars)
        else:
            delegated_host = Host(name=delegated_host_name)
            delegated_host.vars.update(new_delegated_host_vars)
        delegated_host_vars[delegated_host_name] = self.get_vars(loader=loader, play=play, host=delegated_host, task=task, include_delegate_to=False, include_hostvars=False)
    return delegated_host_vars