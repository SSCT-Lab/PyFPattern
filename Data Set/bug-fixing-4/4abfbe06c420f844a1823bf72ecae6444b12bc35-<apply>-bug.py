def apply(self):
    '\n        Run Module based on play book\n        '
    changed = False
    broadcast_domain_details = self.get_broadcast_domain_ports()
    broadcast_domain_exists = False
    results = netapp_utils.get_cserver(self.server)
    cserver = netapp_utils.setup_na_ontap_zapi(module=self.module, vserver=results)
    netapp_utils.ems_log_event('na_ontap_broadcast_domain_ports', cserver)
    if broadcast_domain_details:
        broadcast_domain_exists = True
        if (self.state == 'absent'):
            changed = True
        elif (self.state == 'present'):
            changed = True
    else:
        pass
    if changed:
        if self.module.check_mode:
            pass
        elif broadcast_domain_exists:
            if (self.state == 'present'):
                changed = self.create_broadcast_domain_ports()
            elif (self.state == 'absent'):
                changed = self.delete_broadcast_domain_ports()
    self.module.exit_json(changed=changed)