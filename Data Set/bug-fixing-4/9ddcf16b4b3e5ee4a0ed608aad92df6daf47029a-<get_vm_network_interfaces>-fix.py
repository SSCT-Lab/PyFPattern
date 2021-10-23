def get_vm_network_interfaces(self, vm=None):
    if (vm is None):
        return []
    device_list = []
    for device in vm.config.hardware.device:
        if (isinstance(device, vim.vm.device.VirtualPCNet32) or isinstance(device, vim.vm.device.VirtualVmxnet2) or isinstance(device, vim.vm.device.VirtualVmxnet3) or isinstance(device, vim.vm.device.VirtualE1000) or isinstance(device, vim.vm.device.VirtualE1000e) or isinstance(device, vim.vm.device.VirtualSriovEthernetCard)):
            device_list.append(device)
    return device_list