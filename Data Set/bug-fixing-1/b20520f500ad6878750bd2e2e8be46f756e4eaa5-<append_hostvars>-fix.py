

def append_hostvars(hostvars, groups, key, server, namegroup=False):
    hostvars[key] = dict(ansible_ssh_host=server['interface_ip'], ansible_host=server['interface_ip'], openstack=server)
    for group in get_groups_from_server(server, namegroup=namegroup):
        groups[group].append(key)
