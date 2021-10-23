def get_vpc_offering(self):
    if self.vpc_offering:
        return self.vpc_offering
    args = {
        'name': self.module.params.get('name'),
    }
    vo = self.query_api('listVPCOfferings', **args)
    if vo:
        self.vpc_offering = vo['vpcoffering'][0]
    return self.vpc_offering