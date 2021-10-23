def set_playbook_basedir(self, dir_name):
    '\n        sets the base directory of the playbook so inventory can use it as a\n        basedir for host_ and group_vars, and other things.\n        '
    if (dir_name != self._playbook_basedir):
        self._playbook_basedir = dir_name
        found_group_vars = self._find_group_vars_files(self._playbook_basedir)
        if found_group_vars:
            self._group_vars_files = self._group_vars_files.union(found_group_vars)
            for group in self.groups.values():
                group.vars = combine_vars(group.vars, self.get_group_vars(group))
        found_host_vars = self._find_host_vars_files(self._playbook_basedir)
        if found_host_vars:
            self._host_vars_files = self._find_host_vars_files(self._playbook_basedir)
            for host in self.get_hosts():
                host.vars = combine_vars(host.vars, self.get_host_vars(host))
        self._vars_per_host = {
            
        }
        self._vars_per_group = {
            
        }