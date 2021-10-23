

def run(self, tmp=None, task_vars=None):
    self._supports_check_mode = False
    result = super(ActionModule, self).run(tmp, task_vars)
    if result.get('skipped', False):
        return result
    new_name = self._task.args.get('name', self._task.args.get('hostname', None))
    display.vv(("creating host via 'add_host': hostname=%s" % new_name))
    try:
        (name, port) = parse_address(new_name, allow_ranges=False)
    except:
        name = new_name
        port = None
    if port:
        self._task.args['ansible_ssh_port'] = port
    groups = self._task.args.get('groupname', self._task.args.get('groups', self._task.args.get('group', '')))
    new_groups = []
    if groups:
        if isinstance(groups, list):
            group_list = groups
        elif isinstance(groups, string_types):
            group_list = groups.split(',')
        else:
            raise AnsibleError('Groups must be specfied as a list.', obj=self._task)
        for group_name in group_list:
            if (group_name not in new_groups):
                new_groups.append(group_name.strip())
    host_vars = dict()
    special_args = frozenset(('name', 'hostname', 'groupname', 'groups'))
    for k in self._task.args.keys():
        if (k not in special_args):
            host_vars[k] = self._task.args[k]
    result['changed'] = True
    result['add_host'] = dict(host_name=name, groups=new_groups, host_vars=host_vars)
    return result
