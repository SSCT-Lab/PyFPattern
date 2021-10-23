def create_network(self, network):
    self.result['changed'] = True
    args = self._get_args()
    args['acltype'] = self.module.params.get('acl_type')
    args['zoneid'] = self.get_zone(key='id')
    args['projectid'] = self.get_project(key='id')
    args['account'] = self.get_account(key='name')
    args['domainid'] = self.get_domain(key='id')
    args['startip'] = self.module.params.get('start_ip')
    args['endip'] = self.get_or_fallback('end_ip', 'start_ip')
    args['netmask'] = self.module.params.get('netmask')
    args['gateway'] = self.module.params.get('gateway')
    args['startipv6'] = self.module.params.get('start_ipv6')
    args['endipv6'] = self.get_or_fallback('end_ipv6', 'start_ipv6')
    args['ip6cidr'] = self.module.params.get('cidr_ipv6')
    args['ip6gateway'] = self.module.params.get('gateway_ipv6')
    args['vlan'] = self.module.params.get('vlan')
    args['isolatedpvlan'] = self.module.params.get('isolated_pvlan')
    args['subdomainaccess'] = self.module.params.get('subdomain_access')
    args['vpcid'] = self.get_vpc(key='id')
    if (not self.module.check_mode):
        res = self.cs.createNetwork(**args)
        if ('errortext' in res):
            self.module.fail_json(msg=("Failed: '%s'" % res['errortext']))
        network = res['network']
    return network