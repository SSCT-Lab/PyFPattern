def apply(self):
    '\n        Run Module based on play book\n        '
    changed = False
    broadcast_domain_details = self.get_broadcast_domain_ports()
    results = netapp_utils.get_cserver(self.server)
    cserver = netapp_utils.setup_na_ontap_zapi(module=self.module, vserver=results)
    netapp_utils.ems_log_event('na_ontap_broadcast_domain_ports', cserver)
    if (broadcast_domain_details is None):
        self.module.fail_json(msg=('Error broadcast domain not found: %s' % self.broadcast_domain))
    if self.module.check_mode:
        pass
    elif (self.state == 'present'):
        ports_to_add = [port for port in self.ports if (port not in broadcast_domain_details['ports'])]
        if (len(ports_to_add) > 0):
            changed = self.create_broadcast_domain_ports(ports_to_add)
    elif (self.state == 'absent'):
        ports_to_delete = [port for port in self.ports if (port in broadcast_domain_details['ports'])]
        if (len(ports_to_delete) > 0):
            changed = self.delete_broadcast_domain_ports(ports_to_delete)
    self.module.exit_json(changed=changed)