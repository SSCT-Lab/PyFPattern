def apply(self):
    '\n        Run Module based on play book\n        '
    changed = False
    results = netapp_utils.get_cserver(self.server)
    cserver = netapp_utils.setup_ontap_zapi(module=self.module, vserver=results)
    netapp_utils.ems_log_event('na_ontap_service_processor_network', cserver)
    spn_details = self.get_service_processor_network()
    spn_exists = False
    if spn_details:
        spn_exists = True
        if (self.state == 'present'):
            if (((self.dhcp is not None) and (self.dhcp != spn_details['dhcp_value'])) or ((self.gateway_ip_address is not None) and (self.gateway_ip_address != spn_details['gateway_ip_address_value'])) or ((self.ip_address is not None) and (self.ip_address != spn_details['ip_address_value'])) or ((self.netmask is not None) and (self.netmask != spn_details['netmask_value'])) or ((self.prefix_length is not None) and (str(self.prefix_length) != spn_details['prefix_length_value'])) or ((self.is_enabled is not None) and (str(self.is_enabled).lower() != spn_details['is_enabled_value']))):
                changed = True
    else:
        self.module.fail_json(msg=('Error No Service Processor for node: %s' % self.node))
    if changed:
        if self.module.check_mode:
            pass
        elif (self.state == 'present'):
            if spn_exists:
                self.modify_service_processor_network()
    self.module.exit_json(changed=changed)