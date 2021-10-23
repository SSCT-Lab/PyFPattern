def encode_address_from_string(self, record):
    if self._network_pattern.match(record):
        return record
    elif self._host_pattern.match(record):
        return record
    elif (self._rd_net_pattern.match(record) or self._rd_host_pattern.match(record)):
        return record
    else:
        parts = record.split(self._separator)
        if (parts[0] == ''):
            return
        if (not is_valid_ip_interface(parts[0])):
            raise F5ModuleError("When specifying an 'address' type, the value to the left of the separator must be an IP.")
        key = ip_interface('{0}'.format(str(parts[0])))
        if (len(parts) == 2):
            if (key.network.prefixlen in [32, 128]):
                return self.encode_host(str(key.ip), parts[1])
            return self.encode_network(str(key.network.network_address), key.network.prefixlen, parts[1])
        elif ((len(parts) == 1) and (parts[0] != '')):
            if (key.network.prefixlen in [32, 128]):
                return self.encode_host(str(key.ip), str(key.ip))
            return self.encode_network(str(key.network.network_address), key.network.prefixlen, str(key.network.network_address))