def get_vars(self, loader, play=None, host=None, task=None, include_hostvars=True, include_delegate_to=True, use_cache=True):
    '\n        Returns the variables, with optional "context" given via the parameters\n        for the play, host, and task (which could possibly result in different\n        sets of variables being returned due to the additional context).\n\n        The order of precedence is:\n        - play->roles->get_default_vars (if there is a play context)\n        - group_vars_files[host] (if there is a host context)\n        - host_vars_files[host] (if there is a host context)\n        - host->get_vars (if there is a host context)\n        - fact_cache[host] (if there is a host context)\n        - play vars (if there is a play context)\n        - play vars_files (if there\'s no host context, ignore\n          file names that cannot be templated)\n        - task->get_vars (if there is a task context)\n        - vars_cache[host] (if there is a host context)\n        - extra vars\n        '
    display.debug('in VariableManager get_vars()')
    cache_entry = self._get_cache_entry(play=play, host=host, task=task)
    if ((cache_entry in VARIABLE_CACHE) and use_cache):
        display.debug('vars are cached, returning them now')
        return VARIABLE_CACHE[cache_entry]
    all_vars = dict()
    magic_variables = self._get_magic_variables(loader=loader, play=play, host=host, task=task, include_hostvars=include_hostvars, include_delegate_to=include_delegate_to)
    if play:
        for role in play.get_roles():
            all_vars = combine_vars(all_vars, role.get_default_vars())
    if (task and (task._role is not None) and (play or (task.action == 'include_role'))):
        all_vars = combine_vars(all_vars, task._role.get_default_vars(dep_chain=task.get_dep_chain()))
    if host:
        all_vars = combine_vars(all_vars, host.get_group_vars())
        if ('all' in self._group_vars_files):
            data = preprocess_vars(self._group_vars_files['all'])
            for item in data:
                all_vars = combine_vars(all_vars, item)
        for group in sorted(host.get_groups(), key=(lambda g: (g.depth, g.priority, g.name))):
            if ((group.name in self._group_vars_files) and (group.name != 'all')):
                for data in self._group_vars_files[group.name]:
                    data = preprocess_vars(data)
                    for item in data:
                        all_vars = combine_vars(all_vars, item)
        all_vars = combine_vars(all_vars, host.get_vars())
        host_name = host.get_name()
        if (host_name in self._host_vars_files):
            for data in self._host_vars_files[host_name]:
                data = preprocess_vars(data)
                for item in data:
                    all_vars = combine_vars(all_vars, item)
        try:
            host_facts = wrap_var(self._fact_cache.get(host.name, dict()))
            if (not C.NAMESPACE_FACTS):
                all_vars = combine_vars(all_vars, host_facts)
            all_vars = combine_vars(all_vars, {
                'ansible_facts': host_facts,
            })
            if ('ansible_local' in all_vars['ansible_facts']):
                all_vars.update({
                    'ansible_local': all_vars['ansible_facts']['ansible_local'],
                })
            else:
                all_vars.update({
                    'ansible_local': {
                        
                    },
                })
            if ('ansible_local' in all_vars['ansible_facts']):
                del all_vars['ansible_facts']['ansible_local']
        except KeyError:
            pass
    if play:
        all_vars = combine_vars(all_vars, play.get_vars())
        for vars_file_item in play.get_vars_files():
            temp_vars = combine_vars(all_vars, self._extra_vars)
            temp_vars = combine_vars(temp_vars, magic_variables)
            templar = Templar(loader=loader, variables=temp_vars)
            vars_file_list = vars_file_item
            if (not isinstance(vars_file_list, list)):
                vars_file_list = [vars_file_list]
            try:
                for vars_file in vars_file_list:
                    vars_file = templar.template(vars_file)
                    try:
                        data = preprocess_vars(loader.load_from_file(vars_file))
                        if (data is not None):
                            for item in data:
                                all_vars = combine_vars(all_vars, item)
                        break
                    except AnsibleFileNotFound:
                        continue
                    except AnsibleParserError:
                        raise
                else:
                    if include_delegate_to:
                        raise AnsibleFileNotFound(('vars file %s was not found' % vars_file_item))
            except (UndefinedError, AnsibleUndefinedVariable):
                if ((host is not None) and self._fact_cache.get(host.name, dict()).get('module_setup') and (task is not None)):
                    raise AnsibleUndefinedVariable(("an undefined variable was found when attempting to template the vars_files item '%s'" % vars_file_item), obj=vars_file_item)
                else:
                    display.vvv(("skipping vars_file '%s' due to an undefined variable" % vars_file_item))
                    continue
        if (not C.DEFAULT_PRIVATE_ROLE_VARS):
            for role in play.get_roles():
                all_vars = combine_vars(all_vars, role.get_vars(include_params=False))
    if task:
        if task._role:
            all_vars = combine_vars(all_vars, task._role.get_vars(task.get_dep_chain(), include_params=False))
        all_vars = combine_vars(all_vars, task.get_vars())
    if host:
        all_vars = combine_vars(all_vars, self._vars_cache.get(host.get_name(), dict()))
        all_vars = combine_vars(all_vars, self._nonpersistent_fact_cache.get(host.name, dict()))
    if task:
        if task._role:
            all_vars = combine_vars(all_vars, task._role.get_role_params(task.get_dep_chain()))
        all_vars = combine_vars(all_vars, task.get_include_params())
    all_vars = combine_vars(all_vars, self._extra_vars)
    all_vars = combine_vars(all_vars, magic_variables)
    if task:
        if ('environment' not in all_vars):
            all_vars['environment'] = task.environment
        else:
            display.warning("The variable 'environment' appears to be used already, which is also used internally for environment variables set on the task/block/play. You should use a different variable name to avoid conflicts with this internal variable")
    if (task and (task.delegate_to is not None) and include_delegate_to):
        all_vars['ansible_delegated_vars'] = self._get_delegated_vars(loader, play, task, all_vars)
    if (task or play):
        all_vars['vars'] = all_vars.copy()
    display.debug('done with get_vars()')
    return all_vars