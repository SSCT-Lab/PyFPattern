

def sanitize_network_params(self):
    '\n        Function to sanitize user provided network provided params\n\n        Returns: A sanitized list of network params, else fails\n\n        '
    network_devices = list()
    for network in self.params['networks']:
        if (('name' not in network) and ('vlan' not in network)):
            self.module.fail_json(msg='Please specify at least a network name or a VLAN name under VM network list.')
        if (('name' in network) and (find_obj(self.content, [vim.Network], network['name']) is None)):
            self.module.fail_json(msg=("Network '%(name)s' does not exist." % network))
        elif ('vlan' in network):
            dvps = self.cache.get_all_objs(self.content, [vim.dvs.DistributedVirtualPortgroup])
            for dvp in dvps:
                if (hasattr(dvp.config.defaultPortConfig, 'vlan') and (dvp.config.defaultPortConfig.vlan.vlanId == network['vlan'])):
                    network['name'] = dvp.config.name
                    break
                if (dvp.config.name == network['vlan']):
                    network['name'] = dvp.config.name
                    break
            else:
                self.module.fail_json(msg=("VLAN '%(vlan)s' does not exist." % network))
        if ('type' in network):
            if (network['type'] not in ['dhcp', 'static']):
                self.module.fail_json(msg=("Network type '%(type)s' is not a valid parameter. Valid parameters are ['dhcp', 'static']." % network))
            if ((network['type'] != 'static') and (('ip' in network) or ('netmask' in network))):
                self.module.fail_json(msg=('Static IP information provided for network "%(name)s", but "type" is set to "%(type)s".' % network))
        elif (('ip' in network) or ('netmask' in network)):
            network['type'] = 'static'
        else:
            network['type'] = 'dhcp'
        if (network.get('type') == 'static'):
            if (('ip' in network) and ('netmask' not in network)):
                self.module.fail_json(msg="'netmask' is required if 'ip' is specified under VM network list.")
            if (('ip' not in network) and ('netmask' in network)):
                self.module.fail_json(msg="'ip' is required if 'netmask' is specified under VM network list.")
        validate_device_types = ['pcnet32', 'vmxnet2', 'vmxnet3', 'e1000', 'e1000e', 'sriov']
        if (('device_type' in network) and (network['device_type'] not in validate_device_types)):
            self.module.fail_json(msg=("Device type specified '%s' is not valid. Please specify correct device type from ['%s']." % (network['device_type'], "', '".join(validate_device_types))))
        if (('mac' in network) and (not PyVmomiDeviceHelper.is_valid_mac_addr(network['mac']))):
            self.module.fail_json(msg=("Device MAC address '%s' is invalid. Please provide correct MAC address." % network['mac']))
        network_devices.append(network)
    return network_devices
