

def _load_machines(self, machines):
    for machine in machines:
        id_dict = azure_id_to_dict(machine.id)
        resource_group = id_dict['resourceGroups'].lower()
        if self.group_by_security_group:
            self._get_security_groups(resource_group)
        host_vars = dict(ansible_host=None, private_ip=None, private_ip_alloc_method=None, public_ip=None, public_ip_name=None, public_ip_id=None, public_ip_alloc_method=None, fqdn=None, location=machine.location, name=machine.name, type=machine.type, id=machine.id, tags=machine.tags, network_interface_id=None, network_interface=None, resource_group=resource_group, mac_address=None, plan=(machine.plan.name if machine.plan else None), virtual_machine_size=machine.hardware_profile.vm_size, computer_name=(machine.os_profile.computer_name if machine.os_profile else None), provisioning_state=machine.provisioning_state)
        host_vars['os_disk'] = dict(name=machine.storage_profile.os_disk.name, operating_system_type=machine.storage_profile.os_disk.os_type.value)
        if self.include_powerstate:
            host_vars['powerstate'] = self._get_powerstate(resource_group, machine.name)
        if machine.storage_profile.image_reference:
            host_vars['image'] = dict(offer=machine.storage_profile.image_reference.offer, publisher=machine.storage_profile.image_reference.publisher, sku=machine.storage_profile.image_reference.sku, version=machine.storage_profile.image_reference.version)
        if ((machine.os_profile is not None) and (machine.os_profile.windows_configuration is not None)):
            host_vars['ansible_connection'] = 'winrm'
            host_vars['windows_auto_updates_enabled'] = machine.os_profile.windows_configuration.enable_automatic_updates
            host_vars['windows_timezone'] = machine.os_profile.windows_configuration.time_zone
            host_vars['windows_rm'] = None
            if (machine.os_profile.windows_configuration.win_rm is not None):
                host_vars['windows_rm'] = dict(listeners=None)
                if (machine.os_profile.windows_configuration.win_rm.listeners is not None):
                    host_vars['windows_rm']['listeners'] = []
                    for listener in machine.os_profile.windows_configuration.win_rm.listeners:
                        host_vars['windows_rm']['listeners'].append(dict(protocol=listener.protocol, certificate_url=listener.certificate_url))
        for interface in machine.network_profile.network_interfaces:
            interface_reference = self._parse_ref_id(interface.id)
            network_interface = self._network_client.network_interfaces.get(interface_reference['resourceGroups'], interface_reference['networkInterfaces'])
            if network_interface.primary:
                if (self.group_by_security_group and self._security_groups[resource_group].get(network_interface.id, None)):
                    host_vars['security_group'] = self._security_groups[resource_group][network_interface.id]['name']
                    host_vars['security_group_id'] = self._security_groups[resource_group][network_interface.id]['id']
                host_vars['network_interface'] = network_interface.name
                host_vars['network_interface_id'] = network_interface.id
                host_vars['mac_address'] = network_interface.mac_address
                for ip_config in network_interface.ip_configurations:
                    host_vars['private_ip'] = ip_config.private_ip_address
                    host_vars['private_ip_alloc_method'] = ip_config.private_ip_allocation_method
                    if ip_config.public_ip_address:
                        public_ip_reference = self._parse_ref_id(ip_config.public_ip_address.id)
                        public_ip_address = self._network_client.public_ip_addresses.get(public_ip_reference['resourceGroups'], public_ip_reference['publicIPAddresses'])
                        host_vars['ansible_host'] = public_ip_address.ip_address
                        host_vars['public_ip'] = public_ip_address.ip_address
                        host_vars['public_ip_name'] = public_ip_address.name
                        host_vars['public_ip_alloc_method'] = public_ip_address.public_ip_allocation_method
                        host_vars['public_ip_id'] = public_ip_address.id
                        if public_ip_address.dns_settings:
                            host_vars['fqdn'] = public_ip_address.dns_settings.fqdn
        self._add_host(host_vars)
