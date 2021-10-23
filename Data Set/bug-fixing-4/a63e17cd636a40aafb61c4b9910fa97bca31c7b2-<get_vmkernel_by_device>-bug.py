def get_vmkernel_by_device(self, device_name):
    '\n        Check if vmkernel available or not\n        Args:\n            device_name: name of vmkernel device\n\n        Returns: vmkernel managed object if vmkernel found, false if not\n\n        '
    vnics = [vnic for vnic in self.esxi_host_obj.config.network.vnic if (vnic.device == device_name)]
    if vnics:
        return vnics[0]
    return None