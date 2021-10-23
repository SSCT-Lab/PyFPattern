def apply(self):
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