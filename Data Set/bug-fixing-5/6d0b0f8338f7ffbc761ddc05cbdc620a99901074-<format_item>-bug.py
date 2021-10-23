def format_item(self, item):
    d = item.as_dict()
    containers = d['containers']
    ports = d['ip_address']['ports']
    resource_group = d['id'].split('resourceGroups/')[1].split('/')[0]
    for port_index in range(len(ports)):
        ports[port_index] = ports[port_index]['port']
    for container_index in range(len(containers)):
        old_container = containers[container_index]
        new_container = {
            'name': old_container['name'],
            'image': old_container['image'],
            'memory': old_container['resources']['requests']['memory_in_gb'],
            'cpu': old_container['resources']['requests']['cpu'],
            'ports': [],
        }
        for port_index in range(len(old_container['ports'])):
            new_container['ports'].append(old_container['ports'][port_index]['port'])
        containers[container_index] = new_container
    d = {
        'id': d['id'],
        'resource_group': resource_group,
        'name': d['name'],
        'os_type': d['os_type'],
        'ip_address': ('public' if (d['ip_address']['type'] == 'Public') else 'none'),
        'ports': ports,
        'location': d['location'],
        'containers': containers,
    }
    return d