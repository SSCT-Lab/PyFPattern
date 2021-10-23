def get_router(self):
    if (not self.router):
        router = self.module.params.get('name')
        args = {
            'projectid': self.get_project(key='id'),
            'account': self.get_account(key='name'),
            'domainid': self.get_domain(key='id'),
            'listall': True,
        }
        if self.module.params.get('zone'):
            args['zoneid'] = self.get_zone(key='id')
        routers = self.cs.listRouters(**args)
        if routers:
            for r in routers['router']:
                if (router.lower() in [r['name'].lower(), r['id']]):
                    self.router = r
                    break
    return self.router