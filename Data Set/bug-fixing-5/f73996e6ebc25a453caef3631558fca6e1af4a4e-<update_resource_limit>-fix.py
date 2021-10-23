def update_resource_limit(self):
    resource_limit = self.get_resource_limit()
    args = {
        'account': self.get_account(key='name'),
        'domainid': self.get_domain(key='id'),
        'projectid': self.get_project(key='id'),
        'resourcetype': self.get_resource_type(),
        'max': self.module.params.get('limit', (- 1)),
    }
    if self.has_changed(args, resource_limit):
        self.result['changed'] = True
        if (not self.module.check_mode):
            res = self.query_api('updateResourceLimit', **args)
            resource_limit = res['resourcelimit']
    return resource_limit