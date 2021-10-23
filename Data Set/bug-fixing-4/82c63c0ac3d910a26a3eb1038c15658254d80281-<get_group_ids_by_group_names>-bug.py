def get_group_ids_by_group_names(self, group_names):
    group_ids = []
    if self.check_host_group_exist(group_names):
        group_list = self._zapi.hostgroup.get({
            'output': 'extend',
            'filter': {
                'name': group_names,
            },
        })
        for group in group_list:
            group_id = group['groupid']
            group_ids.append({
                'groupid': group_id,
            })
    return group_ids