def get_vpc(self):
    if self.vpc:
        return self.vpc
    args = {
        'account': self.get_account(key='name'),
        'domainid': self.get_domain(key='id'),
        'projectid': self.get_project(key='id'),
        'zoneid': self.get_zone(key='id'),
    }
    vpcs = self.cs.listVPCs(**args)
    if vpcs:
        vpc_name = self.module.params.get('name')
        for v in vpcs['vpc']:
            if (vpc_name.lower() in [v['name'].lower(), v['id']]):
                self.vpc = v
                break
    return self.vpc