def generate_network_dict(array):
    net_facts = {
        
    }
    ports = array.list_network_interfaces()
    for port in range(0, len(ports)):
        int_name = ports[port]['name']
        net_facts[int_name] = {
            'hwaddr': ports[port]['hwaddr'],
            'mtu': ports[port]['mtu'],
            'enabled': ports[port]['enabled'],
            'speed': ports[port]['speed'],
            'address': ports[port]['address'],
            'slaves': ports[port]['slaves'],
            'services': ports[port]['services'],
            'gateway': ports[port]['gateway'],
            'netmask': ports[port]['netmask'],
        }
        if ports[port]['subnet']:
            subnets = array.get_subnet(ports[port]['subnet'])
            if subnets['enabled']:
                net_facts[int_name]['subnet'] = {
                    'name': subnets['name'],
                    'prefix': subnets['prefix'],
                    'vlan': subnets['vlan'],
                }
    return net_facts