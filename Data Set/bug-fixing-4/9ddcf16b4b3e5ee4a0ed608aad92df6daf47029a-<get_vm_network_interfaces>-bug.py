def get_vm_network_interfaces(self, vm=None):
    if (vm is None):
        return []
    device_list = []
    for device in vm.config.hardware.device:
        if (isinstance(device, vim.vm.device.VirtualVmxnet3) or isinstance(device, vim.vm.device.VirtualE1000)):
            device_list.append(device)
    return device_list