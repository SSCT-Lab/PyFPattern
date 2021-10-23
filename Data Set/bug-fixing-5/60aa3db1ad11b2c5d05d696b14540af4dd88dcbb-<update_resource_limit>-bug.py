def update_resource_limit(self):
    resource_limit = self.get_resource_limit()
    args = {
        
    }
    args['account'] = self.get_account(key='name')
    args['domainid'] = self.get_domain(key='id')
    args['projectid'] = self.get_project(key='id')
    args['resourcetype'] = self.get_resource_type()
    args['max'] = self.module.params.get('limit', (- 1))
    if self.has_changed(args, resource_limit):
        self.result['changed'] = True
        if (not self.module.check_mode):
            res = self.cs.updateResourceLimit(**args)
            if ('errortext' in res):
                self.module.fail_json(msg=("Failed: '%s'" % res['errortext']))
            resource_limit = res['resourcelimit']
    return resource_limit