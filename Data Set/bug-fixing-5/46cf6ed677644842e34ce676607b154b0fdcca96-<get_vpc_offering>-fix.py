def get_vpc_offering(self):
    if self.vpc_offering:
        return self.vpc_offering
    args = {
        'name': self.module.params.get('name'),
    }
    vo = self.query_api('listVPCOfferings', **args)
    if vo:
        for vpc_offer in vo['vpcoffering']:
            if (args['name'] == vpc_offer['name']):
                self.vpc_offering = vpc_offer
    return self.vpc_offering