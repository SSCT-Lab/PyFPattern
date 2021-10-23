def _get_dhcp_lease_file(self):
    'Return the path of the lease file.'
    default_iface = self.facts['default_ipv4']['interface']
    dhcp_lease_file_locations = [('/var/lib/dhcp/dhclient.%s.leases' % default_iface), ('/var/lib/dhclient/dhclient-%s.leases' % default_iface), ('/var/lib/dhclient/dhclient--%s.lease' % default_iface), ('/var/db/dhclient.leases.%s' % default_iface)]
    for file_path in dhcp_lease_file_locations:
        if os.path.exists(file_path):
            return file_path
    module.fail_json(msg='Could not find dhclient leases file.')