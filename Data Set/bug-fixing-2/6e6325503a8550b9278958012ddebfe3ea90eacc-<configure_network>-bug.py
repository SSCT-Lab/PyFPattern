

def configure_network(self, vm_obj):
    if (len(self.params['networks']) == 0):
        return
    network_devices = self.sanitize_network_params()
    current_net_devices = self.get_vm_network_interfaces(vm=vm_obj)
    if (len(network_devices) < len(current_net_devices)):
        self.module.fail_json(msg=('Given network device list is lesser than current VM device list (%d < %d). Removing interfaces is not allowed' % (len(network_devices), len(current_net_devices))))
    for key in range(0, len(network_devices)):
        nic_change_detected = False
        network_name = network_devices[key]['name']
        if ((key < len(current_net_devices)) and (vm_obj or self.params['template'])):
            nic = vim.vm.device.VirtualDeviceSpec()
            nic.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
            nic.device = current_net_devices[key]
            if (('wake_on_lan' in network_devices[key]) and (nic.device.wakeOnLanEnabled != network_devices[key].get('wake_on_lan'))):
                nic.device.wakeOnLanEnabled = network_devices[key].get('wake_on_lan')
                nic_change_detected = True
            if (('start_connected' in network_devices[key]) and (nic.device.connectable.startConnected != network_devices[key].get('start_connected'))):
                nic.device.connectable.startConnected = network_devices[key].get('start_connected')
                nic_change_detected = True
            if (('allow_guest_control' in network_devices[key]) and (nic.device.connectable.allowGuestControl != network_devices[key].get('allow_guest_control'))):
                nic.device.connectable.allowGuestControl = network_devices[key].get('allow_guest_control')
                nic_change_detected = True
            if (nic.device.deviceInfo.summary != network_name):
                nic.device.deviceInfo.summary = network_name
                nic_change_detected = True
            if ('device_type' in network_devices[key]):
                device = self.device_helper.get_device(network_devices[key]['device_type'], network_name)
                if (nic.device != device):
                    self.module.fail_json(msg=('Changing the device type is not possible when interface is already present. The failing device type is %s' % network_devices[key]['device_type']))
            if (('mac' in network_devices[key]) and (nic.device.macAddress != current_net_devices[key].macAddress)):
                self.module.fail_json(msg=('Changing MAC address has not effect when interface is already present. The failing new MAC address is %s' % nic.device.macAddress))
        else:
            device_type = network_devices[key].get('device_type', 'vmxnet3')
            nic = self.device_helper.create_nic(device_type, ('Network Adapter %s' % (key + 1)), network_devices[key])
            nic.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
            nic_change_detected = True
        if hasattr(self.cache.get_network(network_name), 'portKeys'):
            pg_obj = find_obj(self.content, [vim.dvs.DistributedVirtualPortgroup], network_name)
            if (nic.device.backing and ((not hasattr(nic.device.backing, 'port')) or ((nic.device.backing.port.portgroupKey != pg_obj.key) or (nic.device.backing.port.switchUuid != pg_obj.config.distributedVirtualSwitch.uuid)))):
                nic_change_detected = True
            dvs_port_connection = vim.dvs.PortConnection()
            dvs_port_connection.portgroupKey = pg_obj.key
            dvs_port_connection.switchUuid = pg_obj.config.distributedVirtualSwitch.uuid
            nic.device.backing = vim.vm.device.VirtualEthernetCard.DistributedVirtualPortBackingInfo()
            nic.device.backing.port = dvs_port_connection
        elif isinstance(self.cache.get_network(network_name), vim.OpaqueNetwork):
            nic.device.backing = vim.vm.device.VirtualEthernetCard.OpaqueNetworkBackingInfo()
            nic.device.backing.opaqueNetworkType = 'nsx.LogicalSwitch'
            nic.device.backing.opaqueNetworkId = self.cache.get_network(network_name).summary.opaqueNetworkId
            nic.device.deviceInfo.summary = ('nsx.LogicalSwitch: %s' % self.cache.get_network(network_name).summary.opaqueNetworkId)
        else:
            if (not isinstance(nic.device.backing, vim.vm.device.VirtualEthernetCard.NetworkBackingInfo)):
                nic.device.backing = vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
                nic_change_detected = True
            net_obj = self.cache.get_network(network_name)
            if (nic.device.backing.network != net_obj):
                nic.device.backing.network = net_obj
                nic_change_detected = True
            if (nic.device.backing.deviceName != network_name):
                nic.device.backing.deviceName = network_name
                nic_change_detected = True
        if nic_change_detected:
            self.configspec.deviceChange.append(nic)
            self.change_detected = True
