def node_to_dict(self, inst):
    '\n        :type inst: params.VM\n        '
    if (inst is None):
        return {
            
        }
    inst.get_custom_properties()
    ips = ([ip.get_address() for ip in inst.get_guest_info().get_ips().get_ip()] if (inst.get_guest_info() is not None) else [])
    stats = {
        
    }
    for stat in inst.get_statistics().list():
        stats[stat.get_name()] = stat.get_values().get_value()[0].get_datum()
    return {
        'ovirt_uuid': inst.get_id(),
        'ovirt_id': inst.get_id(),
        'ovirt_image': inst.get_os().get_type(),
        'ovirt_machine_type': self.get_machine_type(inst),
        'ovirt_ips': ips,
        'ovirt_name': inst.get_name(),
        'ovirt_description': inst.get_description(),
        'ovirt_status': inst.get_status().get_state(),
        'ovirt_zone': inst.get_cluster().get_id(),
        'ovirt_tags': self.get_tags(inst),
        'ovirt_stats': stats,
        'ansible_ssh_host': (ips[0] if (len(ips) > 0) else None),
    }