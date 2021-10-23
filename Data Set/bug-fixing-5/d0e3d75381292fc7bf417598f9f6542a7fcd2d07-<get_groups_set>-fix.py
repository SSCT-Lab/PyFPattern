def get_groups_set(self, remove_existing=True):
    if (self.groups is None):
        return None
    info = self.user_info()
    groups = set([x.strip() for x in self.groups.split(',') if x])
    for g in set(groups):
        if (not self.group_exists(g)):
            self.module.fail_json(msg=('Group %s does not exist' % g))
        if (info and remove_existing and (self.group_info(g)[2] == info[3])):
            groups.remove(g)
    return groups