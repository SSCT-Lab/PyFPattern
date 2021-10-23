def get_firewall_rule(self):
    if (not self.firewall_rule):
        cidr = self.module.params.get('cidr')
        protocol = self.module.params.get('protocol')
        start_port = self.module.params.get('start_port')
        end_port = self.get_or_fallback('end_port', 'start_port')
        icmp_code = self.module.params.get('icmp_code')
        icmp_type = self.module.params.get('icmp_type')
        fw_type = self.module.params.get('type')
        if ((protocol in ['tcp', 'udp']) and (not (start_port and end_port))):
            self.module.fail_json(msg=("missing required argument for protocol '%s': start_port or end_port" % protocol))
        if ((protocol == 'icmp') and (not icmp_type)):
            self.module.fail_json(msg="missing required argument for protocol 'icmp': icmp_type")
        if ((protocol == 'all') and (fw_type != 'egress')):
            self.module.fail_json(msg="protocol 'all' could only be used for type 'egress'")
        args = {
            
        }
        args['account'] = self.get_account('name')
        args['domainid'] = self.get_domain('id')
        args['projectid'] = self.get_project('id')
        if (fw_type == 'egress'):
            args['networkid'] = self.get_network(key='id')
            if (not args['networkid']):
                self.module.fail_json(msg='missing required argument for type egress: network')
            firewall_rules = self.cs.listEgressFirewallRules(**args)
        else:
            args['ipaddressid'] = self.get_ip_address('id')
            if (not args['ipaddressid']):
                self.module.fail_json(msg='missing required argument for type ingress: ip_address')
            firewall_rules = self.cs.listFirewallRules(**args)
        if (firewall_rules and ('firewallrule' in firewall_rules)):
            for rule in firewall_rules['firewallrule']:
                type_match = self._type_cidr_match(rule, cidr)
                protocol_match = (self._tcp_udp_match(rule, protocol, start_port, end_port) or self._icmp_match(rule, protocol, icmp_code, icmp_type) or self._egress_all_match(rule, protocol, fw_type))
                if (type_match and protocol_match):
                    self.firewall_rule = rule
                    break
    return self.firewall_rule