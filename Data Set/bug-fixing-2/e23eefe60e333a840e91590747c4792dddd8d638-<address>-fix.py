

@property
def address(self):
    if (self._values['address'] is None):
        return None
    elif (self._values['address'] == 'any6'):
        return 'any6'
    try:
        addr = netaddr.IPAddress(self._values['address'].split('%')[0])
        return str(addr)
    except netaddr.AddrFormatError:
        raise F5ModuleError("The specified 'address' value is not a valid IP address.")
