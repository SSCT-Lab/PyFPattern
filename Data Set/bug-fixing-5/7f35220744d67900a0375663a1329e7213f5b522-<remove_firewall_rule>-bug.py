def remove_firewall_rule(self):
    firewall_rule = self.get_firewall_rule()
    if firewall_rule:
        self.result['changed'] = True
        args = {
            
        }
        args['id'] = firewall_rule['id']
        fw_type = self.module.params.get('type')
        if (not self.module.check_mode):
            if (fw_type == 'egress'):
                res = self.cs.deleteEgressFirewallRule(**args)
            else:
                res = self.cs.deleteFirewallRule(**args)
            if ('errortext' in res):
                self.module.fail_json(msg=("Failed: '%s'" % res['errortext']))
            poll_async = self.module.params.get('poll_async')
            if poll_async:
                res = self.poll_job(res, 'firewallrule')
    return firewall_rule