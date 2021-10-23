def prefix_to_attr(attr_id):
    '\n     Helper method to convert ID prefix to mount target attribute\n    '
    attr_by_prefix = {
        'fsmt-': 'mount_target_id',
        'subnet-': 'subnet_id',
        'eni-': 'network_interface_id',
        'sg-': 'security_groups',
    }
    return first_or_default([attr_name for (prefix, attr_name) in attr_by_prefix.items() if str(attr_id).startswith(prefix)], 'ip_address')