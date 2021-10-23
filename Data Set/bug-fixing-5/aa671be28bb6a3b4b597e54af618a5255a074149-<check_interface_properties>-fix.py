def check_interface_properties(self, exist_interface_list, interfaces):
    interfaces_port_list = []
    if (interfaces is not None):
        if (len(interfaces) >= 1):
            for interface in interfaces:
                interfaces_port_list.append(str(interface['port']))
    exist_interface_ports = []
    if (len(exist_interface_list) >= 1):
        for exist_interface in exist_interface_list:
            exist_interface_ports.append(str(exist_interface['port']))
    if (set(interfaces_port_list) != set(exist_interface_ports)):
        return True
    for exist_interface in exist_interface_list:
        exit_interface_port = str(exist_interface['port'])
        for interface in interfaces:
            interface_port = str(interface['port'])
            if (interface_port == exit_interface_port):
                for key in interface.keys():
                    if (str(exist_interface[key]) != str(interface[key])):
                        return True
    return False