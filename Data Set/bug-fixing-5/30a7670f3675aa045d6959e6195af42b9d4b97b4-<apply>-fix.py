def apply(self):
    self.asup_log_for_cserver('na_ontap_vscan_scanner_pool')
    changed = False
    scanner_pool_obj = self.get_scanner_pool()
    if (self.state == 'present'):
        if (not scanner_pool_obj):
            self.create_scanner_pool()
            if self.scanner_policy:
                self.apply_policy()
            changed = True
        if scanner_pool_obj:
            if self.scanner_policy:
                if (scanner_pool_obj.get_child_content('scanner-policy') != self.scanner_policy):
                    self.apply_policy()
                    changed = True
    if (self.state == 'absent'):
        if scanner_pool_obj:
            self.delete_scanner_pool()
            changed = True
    self.module.exit_json(changed=changed)