def ipv6_structure_op_supported(self):
    data = get_capabilities(self.module)
    if data:
        nxos_os_version = data['device_info']['network_os_version']
        unsupported_versions = ['I2', 'F1', 'A8']
        for ver in unsupported_versions:
            if (ver in nxos_os_version):
                return False
        return True