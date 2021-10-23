def encode_address_from_dict(self, record):
    if is_valid_ip_interface(record['key']):
        key = ip_interface('{0}'.format(str(record['key'])))
    else:
        raise F5ModuleError("When specifying an 'address' type, the value to the left of the separator must be an IP.")
    if (key and ('value' in record)):
        if (key.network.prefixlen in [32, 128]):
            return self.encode_host(str(key.ip), record['value'])
        return self.encode_network(str(key.network.network_address), key.network.prefixlen, record['value'])
    elif key:
        if (key.network.prefixlen in [32, 128]):
            return self.encode_host(str(key.ip), str(key.ip))
        return self.encode_network(str(key.network.network_address), key.network.prefixlen, str(key.network.network_address))