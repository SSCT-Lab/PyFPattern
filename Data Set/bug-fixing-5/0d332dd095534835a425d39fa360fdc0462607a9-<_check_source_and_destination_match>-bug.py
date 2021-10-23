def _check_source_and_destination_match(self):
    'Verify that destination and source are of the same IP version\n\n        BIG-IP does not allow for mixing of the IP versions for destination and\n        source addresses. For example, a destination IPv6 address cannot be\n        associated with a source IPv4 address.\n\n        This method checks that you specified the same IP version for these\n        parameters\n\n        Raises:\n            F5ModuleError: Raised when the IP versions of source and destination differ.\n        '
    if (self.want.source and self.want.destination):
        want = netaddr.IPNetwork(self.want.source)
        have = netaddr.IPNetwork(self.want.destination_tuple.ip)
        if (want.version != have.version):
            raise F5ModuleError('The source and destination addresses for the virtual server must be be the same type (IPv4 or IPv6).')