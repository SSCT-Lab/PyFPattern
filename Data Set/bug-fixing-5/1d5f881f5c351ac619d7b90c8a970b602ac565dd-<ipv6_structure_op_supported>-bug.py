def ipv6_structure_op_supported(self):
    data = self.run('show version', output='json')
    if data:
        unsupported_versions = ['I2', 'F1', 'A8']
        for ver in unsupported_versions:
            if (ver in data.get('kickstart_ver_str')):
                return False
        return True