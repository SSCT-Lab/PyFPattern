def get_resource_limit(self):
    args = {
        'account': self.get_account(key='name'),
        'domainid': self.get_domain(key='id'),
        'projectid': self.get_project(key='id'),
        'resourcetype': self.get_resource_type(),
    }
    resource_limit = self.query_api('listResourceLimits', **args)
    if resource_limit:
        if ('limit' in resource_limit['resourcelimit'][0]):
            resource_limit['resourcelimit'][0]['limit'] = int(resource_limit['resourcelimit'][0])
        return resource_limit['resourcelimit'][0]
    self.module.fail_json(msg=("Resource limit type '%s' not found." % self.module.params.get('resource_type')))