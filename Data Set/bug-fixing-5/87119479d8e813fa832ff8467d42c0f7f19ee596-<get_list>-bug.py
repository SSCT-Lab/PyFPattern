def get_list(self, project_id=None, domain_id=None):
    data = {
        'all': {
            'hosts': [],
        },
        '_meta': {
            'hostvars': {
                
            },
        },
    }
    groups = self.cs.listInstanceGroups(projectid=project_id, domainid=domain_id)
    if groups:
        for group in groups['instancegroup']:
            group_name = group['name']
            if (group_name and (not (group_name in data))):
                data[group_name] = {
                    'hosts': [],
                }
    hosts = self.cs.listVirtualMachines(projectid=project_id, domainid=domain_id)
    if (not hosts):
        return data
    for host in hosts['virtualmachine']:
        host_name = host['displayname']
        data['all']['hosts'].append(host_name)
        data['_meta']['hostvars'][host_name] = {
            
        }
        data['_meta']['hostvars'][host_name]['zone'] = host['zonename']
        group_name = host['zonename']
        if (group_name not in data):
            data[group_name] = {
                'hosts': [],
            }
        data[group_name]['hosts'].append(host_name)
        if ('group' in host):
            data['_meta']['hostvars'][host_name]['group'] = host['group']
        data['_meta']['hostvars'][host_name]['state'] = host['state']
        data['_meta']['hostvars'][host_name]['service_offering'] = host['serviceofferingname']
        data['_meta']['hostvars'][host_name]['affinity_group'] = host['affinitygroup']
        data['_meta']['hostvars'][host_name]['security_group'] = host['securitygroup']
        data['_meta']['hostvars'][host_name]['cpu_number'] = host['cpunumber']
        data['_meta']['hostvars'][host_name]['cpu_speed'] = host['cpuspeed']
        if ('cpuused' in host):
            data['_meta']['hostvars'][host_name]['cpu_used'] = host['cpuused']
        data['_meta']['hostvars'][host_name]['created'] = host['created']
        data['_meta']['hostvars'][host_name]['memory'] = host['memory']
        data['_meta']['hostvars'][host_name]['tags'] = host['tags']
        data['_meta']['hostvars'][host_name]['hypervisor'] = host['hypervisor']
        data['_meta']['hostvars'][host_name]['created'] = host['created']
        data['_meta']['hostvars'][host_name]['nic'] = []
        for nic in host['nic']:
            data['_meta']['hostvars'][host_name]['nic'].append({
                'ip': nic['ipaddress'],
                'mac': nic['macaddress'],
                'netmask': nic['netmask'],
                'gateway': nic['gateway'],
                'type': nic['type'],
            })
            if nic['isdefault']:
                data['_meta']['hostvars'][host_name]['default_ip'] = nic['ipaddress']
        group_name = ''
        if ('group' in host):
            group_name = host['group']
        if (group_name and (group_name in data)):
            data[group_name]['hosts'].append(host_name)
    return data