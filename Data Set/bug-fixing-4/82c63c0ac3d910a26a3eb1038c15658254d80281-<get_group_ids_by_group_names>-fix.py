def get_group_ids_by_group_names(self, group_names):
    if self.check_host_group_exist(group_names):
        return self._zapi.hostgroup.get({
            'output': 'groupid',
            'filter': {
                'name': group_names,
            },
        })