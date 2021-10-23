def get_resource_limit(self):
    args = {
        
    }
    args['account'] = self.get_account(key='name')
    args['domainid'] = self.get_domain(key='id')
    args['projectid'] = self.get_project(key='id')
    args['resourcetype'] = self.get_resource_type()
    resource_limit = self.cs.listResourceLimits(**args)
    if resource_limit:
        return resource_limit['resourcelimit'][0]
    self.module.fail_json(msg=("Resource limit type '%s' not found." % self.module.params.get('resource_type')))