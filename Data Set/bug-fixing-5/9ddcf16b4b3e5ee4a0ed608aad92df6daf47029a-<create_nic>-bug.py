def create_nic(self, device_type, device_label, device_infos):
    nic = vim.vm.device.VirtualDeviceSpec()
    if (device_type == 'vmxnet3'):
        nic.device = vim.vm.device.VirtualVmxnet3()
    elif (device_type == 'e1000'):
        nic.device = vim.vm.device.VirtualE1000()
    else:
        self.module.fail_json(msg=("invalid device_type '%s' for network %s" % (device_type, device_infos['network'])))
    nic.device.wakeOnLanEnabled = True
    nic.device.addressType = 'assigned'
    nic.device.deviceInfo = vim.Description()
    nic.device.deviceInfo.label = device_label
    nic.device.deviceInfo.summary = device_infos['network']
    nic.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
    nic.device.connectable.startConnected = True
    nic.device.connectable.allowGuestControl = True
    nic.device.connectable.connected = True
    if ('mac' in device_infos):
        nic.device.macAddress = device_infos['mac']
    return nic