def apply(self):
    results = netapp_utils.get_cserver(self.server)
    cserver = netapp_utils.setup_na_ontap_zapi(module=self.module, vserver=results)
    netapp_utils.ems_log_event('na_ontap_firewall_policy', cserver)
    changed = False
    if (self.parameters['state'] == 'present'):
        policy = self.get_firewall_policy()
        if (not policy):
            self.create_firewall_policy()
            if (not self.check_config(self.get_firewall_config())):
                self.modify_firewall_config()
            changed = True
        else:
            if self.check_policy(policy):
                self.modify_firewall_policy()
                changed = True
            if (not self.check_config(self.get_firewall_config())):
                self.modify_firewall_config()
                changed = True
    elif self.get_firewall_policy():
        self.destroy_firewall_policy()
        if (not self.check_config(self.get_firewall_config())):
            self.modify_firewall_config()
        changed = True
    elif (not self.check_config(self.get_firewall_config())):
        self.modify_firewall_config()
        changed = True
    self.module.exit_json(changed=changed)