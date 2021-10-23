def decode_address_from_string(self, record):
    matches = self._network_pattern.match(record)
    if matches:
        key = '{0}/{1}'.format(matches.group('addr'), matches.group('prefix'))
        addr = ip_network(key)
        value = record.split(self._separator)[1].strip().strip('"')
        result = dict(name=str(addr), data=value)
        return result
    matches = self._host_pattern.match(record)
    if matches:
        key = matches.group('addr')
        addr = ip_interface('{0}'.format(str(key)))
        value = record.split(self._separator)[1].strip().strip('"')
        result = dict(name=str(addr), data=value)
        return result
    raise F5ModuleError('The value "{0}" is not an address'.format(record))