def node_to_dict(self, inst):
    md = {
        
    }
    if (inst is None):
        return {
            
        }
    if inst.extra['metadata'].has_key('items'):
        for entry in inst.extra['metadata']['items']:
            md[entry['key']] = entry['value']
    net = inst.extra['networkInterfaces'][0]['network'].split('/')[(- 1)]
    if (self.ip_type == 'internal'):
        ssh_host = inst.private_ips[0]
    else:
        ssh_host = (inst.public_ips[0] if (len(inst.public_ips) >= 1) else inst.private_ips[0])
    return {
        'gce_uuid': inst.uuid,
        'gce_id': inst.id,
        'gce_image': inst.image,
        'gce_machine_type': inst.size,
        'gce_private_ip': inst.private_ips[0],
        'gce_public_ip': (inst.public_ips[0] if (len(inst.public_ips) >= 1) else None),
        'gce_name': inst.name,
        'gce_description': inst.extra['description'],
        'gce_status': inst.extra['status'],
        'gce_zone': inst.extra['zone'].name,
        'gce_tags': inst.extra['tags'],
        'gce_metadata': md,
        'gce_network': net,
        'ansible_ssh_host': ssh_host,
    }