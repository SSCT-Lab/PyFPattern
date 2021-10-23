def create_firewall_rule(self):
    firewall_rule = self.get_firewall_rule()
    if (not firewall_rule):
        self.result['changed'] = True
        args = {
            'cidrlist': self.module.params.get('cidr'),
            'protocol': self.module.params.get('protocol'),
            'startport': self.module.params.get('start_port'),
            'endport': self.get_or_fallback('end_port', 'start_port'),
            'icmptype': self.module.params.get('icmp_type'),
            'icmpcode': self.module.params.get('icmp_code'),
        }
        fw_type = self.module.params.get('type')
        if (not self.module.check_mode):
            if (fw_type == 'egress'):
                args['networkid'] = self.get_network(key='id')
                res = self.cs.createEgressFirewallRule(**args)
            else:
                args['ipaddressid'] = self.get_ip_address('id')
                res = self.cs.createFirewallRule(**args)
            if ('errortext' in res):
                self.module.fail_json(msg=("Failed: '%s'" % res['errortext']))
            poll_async = self.module.params.get('poll_async')
            if poll_async:
                firewall_rule = self.poll_job(res, 'firewallrule')
    return firewall_rule