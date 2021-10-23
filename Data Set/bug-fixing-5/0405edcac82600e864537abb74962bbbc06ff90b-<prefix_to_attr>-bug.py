def prefix_to_attr(attr_id):
    '\n     Helper method to convert ID prefix to mount target attribute\n    '
    attr_by_prefix = {
        'fsmt-': 'MountTargetId',
        'subnet-': 'SubnetId',
        'eni-': 'NetworkInterfaceId',
        'sg-': 'SecurityGroups',
    }
    prefix = first_or_default(filter((lambda pref: str(attr_id).startswith(pref)), attr_by_prefix.keys()))
    if prefix:
        return attr_by_prefix[prefix]
    return 'IpAddress'