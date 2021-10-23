def populate_interfaces(self, interfaces):
    interfaces_dict = dict()
    for if_data in interfaces:
        if_dict = dict()
        if_dict['MAC Address'] = if_data['Mac address']
        if_dict['Actual Speed'] = if_data['Actual speed']
        if_dict['MTU'] = if_data['MTU']
        if_dict['Admin State'] = if_data['Admin state']
        if_dict['Operational State'] = if_data['Operational state']
        if_name = if_dict['Interface Name'] = if_data['header']
        interfaces_dict[if_name] = if_dict
    return interfaces_dict