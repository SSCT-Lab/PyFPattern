def populate_interfaces(self, interfaces, os_version):
    interfaces_dict = dict()
    for if_data in interfaces:
        if_dict = dict()
        if (os_version >= BaseOnyxModule.ONYX_API_VERSION):
            for (if_name, interface_data) in iteritems(if_data):
                interface_data = interface_data[0]
                if_dict = self.extractIfData(interface_data)
                if_name = if_dict['Interface Name'] = if_name
        else:
            if_dict = self.extractIfData(if_data)
            if_name = if_dict['Interface Name'] = if_data['header']
        interfaces_dict[if_name] = if_dict
    return interfaces_dict