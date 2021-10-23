

def configure_network(self, vm_obj):
    if (len(self.params['networks']) == 0):
        return
    network_devices = list()
    for network in self.params['networks']:
        if (('ip' in network) or ('netmask' in network)):
            if (('ip' not in network) or (not ('netmask' in network))):
                self.module.fail_json(msg="Both 'ip' and 'netmask' are required together.")
        if ('name' in network):
            if (get_obj(self.content, [vim.Network], network['name']) is None):
                self.module.fail_json(msg=("Network '%(name)s' does not exists" % network))
        elif ('vlan' in network):
            dvps = get_all_objs(self.content, [vim.dvs.DistributedVirtualPortgroup])
            for dvp in dvps:
                if (hasattr(dvp.config.defaultPortConfig, 'vlan') and (dvp.config.defaultPortConfig.vlan.vlanId == network['vlan'])):
                    network['name'] = dvp.config.name
                    break
                if (dvp.config.name == network['vlan']):
                    network['name'] = dvp.config.name
                    break
            else:
                self.module.fail_json(msg=("VLAN '%(vlan)s' does not exist" % network))
        else:
            self.module.fail_json(msg='You need to define a network name or a vlan')
        network_devices.append(network)
    current_net_devices = self.get_vm_network_interfaces(vm=vm_obj)
    if (len(network_devices) < len(current_net_devices)):
        self.module.fail_json(msg=('given network device list is lesser than current VM device list (%d < %d). Removing interfaces is not allowed' % (len(network_devices), len(current_net_devices))))
    for key in range(0, len(network_devices)):
        device_type = network_devices[key].get('device_type', 'vmxnet3')
        nic = self.device_helper.create_nic(device_type, ('Network Adapter %s' % (key + 1)), network_devices[key])
        nic_change_detected = False
        if ((key < len(current_net_devices)) and (vm_obj or self.should_deploy_from_template())):
            nic.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
            if (('mac' in network_devices[key]) and (nic.device.macAddress != current_net_devices[key].macAddress)):
                self.module.fail_json(msg=('Changing MAC address has not effect when interface is already present. The failing new MAC address is %s' % nic.device.macAddress))
            nic.device = current_net_devices[key]
            nic.device.deviceInfo = vim.Description()
        else:
            nic.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
            nic_change_detected = True
        if hasattr(self.cache.get_network(network_devices[key]['name']), 'portKeys'):
            pg_obj = get_obj(self.content, [vim.dvs.DistributedVirtualPortgroup], network_devices[key]['name'])
            if (nic.device.backing and ((nic.device.backing.port.portgroupKey != pg_obj.key) or (nic.device.backing.port.switchUuid != pg_obj.config.distributedVirtualSwitch.uuid))):
                nic_change_detected = True
            dvs_port_connection = vim.dvs.PortConnection()
            dvs_port_connection.portgroupKey = pg_obj.key
            dvs_port_connection.switchUuid = pg_obj.config.distributedVirtualSwitch.uuid
            nic.device.backing = vim.vm.device.VirtualEthernetCard.DistributedVirtualPortBackingInfo()
            nic.device.backing.port = dvs_port_connection
            nic_change_detected = True
        else:
            if (not isinstance(nic.device.backing, vim.vm.device.VirtualEthernetCard.NetworkBackingInfo)):
                nic.device.backing = vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
                nic_change_detected = True
            net_obj = self.cache.get_network(network_devices[key]['name'])
            if (nic.device.backing.network != net_obj):
                nic.device.backing.network = net_obj
                nic_change_detected = True
            if (nic.device.backing.deviceName != network_devices[key]['name']):
                nic.device.backing.deviceName = network_devices[key]['name']
                nic_change_detected = True
        if nic_change_detected:
            self.configspec.deviceChange.append(nic)
            self.change_detected = True
