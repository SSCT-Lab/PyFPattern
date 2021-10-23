def _get_delegated_vars(self, play, task, existing_variables):
    vars_copy = existing_variables.copy()
    templar = Templar(loader=self._loader, variables=vars_copy)
    items = []
    if (task.loop_with is not None):
        if (task.loop_with in lookup_loader):
            try:
                loop_terms = listify_lookup_plugin_terms(terms=task.loop, templar=templar, loader=self._loader, fail_on_undefined=True, convert_bare=False)
                items = lookup_loader.get(task.loop_with, loader=self._loader, templar=templar).run(terms=loop_terms, variables=vars_copy)
            except AnsibleUndefinedVariable:
                items = [None]
        else:
            raise AnsibleError(("Failed to find the lookup named '%s' in the available lookup plugins" % task.loop_with))
    elif (task.loop is not None):
        items = templar.template(task.loop)
    else:
        items = [None]
    delegated_host_vars = dict()
    item_var = getattr(task.loop_control, 'loop_var', 'item')
    cache_items = False
    for item in items:
        if (item is not None):
            vars_copy[item_var] = item
        templar.set_available_variables(vars_copy)
        delegated_host_name = templar.template(task.delegate_to, fail_on_undefined=False)
        if (delegated_host_name != task.delegate_to):
            cache_items = True
        if (delegated_host_name is None):
            raise AnsibleError(message='Undefined delegate_to host for task:', obj=task._ds)
        if (not isinstance(delegated_host_name, string_types)):
            raise AnsibleError(message=("the field 'delegate_to' has an invalid type (%s), and could not be converted to a string type." % type(delegated_host_name)), obj=task._ds)
        if (delegated_host_name in delegated_host_vars):
            continue
        new_port = C.DEFAULT_REMOTE_PORT
        if (C.DEFAULT_TRANSPORT == 'winrm'):
            new_port = 5986
        new_delegated_host_vars = dict(ansible_delegated_host=delegated_host_name, ansible_host=delegated_host_name, ansible_port=new_port, ansible_user=C.DEFAULT_REMOTE_USER, ansible_connection=C.DEFAULT_TRANSPORT)
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
                        delegated_host.vars = combine_vars(delegated_host.vars, new_delegated_host_vars)
        else:
            delegated_host = Host(name=delegated_host_name)
            delegated_host.vars = combine_vars(delegated_host.vars, new_delegated_host_vars)
        delegated_host_vars[delegated_host_name] = self.get_vars(play=play, host=delegated_host, task=task, include_delegate_to=False, include_hostvars=False)
    if cache_items:
        task.loop_with = None
        task.loop = items
    return delegated_host_vars