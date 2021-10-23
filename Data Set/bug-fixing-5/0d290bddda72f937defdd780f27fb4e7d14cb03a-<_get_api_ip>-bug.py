def _get_api_ip(self):
    'Return the IP of the DHCP server.'
    if (not self.api_ip):
        dhcp_lease_file = self._get_dhcp_lease_file()
        for line in open(dhcp_lease_file):
            if ('dhcp-server-identifier' in line):
                line = line.translate(None, ';')
                self.api_ip = line.split()[2]
                break
        if (not self.api_ip):
            module.fail_json(msg='No dhcp-server-identifier found in leases file.')
    return self.api_ip