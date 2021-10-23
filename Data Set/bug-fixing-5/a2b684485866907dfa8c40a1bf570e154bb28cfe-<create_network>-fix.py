def create_network(self, network):
    self.result['changed'] = True
    args = self._get_args()
    args.update({
        'acltype': self.module.params.get('acl_type'),
        'zoneid': self.get_zone(key='id'),
        'projectid': self.get_project(key='id'),
        'account': self.get_account(key='name'),
        'domainid': self.get_domain(key='id'),
        'startip': self.module.params.get('start_ip'),
        'endip': self.get_or_fallback('end_ip', 'start_ip'),
        'netmask': self.module.params.get('netmask'),
        'gateway': self.module.params.get('gateway'),
        'startipv6': self.module.params.get('start_ipv6'),
        'endipv6': self.get_or_fallback('end_ipv6', 'start_ipv6'),
        'ip6cidr': self.module.params.get('cidr_ipv6'),
        'ip6gateway': self.module.params.get('gateway_ipv6'),
        'vlan': self.module.params.get('vlan'),
        'isolatedpvlan': self.module.params.get('isolated_pvlan'),
        'subdomainaccess': self.module.params.get('subdomain_access'),
        'vpcid': self.get_vpc(key='id'),
    })
    if (not self.module.check_mode):
        res = self.cs.createNetwork(**args)
        if ('errortext' in res):
            self.module.fail_json(msg=("Failed: '%s'" % res['errortext']))
        network = res['network']
    return network