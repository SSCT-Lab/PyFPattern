def get_vmkernel_by_ip(self, ip_address):
    '\n        Check if vmkernel available or not\n        Args:\n            ip_address: IP address of vmkernel device\n\n        Returns: vmkernel managed object if vmkernel found, false if not\n\n        '
    vnics = [vnic for vnic in self.esxi_host_obj.config.network.vnic if (vnic.spec.ip.ipAddress == ip_address)]
    if vnics:
        return vnics[0]
    return None