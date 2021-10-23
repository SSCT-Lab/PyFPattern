def populate_interfaces(self, interfaces):
    facts = dict()
    for (key, value) in iteritems(interfaces):
        intf = dict()
        intf['description'] = self.parse_description(value)
        intf['macaddress'] = self.parse_macaddress(value)
        intf['mtu'] = self.parse_mtu(value)
        intf['bandwidth'] = self.parse_bandwidth(value)
        intf['mediatype'] = self.parse_mediatype(value)
        intf['duplex'] = self.parse_duplex(value)
        intf['lineprotocol'] = self.parse_lineprotocol(value)
        intf['operstatus'] = self.parse_operstatus(value)
        intf['type'] = self.parse_type(value)
        facts[key] = intf
    return facts